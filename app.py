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
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode='subscription' if is_subscription else 'payment',
            customer_email=user_email,
            success_url='https://the-empire-studio.streamlit.app/?success=true',
            cancel_url='https://the-empire-studio.streamlit.app/?canceled=true',
            managed_payments={'enabled': False},  # <-- Désactive l'exigence de code taxe
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

# --- MODULE 1: AutoClip AI (Version Complète) ---
with tab_autoclip:
    st.header("🎬 AutoClip AI — Générateur de scripts vidéo")
    
    col1, col2 = st.columns(2)
    
    with col1:
        topic = st.text_input("Sujet de la vidéo :", placeholder="ex: 3 conseils pour réussir en e-commerce")
        platform = st.selectbox("Plateforme :", ["TikTok / Shorts / Reels", "YouTube Long Format", "LinkedIn Video"])
        duration = st.selectbox("Durée souhaitée :", ["Très court (< 30 sec)", "Format classique (30 - 60 sec)", "Format long (> 1 min)"])

    with col2:
        tone = st.selectbox("Ton de la vidéo :", ["Dynamique & Captivant", "Professionnel & Expert", "Humoristique & Décalé", "Inspirant & Émotionnel"])
        hook_style = st.selectbox("Style d'accroche (Hook) :", ["Question choc", "Statistique / Fait surprenant", "Histoire / Storytelling", "Erreur courante à éviter"])
        target_audience = st.text_input("Cible / Audience (Optionnel) :", placeholder="ex: Débutants, Étudiants, Entrepreneurs...")

    if st.button("Générer le script complet (-1 crédit)", type="primary", use_container_width=True):
        if st.session_state.credits <= 0:
            st.error("❌ Crédits insuffisants. Veuillez recharger votre compte dans la barre latérale.")
        else:
            # Construction d'un prompt ultra-précis grâce aux nouveaux champs
            prompt = f"""
            Rédige un script complet et engageant pour une vidéo.
            - Sujet : {topic}
            - Plateforme : {platform}
            - Durée : {duration}
            - Ton : {tone}
            - Style d'accroche (Hook) : {hook_style}
            - Cible : {target_audience if target_audience else 'Grand public'}

            Structure le script avec :
            1. HOOK (Accroche visuelle et verbale - 3 premières secondes)
            2. CORPS DU SCRIPT (Détaillé étape par étape)
            3. CALL TO ACTION (CTA pour l'engagement)
            4. INDICATIONS VISUELLES / B-ROLL (Entre crochets [ ])
            """
            
            with st.spinner("Génération du script sur-mesure en cours..."):
                response = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}]
                )
                script = response.choices[0].message.content
                
                # Décrémenter le crédit
                new_credits = st.session_state.credits - 1
                supabase.table("profiles").update({"credits": new_credits}).eq("id", st.session_state.user.id).execute()
                st.session_state.credits = new_credits

                st.success("Script généré avec succès !")
                st.markdown(script)

# --- MODULE 2: BioCraft AI (Version enrichie) ---
with tab_biocraft:
    st.header("👤 BioCraft AI — Optimisation de profil")
    
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        bio_topic = st.text_input("Quelle est votre activité ou niche ?", placeholder="ex: Producteur de House Music & Créateur TikTok")
        platform_bio = st.selectbox("Plateforme cible :", ["Instagram", "TikTok", "LinkedIn", "Twitter / X", "YouTube Bio"])
    with col_b2:
        bio_tone = st.selectbox("Style de bio :", ["Minimaliste & Propre", "Accrocheur & Énergique", "Humoristique & Décalé", "Mystérieux & Intriguant"])
        include_cta = st.selectbox("Appel à l'action (CTA) :", ["Lien vers écoute/musique", "Lien site web / e-commerce", "S'abonner / Follow", "Aucun"])

    if st.button("Générer les bios (-1 crédit)", type="primary", use_container_width=True):
        if st.session_state.credits <= 0:
            st.error("❌ Crédits insuffisants. Veuillez recharger votre compte dans la barre latérale.")
        else:
            prompt = f"""
            Génère 3 propositions de bios différentes optimisées pour {platform_bio}.
            - Activité / Niche : '{bio_topic}'
            - Style : {bio_tone}
            - CTA souhaité : {include_cta}
            
            Formatte chaque proposition clairement avec des émojis adaptés et respecte la limite de caractères de la plateforme.
            """
            with st.spinner("Optimisation des bios en cours..."):
                response = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}]
                )
                bios = response.choices[0].message.content

                new_credits = st.session_state.credits - 1
                supabase.table("profiles").update({"credits": new_credits}).eq("id", st.session_state.user.id).execute()
                st.session_state.credits = new_credits

                st.success("Bios générées avec succès !")
                st.markdown(bios)

# --- MODULE 3: CopyCraft AI (Version enrichie) ---
with tab_copycraft:
    st.header("✍️ CopyCraft AI — Rédaction commerciale")
    
    copy_topic = st.text_area("Décrivez votre produit ou service :", placeholder="ex: Une montre Citizen Promaster Dive Eco-Drive 200m")
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        copy_format = st.selectbox("Format de rédaction :", ["Fiche produit e-commerce", "Post publicitaire réseaux sociaux", "Email de vente / Newsletter", "Page de vente (Landing Page)"])
        copy_objective = st.selectbox("Objectif marketing :", ["Générer des clics / Trafic", "Pousser à l'achat immédiat", "Mettre en avant les caractéristiques techniques", "Créer de l'émotion / Coup de cœur"])
    with col_c2:
        copy_tone = st.selectbox("Ton publicitaire :", ["Vendeur & Persuasif (Hard sell)", "Élégant & Premium", "Urgent & Dynamique", "Éducatif & Rassurant"])
        target_client = st.text_input("Client idéal (Persona) :", placeholder="ex: Passionnés de montres, plongeurs, aventuriers...")

    if st.button("Rédiger le contenu (-1 crédit)", type="primary", use_container_width=True):
        if st.session_state.credits <= 0:
            st.error("❌ Crédits insuffisants. Veuillez recharger votre compte dans la barre latérale.")
        else:
            prompt = f"""
            Rédige un texte marketing de haute qualité.
            - Produit / Service : '{copy_topic}'
            - Format : {copy_format}
            - Objectif : {copy_objective}
            - Ton : {copy_tone}
            - Client cible : {target_client if target_client else 'Grand public'}
            
            Structure ton texte avec un titre fort, des points clés percutants et un appel à l'action irrésistible.
            """
            with st.spinner("Rédaction commerciale en cours..."):
                response = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}]
                )
                copy_text = response.choices[0].message.content

                new_credits = st.session_state.credits - 1
                supabase.table("profiles").update({"credits": new_credits}).eq("id", st.session_state.user.id).execute()
                st.session_state.credits = new_credits

                st.success("Contenu rédigé avec succès !")
                st.markdown(copy_text)
