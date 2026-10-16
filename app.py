import streamlit as st
import stripe
from supabase import create_client, Client
from groq import Groq

# ---------------------------------------------------------
# 1. INITIALISATION & CONFIGURATION DE LA PAGE
# ---------------------------------------------------------
st.set_page_config(
    page_title="The Empire Studio - AI Content Suite",
    page_icon="⚡",
    layout="wide"
)

# Initialisation des API via Streamlit Secrets
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
# 2. GESTION DE LA SESSION UTILISATEUR
# ---------------------------------------------------------
if "user" not in st.session_state:
    st.session_state.user = None

if "credits" not in st.session_state:
    st.session_state.credits = 0

def refresh_user_credits(user_id):
    """ Récupère le solde de crédits de l'utilisateur depuis Supabase """
    try:
        res = supabase.table("profiles").select("credits").eq("id", user_id).execute()
        if res.data:
            st.session_state.credits = res.data[0].get("credits", 0)
    except Exception as e:
        st.error(f"Erreur lors de la récupération des crédits : {e}")

# Vérification du retour de paiement Stripe (Success / Cancel)
query_params = st.query_params
if "success" in query_params:
    st.success("🎉 Paiement réussi ! Vos crédits ou votre abonnement ont été mis à jour.")
elif "canceled" in query_params:
    st.warning("⚠️ Le paiement a été annulé.")

# ---------------------------------------------------------
# 3. FONCTIONS D'ACHAT STRIPE CHECKOUT
# ---------------------------------------------------------
def recharger_via_stripe(price_id, user_email):
    """ Redirige vers la page de paiement sécurisée Stripe Checkout """
    try:
        is_subscription = (price_id != st.secrets["PRICE_SINGLE"])
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode='subscription' if is_subscription else 'payment',
            customer_email=user_email,
            success_url='https://the-empire-studio.streamlit.app/?success=true',
            cancel_url='https://the-empire-studio.streamlit.app/?canceled=true',
        )
        st.markdown(f'<meta http-equiv="refresh" content="0;url={session.url}">', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Erreur lors de l'initialisation du paiement Stripe : {e}")

# ---------------------------------------------------------
# 4. INTERFACE D'AUTHENTIFICATION (SI NON CONNECTÉ)
# ---------------------------------------------------------
if not st.session_state.user:
    st.title("⚡ The Empire Studio")
    st.subheader("Plateforme automatisée de création de contenu par IA")

    tab_login, tab_signup = st.tabs(["Connexion", "Créer un compte"])

    with tab_login:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Mot de passe", type="password", key="login_pass")
        if st.button("Se connecter", type="primary"):
            try:
                res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                st.session_state.user = res.user
                refresh_user_credits(res.user.id)
                st.rerun()
            except Exception as e:
                st.error(f"Erreur d'authentification : {e}")

    with tab_signup:
        new_email = st.text_input("Email", key="signup_email")
        new_password = st.text_input("Mot de passe", type="password", key="signup_pass")
        if st.button("Créer mon compte"):
            try:
                res = supabase.auth.sign_up({"email": new_email, "password": new_password})
                st.success("Compte créé avec succès ! Vous pouvez maintenant vous connecter.")
            except Exception as e:
                st.error(f"Erreur d'inscription : {e}")

    st.stop()

# ---------------------------------------------------------
# 5. APPLICATION PRINCIPALE (UTILISATEUR CONNECTÉ)
# ---------------------------------------------------------
# Mise à jour des crédits
refresh_user_credits(st.session_state.user.id)

# Barre latérale (Sidebar)
with st.sidebar:
    st.title("⚡ Empire Studio")
    st.write(f"👤 **Compte :** {st.session_state.user.email}")
    st.metric(label="Crédits disponibles", value=st.session_state.credits)

    if st.button("Se déconnecter"):
        supabase.auth.sign_out()
        st.session_state.user = None
        st.session_state.credits = 0
        st.rerun()

    st.divider()
    st.markdown("### 💳 Tarifs & Recharges")

    # Options d'achat
    if st.button("1 Crédit — 3,49 $", use_container_width=True):
        recharger_via_stripe(st.secrets["PRICE_SINGLE"], st.session_state.user.email)

    if st.button("Plan PRO (15 crédits) — 14,99 $/mois", use_container_width=True):
        recharger_via_stripe(st.secrets["PRICE_PRO"], st.session_state.user.email)

    if st.button("Plan PREMIUM (30 crédits) — 24,99 $/mois", use_container_width=True):
        recharger_via_stripe(st.secrets["PRICE_PREMIUM"], st.session_state.user.email)

    if st.button("Plan INFINITE (Illimité) — 49,99 $/mois", use_container_width=True):
        recharger_via_stripe(st.secrets["PRICE_INFINITE"], st.session_state.user.email)

# ---------------------------------------------------------
# 6. MODULES IA DU STUDIO
# ---------------------------------------------------------
st.title("🚀 Espace de Création")

tab_autoclip, tab_biocraft, tab_copycraft = st.tabs(["🎬 AutoClip AI", "👤 BioCraft AI", "✍️ CopyCraft AI"])

# --- MODULE 1: AutoClip AI ---
with tab_autoclip:
    st.header("🎬 AutoClip AI — Générateur de scripts vidéo")
    topic = st.text_input("Sujet de la vidéo ou du Reels/TikTok :", placeholder="ex: 3 conseils pour réussir en e-commerce")
    platform = st.selectbox("Plateforme :", ["TikTok / Shorts / Reels", "YouTube Long Format", "LinkedIn Video"])

    if st.button("Générer le script (-1 crédit)", type="primary"):
        if st.session_state.credits <= 0:
            st.error("❌ Crédits insuffisants. Veuillez recharger votre compte dans la barre latérale.")
        else:
            prompt = f"Rédige un script complet et très engagent pour une vidéo {platform} sur le sujet : '{topic}'."
            with st.spinner("Génération du script en cours..."):
                response = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}]
                )
                script = response.choices[0].message.content
                
                # Décrémenter 1 crédit dans Supabase
                new_credits = st.session_state.credits - 1
                supabase.table("profiles").update({"credits": new_credits}).eq("id", st.session_state.user.id).execute()
                st.session_state.credits = new_credits

                st.success("Script généré avec succès !")
                st.markdown(script)

