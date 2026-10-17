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
    st.markdown("<p style='text-align: center; color: #888;'>Générateur de Scripts & Master-Prompts Vidéo Haute Définition</p>", unsafe_allow_html=True)
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
# 7. MODULE AUTOCLIP AI DE PRÉCISION
# ---------------------------------------------------------
st.title("🎬 AutoClip AI — Studio de Scripting & Production Vidéo")
st.markdown("Choisissez le type de vidéo (Tournage réel ou Génération par IA) pour obtenir un script complet, minuté et sur-mesure.")

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    topic = st.text_input("🎯 Sujet / Thème de la vidéo :", placeholder="ex: 3 astuces pour créer un banger House Music")
    creator_type = st.radio("👤 Format de vidéo :", ["Générée par IA (Automation / Faceless)", "Personne Réelle (Face Cam / Tournage réel)"])
    platform = st.selectbox("📱 Plateforme cible :", ["TikTok", "Instagram Reels", "YouTube Shorts", "YouTube Format Long", "LinkedIn Vidéo"])

with col2:
    duration = st.selectbox("⏱️ Durée souhaitée :", ["Courte (15 à 30 sec)", "Standard (30 à 60 sec)", "Long Short (60 à 90 sec)", "Format Long (3 à 5 min)"])
    tone = st.selectbox("🎭 Ambiance & Énergie :", ["Dynamique & Captivant", "Cash, Direct & Provocateur", "Éducatif, Clair & Expert", "Luxe, Sombre & Premium", "Humoristique & Décalé"])
    hook_style = st.selectbox("🪝 Style d'accroche (Hook) :", ["Question choc / Provocation", "Statistique / Chiffre incroyable", "Mise en garde / Erreur grave", "Scénario 'Imagine si...'", "Mythe populaire à déconstruire"])

with col3:
    structure = st.selectbox("🏗️ Structure narrative :", ["Problème -> Agitation -> Solution", "Méthode en 3 étapes pas-à-pas", "Avant / Après (Transformation)", "Storytelling / Récit captivant"])
    cta_type = st.selectbox("🎯 Objectif du Call To Action (CTA) :", ["Commenter un mot-clé précis", "S'abonner pour la suite", "Cliquer sur le lien en bio", "Partager la vidéo"])
    extra_details = st.text_area("⚙️ Détails visuels / Mots-clés imposés :", placeholder="ex: Ambiance studio de musique néon sombre, tempo 128 BPM, sons de synthétiseur...")

st.divider()

