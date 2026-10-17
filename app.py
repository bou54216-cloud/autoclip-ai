import streamlit as st
import stripe
from supabase import create_client, Client
from groq import Groq
import streamlit.components.v1 as components

# ---------------------------------------------------------
# 1. CONFIGURATION ET DESIGN CSS PREMIUM
# ---------------------------------------------------------
st.set_page_config(
    page_title="The Empire Studio — AI Content Suite",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Injection CSS pour une interface SaaS haut de gamme
st.markdown("""
<style>
    .stApp {
        background-color: #0E1117;
    }
    div[data-testid="stVerticalBlock"] > div {
        border-radius: 10px;
    }
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px;
        padding: 8px 16px;
        background-color: #1E232A;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FF4B4B !important;
        color: white !important;
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
    """ Récupère ou initialise le solde de crédits depuis Supabase """
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
# 4. FONCTION DE GÉNÉRATION GROQ AVEC SÉCOURS (FALLBACK)
# ---------------------------------------------------------
def generer_avec_groq(prompt):
    """ Tente plusieurs modèles Groq en cascade pour éviter les erreurs de disponibilité """
    modeles = ["llama-3.3-70b-versatile", "llama3-70b-8192", "llama3-8b-8192"]
    
    for model in modeles:
        try:
            response = groq_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception:
            continue
            
    raise Exception("Tous les modèles Groq ont échoué. Veuillez vérifier votre clé API.")

# ---------------------------------------------------------
# 5. FONCTION REDIRECTION STRIPE CHECKOUT
# ---------------------------------------------------------
def recharger_via_stripe(price_id, user_email):
    """ Crée la session Stripe Checkout et redirige la fenêtre principale """
    try:
        is_subscription = (price_id != st.secrets["PRICE_SINGLE"])
        
        session = stripe.checkout.Session.create(
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
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
# 6. ECRAN DE CONNEXION / INSCRIPTION
# ---------------------------------------------------------
if not st.session_state.user:
    st.markdown("<h1 style='text-align: center;'>⚡ The Empire Studio</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888;'>Studio IA Haute Performance — Monetization Ready</p>", unsafe_allow_html=True)
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
# 7. APPLICATION PRINCIPALE & BARRE LATÉRALE
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
    st.title("⚡ Empire Studio")
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
# 8. MODULES IA DE CRÉATION
# ---------------------------------------------------------
st.title("🚀 Espace de Création Avancé")

tab_autoclip, tab_biocraft, tab_copycraft = st.tabs(["🎬 AutoClip AI", "👤 BioCraft AI", "✍️ CopyCraft AI"])

# --- MODULE 1: AutoClip AI ---
with tab_autoclip:
    st.header("🎬 AutoClip AI — Générateur de scripts vidéo sur-mesure")
    
    col1, col2 = st.columns(2)
    with col1:
        topic = st.text_input("Sujet principal de la vidéo :", placeholder="ex: 3 erreurs à éviter quand on lance son business")
        platform = st.selectbox("Plateforme cible :", ["TikTok / Shorts / Reels (< 1 min)", "YouTube Long Format", "LinkedIn Vidéo pro", "Publicité vidéo (Meta/TikTok)"])
        duration = st.selectbox("Format / Durée :", ["Flash (< 30 sec)", "Standard (30 à 60 sec)", "Approfondi (1 à 3 min)"])
        tone = st.selectbox("Ton / Ambiance :", ["Dynamique & Énergique", "Cash, Direct & Provocant", "Éducatif & Expert", "Storytelling", "Humoristique"])

    with col2:
        hook_style = st.selectbox("Style d'accroche (Hook 0-3s) :", ["Question choc", "Statistique / Fait insolite", "Scénario 'Imagine si...'", "Mythe à briser"])
        structure = st.selectbox("Structure narrative :", ["3 étapes clés", "Problème / Agitation / Solution", "Avant / Après", "Liste numérotée"])
        target_audience = st.text_input("Audience cible (Persona) :", placeholder="ex: Étudiants, entrepreneurs, passionnés de musique...")
        cta_type = st.selectbox("Appel à l'action (CTA) :", ["S'abonner", "Commenter pour recevoir un lien", "Cliquer sur le lien en bio", "Partager à un ami"])

    keywords = st.text_input("Mots-clés obligatoires (optionnel) :", placeholder="ex: house music, productivité, indépendance")

    if st.button("Générer le script (-1 crédit)", type="primary", use_container_width=True):
        if st.session_state.credits <= 0:
            st.error("❌ Crédits insuffisants. Veuillez recharger votre solde dans la barre latérale.")
        else:
            prompt = f"""
            Agis en tant que Directeur Artistique et Expert Copywriter vidéo.
            Rédige un script hautement engageant.
            - Sujet: {topic}
            - Plateforme: {platform}
            - Durée: {duration}
            - Ton: {tone}
            - Hook: {hook_style}
            - Structure: {structure}
            - Audience: {target_audience if target_audience else 'Grand public'}
            - CTA: {cta_type}
            - Mots-clés: {keywords if keywords else 'Aucun'}

            Format exigé :
            1. **HOOK (0-3s)**: Verbal + Indication visuelle [B-Roll].
            2. **DÉVELOPPEMENT**: Corps du script rythmé.
            3. **CALL TO ACTION**: Transition naturelle.
            4. **CONSEILS MONTAGE**: Musique, rythme, effets.
            """
            with st.spinner("Génération du script sur-mesure..."):
                try:
                    script = generer_avec_groq(prompt)
                    
                    new_credits = st.session_state.credits - 1
                    supabase.table("profiles").update({"credits": new_credits}).eq("id", st.session_state.user.id).execute()
                    st.session_state.credits = new_credits

                    st.success("Script généré avec succès !")
                    st.markdown(script)
                except Exception as e:
                    st.error(f"Erreur lors de la génération : {e}")

# --- MODULE 2: BioCraft AI ---
with tab_biocraft:
    st.header("👤 BioCraft AI — Optimisation de profil multi-plateforme")
    
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        bio_topic = st.text_input("Activité / Domaine :", placeholder="ex: Producteur de House Music & Créateur TikTok")
        platform_bio = st.selectbox("Plateforme cible :", ["Instagram", "TikTok", "LinkedIn", "X (Twitter)", "YouTube Bio"])
        bio_vibe = st.selectbox("Vibe / Style :", ["Minimaliste & Clean", "Énergique & Impactant", "Corporate", "Artistique", "Exclusif"])
    with col_b2:
        include_stats = st.text_input("Réalisations / Stats (optionnel) :", placeholder="ex: +1M d'écoutes, 5 ans d'expérience")
        cta_bio = st.selectbox("Objectif CTA :", ["Écouter ma musique", "Visiter le site e-commerce", "Prendre RDV", "S'abonner"])
        emoji_style = st.selectbox("Émojis :", ["Subtil (1 ou 2 max)", "Dynamique", "Aucun"])

    if st.button("Générer les bios (-1 crédit)", type="primary", use_container_width=True):
        if st.session_state.credits <= 0:
            st.error("❌ Crédits insuffisants. Veuillez recharger votre solde dans la barre latérale.")
        else:
            prompt = f"""
            Génère 3 variations de bios captivantes optimisées pour {platform_bio}.
            - Domaine: {bio_topic}
            - Style: {bio_vibe}
            - Stats: {include_stats if include_stats else 'Aucune'}
            - Objectif CTA: {cta_bio}
            - Émojis: {emoji_style}
            """
            with st.spinner("Création des bios..."):
                try:
                    bios = generer_avec_groq(prompt)

                    new_credits = st.session_state.credits - 1
                    supabase.table("profiles").update({"credits": new_credits}).eq("id", st.session_state.user.id).execute()
                    st.session_state.credits = new_credits

                    st.success("Bios générées !")
                    st.markdown(bios)
                except Exception as e:
                    st.error(f"Erreur lors de la génération : {e}")

# --- MODULE 3: CopyCraft AI ---
with tab_copycraft:
    st.header("✍️ CopyCraft AI — Studio de Copywriting")
    
    copy_topic = st.text_area("Description du produit / service :", placeholder="ex: Montre Citizen Promaster Dive Eco-Drive 200m, étanche, solaire, bracelet résine...")
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        copy_format = st.selectbox("Format marketing :", ["Fiche produit e-commerce SEO", "Publicité réseaux sociaux (Conversion)", "Email de vente", "Landing Page", "Script UGC"])
        copy_objective = st.selectbox("Objectif principal :", ["Conversion directe", "Créer l'urgence", "Lever les objections", "Coup de cœur émotionnel"])
        copywriting_framework = st.selectbox("Framework :", ["AIDA (Attention, Intérêt, Désir, Action)", "PAS (Problème, Agitation, Solution)", "FAB (Features, Advantages, Benefits)"])

    with col_c2:
        copy_tone = st.selectbox("Ton :", ["Vendeur percutant", "Luxe & Premium", "Authentique & Proche", "Éducatif"])
        target_persona = st.text_input("Client idéal (Persona) :", placeholder="ex: Passionnés d'horlogerie et d'aventure")
        urgency_element = st.text_input("Offre / Urgence (optionnel) :", placeholder="ex: -20% ce weekend")

    if st.button("Lancer la rédaction (-1 crédit)", type="primary", use_container_width=True):
        if st.session_state.credits <= 0:
            st.error("❌ Crédits insuffisants. Veuillez recharger votre solde dans la barre latérale.")
        else:
            prompt = f"""
            Agis en tant que Copywriter Senior. Rédige un texte marketing hautement persuasif.
            - Produit: {copy_topic}
            - Format: {copy_format}
            - Objectif: {copy_objective}
            - Framework: {copywriting_framework}
            - Ton: {copy_tone}
            - Persona: {target_persona if target_persona else 'Grand public'}
            - Urgence: {urgency_element if urgency_element else 'Aucun'}
            """
            with st.spinner("Rédaction stratégique en cours..."):
                try:
                    copy_text = generer_avec_groq(prompt)

                    new_credits = st.session_state.credits - 1
                    supabase.table("profiles").update({"credits": new_credits}).eq("id", st.session_state.user.id).execute()
                    st.session_state.credits = new_credits

                    st.success("Texte rédigé avec succès !")
                    st.markdown(copy_text)
                except Exception as e:
                    st.error(f"Erreur lors de la rédaction : {e}")
