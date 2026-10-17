import streamlit as st
import stripe
from supabase import create_client, Client
from groq import Groq
import streamlit.components.v1 as components

# ---------------------------------------------------------
# 1. CONFIGURATION ET DESIGN CSS PREMIUM
# ---------------------------------------------------------
st.set_page_config(
    page_title="AutoClip AI — Studio de Scripting & Automation Vidéo Pro",
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
    st.markdown("<p style='text-align: center; color: #888;'>Le Générateur de Scripts Vidéo le Plus Avancé du Marché</p>", unsafe_allow_html=True)
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
# 7. MODULE EXPERT : CONFIGURATION COMPLÈTE DE PRODUCTION
# ---------------------------------------------------------
st.title("🎬 AutoClip AI — Studio de Directing & Scripting High-End")
st.markdown("Configurez la totalité des paramètres de votre vidéo pour recevoir un script de niveau cinéma / agence publicitaire.")

st.divider()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.subheader("1. Concept & Format")
    topic = st.text_input("🎯 Sujet exact :", placeholder="ex: 3 secrets pour mixer une House Music percutante")
    creator_type = st.radio("👤 Format de production :", ["Générée par IA (Automation / Faceless)", "Personne Réelle (Face Cam / Tournage réel)"])
    platform = st.selectbox("📱 Plateforme cible :", ["TikTok", "Instagram Reels", "YouTube Shorts", "YouTube Format Long", "LinkedIn Video", "Publicité vidéo (Meta/TikTok)"])
    duration = st.selectbox("⏱️ Durée visée :", ["Flash (15 - 30 sec)", "Standard Short (30 - 60 sec)", "Long Short (60 - 90 sec)", "Format Long (3 - 5 min)"])

with col2:
    st.subheader("2. Cible & Psychologie")
    target_persona = st.text_input("👥 Client / Audience Cible :", placeholder="ex: Producteurs débutants, DJ, passionnés de House")
    audience_frustration = st.text_input("💢 Frustration / Problème majeur :", placeholder="ex: Un son plat sans relief, kick noyé dans la basse")
    tone = st.selectbox("🎭 Ambiance & Énergie :", ["Dynamique & Énergique", "Cash, Provocateur & Sans Filtre", "Éducatif, Clair & Expert", "Luxe, Sombre & Futuriste", "Storytelling Émotionnel"])

with col3:
    st.subheader("3. Rétention & Structure")
    hook_style = st.selectbox("🪝 Type d'accroche (Hook 0-3s) :", ["Question choc / Provocation", "Statistique / Chiffre dingue", "Mise en garde / Erreur grave", "Scénario 'Imagine si...'", "Mythe populaire à briser"])
    pacing = st.selectbox("⚡ Rythme de montage :", ["Ultra-rapide (Cuts < 1.2s + SFX)", "Modéré & Captivant (Rythme parlé fluide)", "Analytique & Posé"])
    structure = st.selectbox("🏗️ Framework narratif :", ["PAS (Problème -> Agitation -> Solution)", "3 Piliers / Astuces pas-à-pas", "Avant / Après (Transformation)", "Récit / Storytelling dramatique"])

with col4:
    st.subheader("4. Conversion & Style")
    cta_type = st.selectbox("🎯 Call To Action (CTA) :", ["Commenter un mot-clé (Automation)", "S'abonner pour la partie 2", "Cliquer sur le lien en bio", "Enregistrer & Partager"])
    music_genre = st.text_input("🎵 Genre musical / Tempo :", placeholder="ex: House 128 BPM, Synthwave sombre, No Music")
    extra_details = st.text_area("⚙️ Mots-clés / Éléments imposés :", placeholder="ex: Parler de sidechain, EQ, néon rouge, ambiance club...")

st.divider()

if st.button("🚀 Générer le Plan de Production & Script d'Élite (-1 crédit)", type="primary", use_container_width=True):
    if st.session_state.credits <= 0:
        st.error("❌ Crédits insuffisants. Veuillez recharger votre solde dans la barre latérale.")
    else:
        is_ia_mode = (creator_type == "Générée par IA (Automation / Faceless)")
        
        prompt = f"""
        Tu es le Meilleur Directeur Artistique, Réalisateur Vidéo et Master Copywriter au Monde.
        Rédige un SCRIPT ULTRA-DÉTAILLÉ, LONG, HYPER PRÉCIS ET PROFESSIONNEL pour une vidéo à haut taux de rétention.

        NE CITE AUCUN NOM D'APPLICATION NI DE LOGICIEL TIERS.

        --- FICHE DE TOURNAGE / PRODUCTION ---
        - Sujet : {topic}
        - Mode de production : {creator_type}
        - Plateforme : {platform}
        - Durée : {duration}
        - Persona / Cible : {target_persona if target_persona else 'Grand public'}
        - Frustration majeure traitée : {audience_frustration if audience_frustration else 'Non spécifiée'}
        - Ton & Ambiance : {tone}
        - Style de Hook (0-3s) : {hook_style}
        - Rythme de montage : {pacing}
        - Framework narratif : {structure}
        - Call To Action (CTA) : {cta_type}
        - Style musical : {music_genre if music_genre else 'À adapter selon l ambiance'}
        - Exigences spécifiques : {extra_details if extra_details else 'Aucune'}

        --- FORMAT DE RÉPONSE EXIGÉ (Markdown d'Élite) ---

        # 🎬 PLAN DE PRODUCTION HAUTE PERFORMANCE

        ### 📋 1. DIRECTION ARTISTIQUE & FICHE TECHNIQUE
        - **Format & Cadre** : 9:16 Vertical
        - **Éclairage & Palette de couleurs** : [Direction précise des néons, ombres, contrastes]
        - **Ambiance sonore & Musique** : {music_genre if music_genre else 'BPM adapté, sons percutants'}
        - **Style de sous-titres** : [Style dynamique, surlignage mot par mot, couleurs clés]
        - **Stratégie de Rétention** : [Méthode appliquée pour garder l'attention de 0 à la fin]

        ---

        ### 🪝 2. L'ACCROCHE CHOC (HOOK - 0 à 3 SECONDES)
        * **Timecode** : `00:00 - 00:03`
        * **Texte / Dialogue exact (Word-for-word)** : "..."
        * **Visual Direction / {"Prompt Visuel Brut (Anglais)" if is_ia_mode else "Jeu du présentateur"}** : {"`...`" if is_ia_mode else "[Action exacte, mouvement rapide devant la caméra]"}
        * **Incrustation Texte (On-Screen Text)** : "..."
        * **Effet Sonore (SFX)** : [Boom / Whoosh / Glitch]

        ---

        ### 🎬 3. DÉCOUPAGE DÉTAILLÉ SÉQUENCE PAR SÉQUENCE (Minuté)

        Découpe la vidéo en 4 à 6 séquences chronologiques détaillées :

        #### 🔹 SÉQUENCE 1 : Agitation du Problème & Empirisme (`00:03 - 00:15`)
        * **Voix-off / Dialogues exacts** : "..."
        * **Visual Direction / {"Prompt Visuel (Anglais)" if is_ia_mode else "Plan de coupe B-Roll"}** : {"`...`" if is_ia_mode else "[Préciser le plan B-Roll]"}
        * **Texte & Graphisme à l'écran** : [Mots-clés en gros / Surlignage]
        * **SFX & Transitions** : [Swoosh / Bip]

        #### 🔹 SÉQUENCE 2 : La Révélation / Déconstruction du Mythe (`00:15 - 00:30`)
        * **Voix-off / Dialogues exacts** : "..."
        * **Visual Direction / {"Prompt Visuel (Anglais)" if is_ia_mode else "Plan de coupe B-Roll"}** : {"`...`" if is_ia_mode else "[Démonstration à l écran / Geste]"}
        * **Texte & Graphisme à l'écran** : [Puces clés / Graphique]

        #### 🔹 SÉQUENCE 3 : L'Astuce Maîtresse & Application Pratique (`00:30 - 00:50`)
        * **Voix-off / Dialogues exacts** : "..."
        * **Visual Direction / {"Prompt Visuel (Anglais)" if is_ia_mode else "Plan de coupe B-Roll"}** : {"`...`" if is_ia_mode else "[Zoom sur l action ou l outil]"}
        * **Texte & Graphisme à l'écran** : [Étape 1, 2, 3]

        #### 🔹 SÉQUENCE 4 : Preuve & Transformation (`00:50 - 01:10`)
        * **Voix-off / Dialogues exacts** : "..."
        * **Visual Direction / {"Prompt Visuel (Anglais)" if is_ia_mode else "Plan de coupe B-Roll"}** : {"`...`" if is_ia_mode else "[Résultat final probant]"}

        ---

        ### 🎯 4. CONCLUSION & CONVERSION (CTA)
        * **Timecode** : `Fin de vidéo`
        * **Réplique exacte** : "..."
        * **Visual Direction** : [Animation de bouton / Pointage du doigt]
        * **Incrustation Graphique** : [Mot-clé à commenter ou appel à s abonner]

        ---

        ### 💡 5. SECRETS DU RÉALISATEUR POUR BOOSTER L'ALGORITHME
        - **Astuce de rétention** : [Expliciter le hook visuel secondaire à 10s]
        - **Sound Design** : [Astuce de mixage audio]
        """

        with st.spinner("🎬 Production du plan de tournage et script d'élite..."):
            try:
                response = groq_client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[{"role": "user", "content": prompt}]
                )
                script = response.choices[0].message.content

                new_credits = st.session_state.credits - 1
                supabase.table("profiles").update({"credits": new_credits}).eq("id", st.session_state.user.id).execute()
                st.session_state.credits = new_credits

                st.success("✨ Plan de production & Script d'Élite générés avec succès !")
                st.markdown(script)

            except Exception as e:
                st.error(f"Erreur lors de la génération : {e}")
