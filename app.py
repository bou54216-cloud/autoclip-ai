import streamlit as st
import stripe
from supabase import create_client, Client
from groq import Groq
import streamlit.components.v1 as components

# ---------------------------------------------------------
# 1. CONFIGURATION ET DESIGN CSS PREMIUM
# ---------------------------------------------------------
st.set_page_config(
    page_title="AutoClip AI — Studio de Automation & Scripting Vidéo Pro",
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
    st.markdown("<p style='text-align: center; color: #888;'>Générateur de Scripts & Master-Prompts pour Génération Vidéo IA</p>", unsafe_allow_html=True)
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
st.title("🎬 AutoClip AI — Studio de Production Vidéo & Automation IA")
st.markdown("Configurez la vidéo à produire : obtenez soit un script de tournage humain, soit un Master-Prompt clé en main pour générer la vidéo par IA.")

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    topic = st.text_input("🎯 Sujet / Concept exact :", placeholder="ex: 3 astuces pour créer un banger House Music sur FL Studio")
    creator_type = st.radio("👤 Type de réalisation :", ["Générée 100% par IA (InVideo / Runway / Sora / CapCut)", "Personne Réelle (Face Cam / Tournage réel)"])
    platform = st.selectbox("📱 Plateforme :", ["TikTok", "Instagram Reels", "YouTube Shorts", "YouTube Format Long", "LinkedIn Vidéo"])

with col2:
    duration = st.selectbox("⏱️ Durée de la vidéo :", ["Flash (15 - 30 sec)", "Standard Short (30 - 60 sec)", "Long Short (60 - 90 sec)", "Format Long (3 - 5 min)"])
    tone = st.selectbox("🎭 Ambiance & Ton :", ["Dynamique, Énergique & Futuriste", "Dark, Mystérieux & Captivant", "Éducatif, Clair & Expert", "Luxe, Minimaliste & Premium", "Cash & Provocateur"])
    hook_style = st.selectbox("🪝 Style de Hook (Accroche) :", ["Question choc / Provocation", "Fait incroyable / Statistique", "Mise en garde / Erreur grave", "Scénario 'Imagine si...'", "Mythe populaire à détruire"])

with col3:
    structure = st.selectbox("🏗️ Structure narrative :", ["Problème -> Agitation -> Solution", "3 étapes pas-à-pas", "Avant / Après (Transformation)", "Histoire courte / Storytelling"])
    cta_type = st.selectbox("🎯 Call To Action (CTA) :", ["Commenter un mot-clé pour recevoir un lien", "S'abonner pour ne rien rater", "Cliquer sur le lien en bio", "Partager la vidéo à un ami"])
    extra_details = st.text_area("⚙️ Éléments visuels / Mots-clés imposés :", placeholder="ex: Ambiance studio de musique néon sombre, sons de synthétiseur, rythme rapide...")

st.divider()

if st.button("⚡ Générer le Script & Master-Prompt (-1 crédit)", type="primary", use_container_width=True):
    if st.session_state.credits <= 0:
        st.error("❌ Crédits insuffisants. Veuillez recharger votre solde dans la barre latérale.")
    else:
        # Prompt dynamique adapté selon la sélection (IA vs Humain)
        if creator_type == "Générée 100% par IA (InVideo / Runway / Sora / CapCut)":
            prompt = f"""
            Tu es un Prompt Engineer et Réalisateur Vidéo IA Senior.
            L'utilisateur souhaite générer une vidéo intégrale via un outil d'IA vidéo (comme InVideo AI, Runway Gen-2, Sora, CapCut AI, HeyGen, etc.).

            Rédige un MASTER-PROMPT DE GÉNÉRATION AUTOMATIQUE ainsi qu'un découpage ultra-rigoureux.

            --- CONFIGURATION DU PROJET ---
            - Sujet : {topic}
            - Mode : 100% Généré par IA (Faceless Automation)
            - Plateforme : {platform}
            - Durée : {duration}
            - Style & Ton : {tone}
            - Hook : {hook_style}
            - Structure : {structure}
            - CTA : {cta_type}
            - Consignes visuelles : {extra_details if extra_details else 'Aucune'}

            --- FORMAT DE SORTIE IMPÉRATIF (Markdown propre) ---

            ### 🤖 1. MASTER-PROMPT CLÉ EN MAIN (À copier-coller directement dans InVideo AI / CapCut / Sora)
            `[Rédige un prompt global en Anglais hyper-détaillé décrivant le sujet, le style visuel 8k, le rythme de coupe, la voix-off, la musique de fond et la structure globale]`

            ---

            ### 🎙️ 2. SCRIPT VOIX-OFF (VOICEOVER) EXCLUSIF (Pour ElevenLabs ou synthèse vocale)
            - **Langue** : Français
            - **Style de voix recommandé** : [Ex: Homme, voix grave, ton énergique]
            - **Texte exact à lire (mot à mot avec annotations de pause `[pause]` et d'emphase)** :
            "..."

            ---

            ### 🎬 3. DÉCOUPAGE SCÈNE PAR SCÈNE & PROMPTS VISUELS (Midjourney / Runway / Sora)

            * **Scène 1 : HOOK (0 à 3s)**
              - **Visuel IA (Prompt Runway/Midjourney en Anglais)** : `...`
              - **Texte incrusté à l'écran** : "..."
              - **Effet Sonore (SFX)** : [Whoosh / Boom]

            * **Scène 2 : DÉVELOPPEMENT (3s à 15s)**
              - **Visuel IA (Prompt Runway/Midjourney en Anglais)** : `...`
              - **Texte incrusté à l'écran** : "..."

            * **Scène 3 : CONSEILS / SOLUTION (15s à 30s)**
              - **Visuel IA (Prompt Runway/Midjourney en Anglais)** : `...`
              - **Texte incrusté à l'écran** : "..."

            * **Scène 4 : CALL TO ACTION (30s à fin)**
              - **Visuel IA (Prompt Runway/Midjourney en Anglais)** : `...`
              - **Animation / Incrustation** : [Flèche vers le profil / Bouton Follow]

            ---

            ### 🎵 4. PARAMÈTRES AUDIO & MONTAGE
            - **Style de musique conseillé** : [Genre + BPM exact]
            - **Fréquence des coupes** : [ex: Changement de plan toutes les 1.2 secondes]
            """
        else:
            prompt = f"""
            Tu es un Directeur Artistique et Copywriter Vidéo Senior.
            L'utilisateur tourne une vidéo incarnée (Face Cam / Personne réelle).
            Rédige un script de tournage hyper précis.

            --- CONFIGURATION ---
            - Sujet : {topic}
            - Mode : Présentateur Réel
            - Plateforme : {platform}
            - Durée : {duration}
            - Ton : {tone}
            - Hook : {hook_style}
            - Structure : {structure}
            - CTA : {cta_type}
            - Mots-clés : {extra_details if extra_details else 'Aucun'}

            --- FORMAT DE SORTIE ---
            ### 📌 1. FICHE TECHNIQUE & MATÉRIEL
            - **Axe de caméra / Cadrage** : (Plan poitrine, smartphone vertical)
            - **Ambiance & Éclairage** : (Rétroéclairage néon, lumière douce)

            ### 🪝 2. LE HOOK (0-3s)
            - **Acteur (Dialogue)** : "..."
            - **Jeu d'acteur / Geste** : [Rapprocher rapidement le visage de l'objectif]
            - **Texte à l'écran** : "..."

            ### 🎬 3. SCRIPT COMPLET DÉCOUPÉ
            * **[0:03 - 0:15] Partie 1 : Le Problème**
              - **Dialogue** : "..."
              - **B-Roll à insérer** : [Insérer une capture d'écran / vidéo d'illustration]

            * **[0:15 - 0:35] Partie 2 : La Solution & Astuces**
              - **Dialogue** : "..."
              - **B-Roll à insérer** : [Illustration visuelle]

            ### 🎯 4. CONCLUSION & CALL TO ACTION
            - **Dialogue** : "..."
            - **Action visuelle** : [Pointer du doigt le bas de l'écran]
            """

        with st.spinner("🎬 Génération du plan de production en cours..."):
            try:
                response = groq_client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[{"role": "user", "content": prompt}]
                )
                script = response.choices[0].message.content

                new_credits = st.session_state.credits - 1
                supabase.table("profiles").update({"credits": new_credits}).eq("id", st.session_state.user.id).execute()
                st.session_state.credits = new_credits

                st.success("✨ Master-Prompt & Script générés avec succès !")
                st.markdown(script)

            except Exception as e:
                st.error(f"Erreur lors de la génération : {e}")
