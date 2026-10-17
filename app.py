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
import streamlit.components.v1 as components

def recharger_via_stripe(price_id, user_email):
    """ Crée la session Stripe Checkout et redirige directement l'utilisateur """
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
            managed_payments={'enabled': False},
        )
        
        # Redirection automatique via JavaScript vers la page Checkout Stripe
        js = f"""
        <script>
            window.top.location.href = "{session.url}";
        </script>
        """
        components.html(js, height=0)
        
        # Message de secours avec bouton direct si la redirection automatique est bloquée
        st.info("Redirection vers la page de paiement Stripe...")
        st.markdown(f"[👉 Cliquez ici si la page ne s'ouvre pas automatiquement]({session.url})")
        
    except Exception as e:
        st.error(f"Erreur Stripe : {e}")
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
# 6. MODULES IA DU STUDIO (VERSION AVANCÉE & PROFONDE)
# ---------------------------------------------------------
st.title("🚀 Espace de Création Avancé")

tab_autoclip, tab_biocraft, tab_copycraft = st.tabs(["🎬 AutoClip AI", "👤 BioCraft AI", "✍️ CopyCraft AI"])

# --- MODULE 1: AutoClip AI (Générateur de scripts ultra-détaillé) ---
with tab_autoclip:
    st.header("🎬 AutoClip AI — Générateur de scripts vidéo sur-mesure")
    
    col1, col2 = st.columns(2)
    
    with col1:
        topic = st.text_input("Sujet principal de la vidéo :", placeholder="ex: 3 erreurs à éviter quand on lance son business")
        platform = st.selectbox("Plateforme cible :", ["TikTok / Reels / Shorts (< 1 min)", "YouTube Long Format", "LinkedIn Vidéo pro", "Publicité vidéo (Meta/TikTok)"])
        duration = st.selectbox("Format / Durée :", ["Flash (< 30 sec - Rythme ultra-rapide)", "Standard (30 à 60 sec)", "Approfondi (1 à 3 minutes)"])
        tone = st.selectbox("Ton de la voix / Ambiance :", ["Dynamique & Énergique", "Cash, Direct & Provocant", "Éducatif & Expert", "Storytelling & Émotionnel", "Humoristique & Décalé"])

    with col2:
        hook_style = st.selectbox("Style d'accroche (Hook des 3 premières secondes) :", ["Question choc / Provocation", "Statistique ou Fait insolite", "Scénario 'Imagine si...'", "Briser une idée reçue / Mythe"])
        structure = st.selectbox("Structure narrative :", ["Méthode des 3 étapes clés", "Problème / Agitation / Solution", "Avant / Après (Transformation)", "Liste numérotée rythmée"])
        target_audience = st.text_input("Audience cible (Persona précis) :", placeholder="ex: Étudiants, entrepreneurs débutants, passionnés de musique...")
        cta_type = st.selectbox("Appel à l'action (CTA) final :", ["S'abonner / S'abonner pour la suite", "Commenter pour recevoir un guide/lien", "Cliquer sur le lien en bio", "Partager à un ami"])

    keywords = st.text_input("Mots-clés ou expressions obligatoires (optionnel) :", placeholder="ex: indépendance, house music, stratégie")

    if st.button("Générer le script professionnel (-1 crédit)", type="primary", use_container_width=True):
        if st.session_state.credits <= 0:
            st.error("❌ Crédits insuffisants. Veuillez recharger votre compte dans la barre latérale.")
        else:
            prompt = f"""
            Agis en tant que Directeur Artistique et Expert en Copywriting vidéo. Rédige un script ultra-performant et engageant.
            - Sujet : '{topic}'
            - Plateforme : {platform}
            - Durée : {duration}
            - Ton : {tone}
            - Style d'accroche : {hook_style}
            - Structure narrative : {structure}
            - Audience cible : {target_audience if target_audience else 'Grand public'}
            - Appel à l'action (CTA) : {cta_type}
            - Mots-clés à intégrer : {keywords if keywords else 'Aucun'}

            Structure ton output clairement avec :
            1. **LE HOOK (0-3s)** : Accroche verbale percutante + indication visuelle [B-ROLL / Texte à l'écran].
            2. **LE DÉVELOPPEMENT** : Corps du script structuré selon la méthode choisie, avec un rythme soutenu.
            3. **LE CALL TO ACTION (CTA)** : Transition fluide vers l'action attendue.
            4. **CONSEILS DE MONTAGE** : Idées d'effets visuels, de transitions ou de musique de fond.
            """
            with st.spinner("Génération du script approfondi en cours..."):
                response = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}]
                )
                script = response.choices[0].message.content
                
                new_credits = st.session_state.credits - 1
                supabase.table("profiles").update({"credits": new_credits}).eq("id", st.session_state.user.id).execute()
                st.session_state.credits = new_credits

                st.success("Script généré avec succès !")
                st.markdown(script)

