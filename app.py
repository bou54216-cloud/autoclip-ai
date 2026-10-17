import streamlit as st
import stripe
from supabase import create_client, Client
from groq import Groq
import streamlit.components.v1 as components

# ---------------------------------------------------------
# 1. CONFIGURATION ET DESIGN CSS PREMIUM
# ---------------------------------------------------------
st.set_page_config(
    page_title="AutoClip AI — Studio de Scripts Vidéo Pro",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp { background-color: #0E1117; }
    div[data-testid="stVerticalBlock"] > div { border-radius: 10px; }
    .stButton>button { border-radius: 8px; font-weight: 600; transition: all 0.3s ease; }
    
    /* Style pour encadrer le rendu du script */
    .script-container {
        background-color: #161B22;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #30363D;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. INITIALISATION DES APIS
# ---------------------------------------------------------
stripe.api_key = st.secrets["STRIPE_API_KEY"]

@st.cache_resource
def init_supabase() -> Client:
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

supabase = init_supabase()

@st.cache_resource
def init_groq():
    return Groq(api_key=st.secrets["GROQ_API_KEY"])

groq_client = init_groq()

# ---------------------------------------------------------
# 3. GESTION DE LA SESSION & DES CRÉDITS
# ---------------------------------------------------------
if "user" not in st.session_state:
    st.session_state.user = None

if "credits" not in st.session_state:
    st.session_state.credits = 0

def refresh_user_credits(user_id):
    try:
        res = supabase.table("profiles").select("credits").eq("id", user_id).execute()
        if res.data and len(res.data) > 0:
            st.session_state.credits = res.data[0].get("credits", 0)
        else:
            supabase.table("profiles").insert({"id": user_id, "email": st.session_state.user.email, "credits": 5}).execute()
            st.session_state.credits = 5
    except Exception as e:
        st.error(f"Erreur de synchronisation Supabase : {e}")

# ---------------------------------------------------------
# 4. FONCTION REDIRECTION STRIPE CHECKOUT
# ---------------------------------------------------------
def recharger_via_stripe(price_id, user_email):
    try:
        is_subscription = (price_id != st.secrets["PRICE_SINGLE"])
        
        session = stripe.checkout.Session.create(
            line_items=[{'price': price_id, 'quantity': 1}],
            mode='subscription' if is_subscription else 'payment',
            customer_email=user_email,
            success_url=f"https://the-empire-studio.streamlit.app/?success=true&price_id={price_id}",
            cancel_url='https://the-empire-studio.streamlit.app/?canceled=true',
            managed_payments={'enabled': False},
        )
        
        js = f"<script>window.top.location.href = '{session.url}';</script>"
        components.html(js, height=0)
        st.info("Redirection sécurisée vers Stripe Checkout...")
        st.markdown(f"[👉 Cliquez ici si la redirection ne démarre pas]({session.url})")
        
    except Exception as e:
        st.error(f"Erreur de paiement Stripe : {e}")

# ---------------------------------------------------------
# 5. ECRAN DE CONNEXION / INSCRIPTION
# ---------------------------------------------------------
if not st.session_state.user:
    st.markdown("<h1 style='text-align: center;'>🎬 AutoClip AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888;'>Générateur de Scripts Vidéo Haute Conversion pour Créateurs & Marques</p>", unsafe_allow_html=True)
    st.divider()

    col_auth, _ = st.columns([1, 1])
    with col_auth:
        tab_login, tab_signup = st.tabs(["🔑 Connexion", "📝 Créer un compte"])

        with tab_login:
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Mot de passe", type="password", key="login_pass")
            if st.button("Se connecter", type="primary", use_container_width=True):
                try:
                    res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                    st.session_state.user = res.user
                    refresh_user_credits(res.user.id)
                    st.rerun()
                except Exception as e:
                    st.error(f"Erreur de connexion : {e}")

        with tab_signup:
            new_email = st.text_input("Email", key="signup_email")
            new_password = st.text_input("Mot de passe", type="password", key="signup_pass")
            if st.button("Créer mon compte", use_container_width=True):
                try:
                    res = supabase.auth.sign_up({"email": new_email, "password": new_password})
                    st.success("Compte créé ! Vous pouvez vous connecter.")
                except Exception as e:
                    st.error(f"Erreur d'inscription : {e}")

    st.stop()

# ---------------------------------------------------------
# 6. APPLICATION PRINCIPALE & BARRE LATÉRALE
# ---------------------------------------------------------
refresh_user_credits(st.session_state.user.id)

query_params = st.query_params

if "success" in query_params and "payment_processed" not in st.session_state:
    price_id_paid = query_params.get("price_id", "")
    
    credits_to_add = 1
    if price_id_paid == st.secrets.get("PRICE_PRO"):
        credits_to_add = 15
    elif price_id_paid == st.secrets.get("PRICE_PREMIUM"):
        credits_to_add = 30
    elif price_id_paid == st.secrets.get("PRICE_INFINITE"):
        credits_to_add = 999

    try:
        new_credits = st.session_state.credits + credits_to_add
        supabase.table("profiles").update({"credits": new_credits}).eq("id", st.session_state.user.id).execute()
        st.session_state.credits = new_credits
        st.session_state.payment_processed = True
        st.balloons()
        st.success(f"🎉 Paiement validé ! +{credits_to_add} crédits ajoutés à votre compte.")
    except Exception as e:
        st.error(f"Erreur lors du crédit de la commande : {e}")

elif "canceled" in query_params:
    st.warning("⚠️ Transaction annulée.")

# --- BARRE LATÉRALE (SIDEBAR) ---
with st.sidebar:
    st.title("🎬 AutoClip Studio")
    st.write(f"👤 **Membre :** {st.session_state.user.email}")
    st.metric(label="Solde de Crédits", value=f"{st.session_state.credits} CR")
    
    if st.button("Se déconnecter", use_container_width=True):
        supabase.auth.sign_out()
        st.session_state.user = None
        st.session_state.credits = 0
        st.rerun()

    st.divider()
    st.markdown("### 💳 Offres & Recharges")

    if st.button("1 Crédit — 3,49 $", use_container_width=True):
        recharger_via_stripe(st.secrets["PRICE_SINGLE"], st.session_state.user.email)

    if st.button("PRO (15 crédits) — 14,99 $/m", use_container_width=True):
        recharger_via_stripe(st.secrets["PRICE_PRO"], st.session_state.user.email)

    if st.button("PREMIUM (30 crédits) — 24,99 $/m", use_container_width=True):
        recharger_via_stripe(st.secrets["PRICE_PREMIUM"], st.session_state.user.email)

    if st.button("INFINITE (Illimité) — 49,99 $/m", use_container_width=True):
        recharger_via_stripe(st.secrets["PRICE_INFINITE"], st.session_state.user.email)

# ---------------------------------------------------------
# 7. MODULE UNIQUE : AUTOCLIP AI ULTRA-APPROFONDI
# ---------------------------------------------------------
st.title("🎬 AutoClip AI — Studio de Scripting Vidéo Pro")
st.markdown("Configurez vos critères avec précision pour générer un découpage vidéo professionnel sur-mesure.")

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    topic = st.text_input("🎯 Sujet / Concept de la vidéo :", placeholder="ex: 3 secrets pour produire de la house music captivante")
    creator_type = st.radio("👤 Type de créateur / Présentateur :", ["Personne Réelle (Face Cam)", "IA / Faceless (Avatar / Voix Off / B-Roll)"])
    platform = st.selectbox("📱 Plateforme cible :", ["TikTok", "Instagram Reels", "YouTube Shorts", "YouTube Format Long", "LinkedIn Vidéo"])

with col2:
    duration = st.selectbox("⏱️ Durée souhaitée :", ["Ultra-court (15 à 30 sec)", "Standard Short (30 à 60 sec)", "Long Short (60 à 90 sec)", "Format Long (3 à 5 min)"])
    tone = st.selectbox("🎭 Ton & Style d'énergie :", ["Dynamique & Cash", "Éducatif & Inspirant", "Mystérieux & Captivant", "Humoristique & Décalé", "Corporate & Expert"])
    hook_style = st.selectbox("🪝 Style de Hook (Accroche) :", ["Question choc / Provocation", "Chiffre / Statistique incroyable", "Scénario 'Imagine si...'", "Mythe populaire à déconstruire", "Avertissement / Erreur grave"])

with col3:
    structure = st.selectbox("🏗️ Structure narrative :", ["Problème -> Agitation -> Solution", "Storytelling dramatique", "Méthode pas-à-pas (1, 2, 3)", "Avant / Après (Transformation)"])
    cta_type = st.selectbox("🎯 Objectif du Call To Action (CTA) :", ["Commenter un mot-clé précis", "S'abonner pour la partie 2", "Cliquer sur le lien en bio", "Partager la vidéo"])
    extra_details = st.text_area("✍️ Mots-clés / Consignes spécifiques :", placeholder="ex: Parler de tempo 128 BPM, ajouter une ambiance néon sombre...")

st.divider()

if st.button("🚀 Générer le Script Vidéo Ultra-Détaillé (-1 crédit)", type="primary", use_container_width=True):
    if st.session_state.credits <= 0:
        st.error("❌ Crédits insuffisants. Veuillez recharger votre solde dans la barre latérale.")
    else:
        # Prompt ultra-directif pour forcer un rendu structuré et non vague
        prompt = f"""
        Tu es un Réalisateur Vidéo et Copywriter Expert pour réseaux sociaux.
        Rédige un script complet et hyper structuré pour une vidéo court-format.

        --- CRITÈRES DE PRODUCTION ---
        - Sujet : {topic}
        - Présentateur : {creator_type}
        - Plateforme : {platform}
        - Durée : {duration}
        - Ton / Énergie : {tone}
        - Style de Hook (0-3 sec) : {hook_style}
        - Structure narrative : {structure}
        - Objectif CTA : {cta_type}
        - Consignes / Mots-clés : {extra_details if extra_details else 'Aucun'}

        --- FORMAT DE RÉPONSE EXIGÉ ---
        Structure impérativement ton résultat avec les sections suivantes en Markdown propre :

        ### 📌 1. FICHE TECHNIQUE DE LA VIDÉO
        - **Format & Cadrage** : (ex: 9:16 Vertical, plan serré / plan large)
        - **Ambiance Sonore / Musique** : (ex: House dynamique à 128 BPM, fondu d'entrée)
        - **Style d'Édition** : (ex: Rythme de coupe rapide toutes les 1.5s, sous-titres dynamiques jaune/blanc)

        ---

        ### 🪝 2. LE HOOK (0 à 3 Secondes - Maintien de l'attention)
        - **Texte Parlé (Voiceover)** : "..."
        - **Visuel à l'écran** : [Préciser ce que l'on voit ou ce que fait l'avatar/personne]
        - **Texte en Gros à l'écran (On-Screen Text)** : "..."
        - **Effet Sonore (SFX)** : [ex: Whoosh / Explosion sound]

        ---

        ### 🎬 3. DÉCOUPAGE SCÈNE PAR SCÈNE (Script Complet)
        Fournis un tableau Markdown ou une liste détaillée horodatée :

        * **[0:03 - 0:10] Scène 1 : Introduction de la problématique**
          - **Voix / Discours** : "..."
          - **Visuel / B-Roll** : [Description exacte de l'image ou vidéo d'illustration]
          - **Texte / Graphisme** : [Mots-clés affichés]

        * **[0:10 - 0:25] Scène 2 : Développement & Conseils clés**
          - **Voix / Discours** : "..."
          - **Visuel / B-Roll** : [Description visuelle]
          - **Texte / Graphisme** : [Mots-clés affichés]

        * **[0:25 - 0:40] Scène 3 : Preuve / Démonstration / Exemple**
          - **Voix / Discours** : "..."
          - **Visuel / B-Roll** : [Description visuelle]

        ---

        ### 🎯 4. CALL TO ACTION (CTA & Engagement)
        - **Discours Final** : "..."
        - **Visuel / Animation** : [Animation d'abonnement / Flèche vers le profil]

        ---

        ### 🤖 5. PROMPTS IA PRÊTS À L'EMPLOI (Pour la génération visuelle & sonore)
        - **Prompt Midjourney / Leonardo (B-Roll / Images)** : `...`
        - **Prompt Voix Off ElevenLabs (Style de voix)** : `...`
        """

        with st.spinner("🎬 Rédaction du script vidéo structuré en cours..."):
            try:
                response = groq_client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[{"role": "user", "content": prompt}]
                )
                script = response.choices[0].message.content

                # Décrémenter 1 crédit
                new_credits = st.session_state.credits - 1
                supabase.table("profiles").update({"credits": new_credits}).eq("id", st.session_state.user.id).execute()
                st.session_state.credits = new_credits

                st.success("✨ Script généré avec succès !")
                st.markdown(script)

            except Exception as e:
                st.error(f"Erreur lors de la génération : {e}")
