import streamlit as st
import stripe
from supabase import create_client, Client
from groq import Groq
import streamlit.components.v1 as components

# ---------------------------------------------------------
# 1. CONFIGURATION ET DESIGN CSS PREMIUM
# ---------------------------------------------------------
st.set_page_config(
    page_title="AutoClip AI — Studio de Scripting Vidéo Pro",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp { background-color: #0E1117; }
    div[data-testid="stVerticalBlock"] > div { border-radius: 10px; }
    .stButton>button { border-radius: 8px; font-weight: 600; transition: all 0.3s ease; }
    
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
    st.markdown("<p style='text-align: center; color: #888;'>Générateur de Scripts de Tournage Ultra-Détaillés & Professionnels</p>", unsafe_allow_html=True)
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
# 7. MODULE AUTOCLIP AI : SCRIPT DE TOURNAGE ULTRA-DÉTAILLÉ
# ---------------------------------------------------------
st.title("🎬 AutoClip AI — Studio de Scripting Vidéo Avancé")
st.markdown("Renseignez vos éléments clés pour générer un script de tournage complet, minuté et extrêmement précis.")

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    topic = st.text_input("🎯 Sujet / Thème exact de la vidéo :", placeholder="ex: 3 techniques pro pour faire sonner un kick House Music en club")
    platform = st.selectbox("📱 Plateforme cible :", ["TikTok", "Instagram Reels", "YouTube Shorts", "YouTube Format Long", "LinkedIn Vidéo"])
    duration = st.selectbox("⏱️ Durée souhaitée :", ["Courte (30 à 45 sec)", "Standard (60 à 90 sec)", "Format Long (3 à 5 min)", "Format Approfondi (5 à 10 min)"])

with col2:
    creator_type = st.radio("👤 Format du tournage :", ["Face Cam (Présentateur incarné)", "Voix Off sur images réelles (B-Rolls)", "Format mixte (Face Cam + Démonstration écran/écran)"])
    tone = st.selectbox("🎭 Ambiance & Énergie :", ["Dynamique & Énergique", "Cash, Provocateur & Impactant", "Pédagogique, Calme & Expert", "Luxe, Épuré & Premium", "Humoristique & Décalé"])
    hook_style = st.selectbox("🪝 Style d'accroche (Hook) :", ["Question choc / Provocation", "Chiffre / Statistique incroyable", "Erreur grave à éviter absolument", "Mise en scène 'Imagine si...'", "Mythe populaire à briser"])

with col3:
    structure = st.selectbox("🏗️ Structure narrative :", ["Problème -> Agitation -> Solution complète", "Les 3 piliers essentiels (1, 2, 3)", "Avant / Après (Etude de cas / Transformation)", "Format Storytelling / Récit d'expérience"])
    cta_type = st.selectbox("🎯 Objectif du Call To Action (CTA) :", ["Commenter un mot-clé précis", "S'abonner pour ne pas rater la partie 2", "Cliquer sur le lien en bio", "Partager la vidéo à un ami"])
    extra_details = st.text_area("⚙️ Détails / Termes / Contraintes spécifiques :", placeholder="ex: Parler de sidechain compression, 128 BPM, éclairage rouge/bleu studio...")

st.divider()

if st.button("🚀 Générer le Script de Tournage Ultra-Détaillé (-1 crédit)", type="primary", use_container_width=True):
    if st.session_state.credits <= 0:
        st.error("❌ Crédits insuffisants. Veuillez recharger votre solde dans la barre latérale.")
    else:
        prompt = f"""
        Tu es un Réalisateur Vidéo Senior, Directeur de Production et Copywriter de niveau mondial.
        Rédige un SCRIPT DE TOURNAGE EXTÊMEMENT LONG, PRÉCIS ET DÉTAILLÉ pour une vidéo sur les réseaux sociaux.

        Le script doit être exhaustif et exploitable immédiatement sur un plateau de tournage ou en studio.

        --- FICHE DU PROJET ---
        - Sujet : {topic}
        - Plateforme : {platform}
        - Durée visée : {duration}
        - Format de tournage : {creator_type}
        - Ton & Ambiance : {tone}
        - Style d'accroche (Hook) : {hook_style}
        - Structure narrative : {structure}
        - Call To Action (CTA) : {cta_type}
        - Exigences spécifiques : {extra_details if extra_details else 'Aucune'}

        --- FORMAT DE RÉPONSE EXIGÉ (Markdown structuré) ---

        # 📋 PLAN DE PRODUCTION & TOURNAGE

        ### ⚙️ 1. SETUP DE TOURNAGE & DIRECTION ARTISTIQUE
        - **Cadrage & Format** : [ex: 9:16 Vertical / Plan américain / Gros plan]
        - **Éclairage & Ambiance** : [Description précise des lumières, couleurs et contrastes]
        - **Décor & Arrière-plan** : [Éléments à afficher en fond, rangement, accessoires]
        - **Audio & Style sonore** : [Type de micro, musique de fond exacte, tempo/BPM]
        - **Rythme de montage conseillé** : [Fréquence des cuts, zoom in/out, transitions]

        ---

        ### 🪝 2. L'ACCROCHE (HOOK - 0 à 5 SECONDES)
        * **Timecode** : `00:00 - 00:05`
        * **Réplique exacte à dire (Mot à mot)** : "..."
        * **Jeu d'acteur / Mouvement** : [Expression du visage, geste des mains, déplacement]
        * **Axe caméra & Échelle de plan** : [Gros plan serré / Zoom rapide sur les yeux]
        * **Incrustation Texte à l'écran** : "..." [Style de police, couleur, position]
        * **Bruitage / Effet Sonore (SFX)** : [Whoosh / Boom / Glitch sound]

        ---

        ### 🎬 3. DÉCOUPAGE DÉTAILLÉ SÉQUENCE PAR SÉQUENCE (Séquencier Complet)

        Découpe tout le corps de la vidéo en plusieurs séquences numérotées, claires et exhaustives :

        #### 🔹 SÉQUENCE 1 : L'Agitation du Problème / Mise en contexte
        * **Timecode** : `00:05 - 00:20`
        * **Texte / Dialogues exacts** : "..."
        * **Action / Jeu du présentateur** : [Posture, ton de voix, intonation]
        * **Incrustration B-Roll / Plan d'illustration** : [Détail de la vidéo ou image à afficher au montage]
        * **Texte / Graphisme à l'écran** : [Mots-clés en gras / Flèches / Surlignage]
        * **Effet sonore (SFX)** : [Swoosh / Bip / Pop]

        #### 🔹 SÉQUENCE 2 : Le Premier Conseil / Élément Clé
        * **Timecode** : `00:20 - 00:45`
        * **Texte / Dialogues exacts** : "..."
        * **Action / Jeu du présentateur** : [Explication claire, gestuelle descriptive]
        * **Incrustration B-Roll / Plan d'illustration** : [Plan de coupe / Écran partagé / Zoom sur un détail]
        * **Texte / Graphisme à l'écran** : [Puces explicatives / Mots-clés]
        * **Effet sonore (SFX)** : [Transition sonore]

        #### 🔹 SÉQUENCE 3 : L'Astuce Avancée / La Démonstration
        * **Timecode** : `00:45 - 01:15`
        * **Texte / Dialogues exacts** : "..."
        * **Action / Jeu du présentateur** : [Démonstration pratique, montrer un écran ou un objet]
        * **Incrustration B-Roll / Plan d'illustration** : [Gros plan sur l'action ou l'outil]
        * **Texte / Graphisme à l'écran** : [Données / Chiffres clés / Schéma]

        #### 🔹 SÉQUENCE 4 : Résolution & Bénéfice principal
        * **Timecode** : `01:15 - 01:40`
        * **Texte / Dialogues exacts** : "..."
        * **Action / Jeu du présentateur** : [Regard direct caméra, ton rassurant et convaincant]
        * **Incrustration B-Roll / Plan d'illustration** : [Plan large ou résultat final]

        ---

        ### 🎯 4. CALL TO ACTION & CONCLUSION (FIN DE VIDÉO)
        * **Timecode** : `Fin de vidéo`
        * **Réplique exacte** : "..."
        * **Action visuelle du présentateur** : [Pointer du doigt vers le bas / Faire un signe de la main]
        * **Incrustation Graphique** : [Animation de bouton s'abonner / Mot-clé à commenter]
        * **Musique / Outro** : [Fondu sonore descendant]

        ---

        ### 💡 5. CONSEILS DU RÉALISATEUR POUR LE MONTAGE FINAL
        - **Style de sous-titres** : [Style dynamique, couleur mot par mot]
        - **Erreurs fréquentes à éviter lors du tournage** : [Conseils de lumière, d'articulation ou de rythme]
        """

        with st.spinner("🎬 Rédaction du script de tournage ultra-long et détaillé en cours..."):
            try:
                response = groq_client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[{"role": "user", "content": prompt}]
                )
                script = response.choices[0].message.content

                new_credits = st.session_state.credits - 1
                supabase.table("profiles").update({"credits": new_credits}).eq("id", st.session_state.user.id).execute()
                st.session_state.credits = new_credits

                st.success("✨ Script de tournage ultra-détaillé généré avec succès !")
                st.markdown(script)

            except Exception as e:
                st.error(f"Erreur lors de la génération : {e}")