# --- MODULE 2: BioCraft AI (Optimisation de profil experte) ---
with tab_biocraft:
    st.header("👤 BioCraft AI — Optimisation de profil multi-plateforme")
    
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        bio_topic = st.text_input("Activité / Niche / Domaine :", placeholder="ex: Producteur de House Music & Créateur de contenus")
        platform_bio = st.selectbox("Plateforme cible :", ["Instagram", "TikTok", "LinkedIn", "X (Twitter)", "YouTube Channel Bio"])
        bio_vibe = st.selectbox("Vibe / Identité visuelle :", ["Minimaliste & Propre", "Énergique & Impactant", "Corporate & Autorité", "Artistique & Créatif", "Mystérieux & Exclusif"])
    with col_b2:
        include_stats = st.text_input("Chiffres clés ou accomplissements (optionnel) :", placeholder="ex: +1M vues, 5 ans d'expérience...")
        cta_bio = st.selectbox("Objectif du lien en bio :", ["Écouter mon titre / ma musique", "Visiter le site web / E-commerce", "Réserver un appel / Consultation", "S'abonner à la newsletter"])
        emoji_style = st.selectbox("Utilisation des émojis :", ["Subtile et élégante (1 ou 2 max)", "Dynamique et moderne", "Aucun emoji (Pur texte brut)"])

    if st.button("Générer les options de bio sur-mesure (-1 crédit)", type="primary", use_container_width=True):
        if st.session_state.credits <= 0:
            st.error("❌ Crédits insuffisants. Veuillez recharger votre compte dans la barre latérale.")
        else:
            prompt = f"""
            Agis en tant qu'expert en Personal Branding. Fournis 3 propositions de bios différentes, percutantes et optimisées pour {platform_bio}.
            - Activité : '{bio_topic}'
            - Vibe : {bio_vibe}
            - Accomplissements / Chiffres : {include_stats if include_stats else 'Aucun'}
            - Objectif du CTA : {cta_bio}
            - Style d'émojis : {emoji_style}
            
            Respecte scrupuleusement les contraintes de caractères de la plateforme. Propose des structures aérées avec retours à la ligne.
            """
            with st.spinner("Création des bios en cours..."):
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

# --- MODULE 3: CopyCraft AI (Rédaction commerciale & Marketing avancé) ---
with tab_copycraft:
    st.header("✍️ CopyCraft AI — Studio de Copywriting Professionnel")
    
    copy_topic = st.text_area("Décrivez votre produit, service ou projet en détail :", placeholder="ex: Une montre de plongée Citizen Promaster Dive Eco-Drive, robuste, étanche 200m, design intemporel.")
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        copy_format = st.selectbox("Format de contenu marketing :", ["Fiche produit e-commerce optimisée SEO", "Post publicitaire réseaux sociaux (Conversion)", "Séquence d'Emails de vente / Newsletter", "Page de vente complète (Landing Page)", "Script publicitaire UGC"])
        copy_objective = st.selectbox("Objectif psychologique principal :", ["Générer un achat immédiat (Conversion directe)", "Créer l'urgence / Rareté", "Rassurer et lever les objections techniques", "Créer un coup de cœur émotionnel"])
        copywriting_framework = st.selectbox("Cadre de copywriting (Framework) :", ["AIDA (Attention, Intérêt, Désir, Action)", "PAS (Problème, Agitation, Solution)", "FAB (Features, Advantages, Benefits)"])

    with col_c2:
        copy_tone = st.selectbox("Ton rédactionnel :", ["Vendeur percutant (Hard Sell)", "Élégant, Luxe & Premium", "Proche de la communauté (Authentique)", "Éducatif & Autoritaire"])
        target_persona = st.text_input("Client idéal (Persona & Frustrations) :", placeholder="ex: Passionnés d'horlogerie cherchant une montre fiable sans se ruiner")
        urgency_element = st.text_input("Offre spéciale ou urgence (optionnel) :", placeholder="ex: -20% ce weekend, Stock limité à 50 pièces...")

    if st.button("Lancer la rédaction stratégique (-1 crédit)", type="primary", use_container_width=True):
        if st.session_state.credits <= 0:
            st.error("❌ Crédits insuffisants. Veuillez recharger votre compte dans la barre latérale.")
        else:
            prompt = f"""
            Agis en tant que Copywriter Senior spécialisé en e-commerce et conversion. Rédige un texte marketing hautement persuasif.
            - Produit / Service : '{copy_topic}'
            - Format : {copy_format}
            - Objectif : {copy_objective}
            - Framework psychologique : {copywriting_framework}
            - Ton : {copy_tone}
            - Client cible : {target_persona if target_persona else 'Grand public'}
            - Élément d'urgence / Offre : {urgency_element if urgency_element else 'Aucun'}

            Structure ton texte avec un titre irrésistible, des puces bien ciselées, une mise en valeur des bénéfices clients et un appel à l'action percutant.
            """
            with st.spinner("Rédaction commerciale experte en cours..."):
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