# --- MODULE 2: BioCraft AI ---
with tab_biocraft:
    st.header("👤 BioCraft AI — Optimisation de profil")
    bio_topic = st.text_input("Quelle est votre activité ou niche ?", placeholder="ex: Producteur de House Music & Créateur TikTok")
    
    if st.button("Générer les Bio (-1 crédit)"):
        if st.session_state.credits <= 0:
            st.error("❌ Crédits insuffisants. Veuillez recharger votre compte dans la barre latérale.")
        else:
            prompt = f"Propose 3 descriptions courtes, percutantes et optimisées avec émojis pour un profil Instagram/TikTok dans la niche : '{bio_topic}'."
            with st.spinner("Optimisation en cours..."):
                response = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}]
                )
                bios = response.choices[0].message.content

                new_credits = st.session_state.credits - 1
                supabase.table("profiles").update({"credits": new_credits}).eq("id", st.session_state.user.id).execute()
                st.session_state.credits = new_credits

                st.success("Bio générées !")
                st.markdown(bios)

# --- MODULE 3: CopyCraft AI ---
with tab_copycraft:
    st.header("✍️ CopyCraft AI — Rédaction commerciale")
    copy_topic = st.text_area("Décrivez votre produit ou service :", placeholder="ex: Une montre Citizen Promaster Dive Eco-Drive 200m")
    
    if st.button("Rédiger l'accroche (-1 crédit)"):
        if st.session_state.credits <= 0:
            st.error("❌ Crédits insuffisants. Veuillez recharger votre compte dans la barre latérale.")
        else:
            prompt = f"Rédige une fiche produit persuasive et vendeuse pour : '{copy_topic}'."
            with st.spinner("Rédaction en cours..."):
                response = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}]
                )
                copy_text = response.choices[0].message.content

                new_credits = st.session_state.credits - 1
                supabase.table("profiles").update({"credits": new_credits}).eq("id", st.session_state.user.id).execute()
                st.session_state.credits = new_credits

                st.success("Contenu rédigé !")
                st.markdown(copy_text)