if st.button("🚀 Générer le Script Ultra-Détaillé (-1 crédit)", type="primary", use_container_width=True):
    if st.session_state.credits <= 0:
        st.error("❌ Crédits insuffisants. Veuillez recharger votre solde dans la barre latérale.")
    else:
        # Traitement selon le choix (IA neutre vs Tournage réel)
        if creator_type == "Générée par IA (Automation / Faceless)":
            prompt = f"""
            Tu es un Directeur Artistique et Expert en Automation Vidéo.
            Rédige un SCRIPT ULTRA-DÉTAILLÉ ET LONG destiné à être généré par un moteur d'IA vidéo.
            NE CITE AUCUN NOM D'APPLICATION NI DE LOGICIEL TIERS.

            --- CONFIGURATION DE LA VIDÉO ---
            - Sujet : {topic}
            - Mode : Généré par IA (Faceless / Automation)
            - Plateforme : {platform}
            - Durée : {duration}
            - Style & Ton : {tone}
            - Style de Hook (0-3s) : {hook_style}
            - Structure narrative : {structure}
            - Call To Action : {cta_type}
            - Consignes spécifiques : {extra_details if extra_details else 'Aucune'}

            --- FORMAT DE SORTIE EXIGÉ (Markdown clair) ---

            # 🤖 PLAN DE GÉNÉRATION & MASTER-PROMPT

            ### 📝 1. MASTER-PROMPT GLOBAL DE SÉQUENCE (En Anglais)
            `[Rédige un prompt global en anglais décrivant la scène entière, le style visuel photoréaliste 8K, le rendu cinématique, les couleurs, la vitesse des coupes et l'atmosphère sonore]`

            ---

            ### 🎙️ 2. SCRIPT VOIX-OFF (Texte intégral mot à mot)
            - **Intonation & Style vocal conseillé** : [ex: Voix masculine, ton grave, rythme rapide]
            - **Texte exact à lire** :
            "..."

            ---

            ### 🎬 3. DÉCOUPAGE DÉTAILLÉ SCÈNE PAR SCÈNE (Prompts visuels bruts)

            * **Scène 1 : HOOK (0 à 3s)**
              - **Prompt Visuel Brut (En Anglais)** : `...`
              - **Texte Incrusté à l'écran** : "..."
              - **Bruitage / Effet Sonore** : [Sound effect]

            * **Scène 2 : PROBLÈME & CONTEXTE (3s à 15s)**
              - **Prompt Visuel Brut (En Anglais)** : `...`
              - **Texte Incrusté à l'écran** : "..."
              - **Description du mouvement visuel** : [Ex: Camera zoom, slow motion]

            * **Scène 3 : SOLUTION & DÉVELOPPEMENT (15s à 35s)**
              - **Prompt Visuel Brut (En Anglais)** : `...`
              - **Texte Incrusté à l'écran** : "..."

            * **Scène 4 : CONCLUSION & CALL TO ACTION (35s à fin)**
              - **Prompt Visuel Brut (En Anglais)** : `...`
              - **Incrustation graphique** : [Animation bouton follow / flèche vers le profil]

            ---

            ### 🎵 4. PARAMÈTRES AUDIO & MONTAGE
            - **Ambiance musicale** : [Genre musical + Tempo BPM]
            - **Fréquence de transition visuelle** : [ex: Changement de plan toutes les 1.5s]
            """
        else:
            prompt = f"""
            Tu es un Réalisateur Vidéo Senior et Copywriter.
            Rédige un SCRIPT DE TOURNAGE ULTRA-DÉTAILLÉ ET LONG pour un présentateur réel (Face Cam).

            --- CONFIGURATION ---
            - Sujet : {topic}
            - Mode : Présentateur Réel
            - Plateforme : {platform}
            - Durée : {duration}
            - Ton : {tone}
            - Hook : {hook_style}
            - Structure : {structure}
            - CTA : {cta_type}
            - Exigences : {extra_details if extra_details else 'Aucune'}

            --- FORMAT DE SORTIE ---
            # 📋 PLAN DE TOURNAGE RÉEL

            ### ⚙️ 1. DIRECTION ARTISTIQUE & SETUP
            - **Cadrage & Plan** : [ex: Plan poitrine, axe vertical 9:16]
            - **Éclairage & Décor** : [Lumières, ambiance, arrière-plan]

            ### 🪝 2. HOOK (0-5 SECONDES)
            * **Timecode** : `00:00 - 00:05`
            * **Réplique exacte** : "..."
            * **Jeu d'acteur / Geste** : [Expression, posture, mouvement]
            * **Texte à l'écran** : "..."

            ### 🎬 3. DÉCOUPAGE SÉQUENTIEL DÉTAILLÉ
            * **[0:05 - 0:20] Séquence 1 : Agitation du Problème**
              - **Dialogue** : "..."
              - **Plan de coupe / B-Roll** : [Visuel à ajouter]

            * **[0:20 - 0:45] Séquence 2 : Conseils & Démonstration**
              - **Dialogue** : "..."
              - **Plan de coupe / B-Roll** : [Visuel à ajouter]

            ### 🎯 4. CONCLUSION & CALL TO ACTION
            * **Réplique finale** : "..."
            * **Action visuelle** : [Pointer du doigt, geste d'incitation]
            """

        with st.spinner("🎬 Génération du script de production en cours..."):
            try:
                response = groq_client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[{"role": "user", "content": prompt}]
                )
                script = response.choices[0].message.content

                new_credits = st.session_state.credits - 1
                supabase.table("profiles").update({"credits": new_credits}).eq("id", st.session_state.user.id).execute()
                st.session_state.credits = new_credits

                st.success("✨ Script généré avec succès !")
                st.markdown(script)

            except Exception as e:
                st.error(f"Erreur lors de la génération : {e}")
