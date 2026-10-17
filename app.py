import streamlit as st
import stripe
from supabase import create_client, Client
from groq import Groq
import streamlit.components.v1 as components

# ---------------------------------------------------------
# CONFIGURATION ADMINISTRATEUR
# ---------------------------------------------------------
ADMIN_EMAIL = "elliotcarretto29@gmail.com"  # ⚠️ Remplace par ton email de connexion Supabase

# ---------------------------------------------------------
# 1. CONFIGURATION ET DESIGN CSS PREMIUM
# ---------------------------------------------------------
st.set_page_config(
    page_title="AutoClip AI — Studio de Scripting & Production Vidéo",
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
        if st.session_state.user and st.session_state.user.email == ADMIN_EMAIL:
            st.session_state.credits = 999999
            return

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
    st.markdown("<p style='text-align: center; color: #888;'>Le Générateur Universel de Scripts Vidéo & Master-Prompts IA</p>", unsafe_allow_html=True)
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
            # Vérification par LocalStorage (1 seul compte par navigateur/appareil)
            components.html("""
                <script>
                    if (localStorage.getItem('device_registered')) {
                        window.parent.postMessage({type: 'STREAMLIT_DEVICE_BLOCKED'}, '*');
                    }
                </script>
            """, height=0)

            if st.session_state.get("device_blocked", False):
                st.error("⚠️ Un compte a déjà été créé depuis cet appareil/navigateur. Veuillez vous connecter.")
            else:
                new_email = st.text_input("Email", key="signup_email")
                new_password = st.text_input("Mot de passe", type="password", key="signup_pass")
                if st.button("Créer mon compte", use_container_width=True):
                    try:
                        res = supabase.auth.sign_up({"email": new_email, "password": new_password})
                        st.success("Compte créé ! Vous pouvez vous connecter.")
                        
                        # Marquer l'appareil comme enregistré dans le navigateur
                        components.html("""
                            <script>
                                localStorage.setItem('device_registered', 'true');
                            </script>
                        """, height=0)
                    except Exception as e:
                        st.error(f"Erreur d'inscription : {e}")
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
    
    if st.session_state.user.email == ADMIN_EMAIL:
        st.metric(label="Solde de Crédits", value="∞ (Admin)")
    else:
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
# 7. MODULE UNIVERSEL : CONFIGURATION DE PRODUCTION
# ---------------------------------------------------------
st.title("🎬 AutoClip AI — Studio de Directing & Scripting Universel")
st.markdown("Configurez vos critères pour générer un plan de production complet ET le script Auto-Prompt prêt à donner à une IA créatrice de vidéo.")

st.divider()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.subheader("1. Concept & Format")
    topic = st.text_input("🎯 Sujet exact de la vidéo :", placeholder="Entrez le sujet de votre vidéo...")
    creator_type = st.radio("👤 Format de production :", ["Générée par IA (Automation / Faceless)", "Personne Réelle (Face Cam / Tournage réel)"])
    platform = st.selectbox("📱 Plateforme cible :", ["TikTok", "Instagram Reels", "YouTube Shorts", "YouTube Format Long", "LinkedIn Video", "Publicité vidéo (Meta/TikTok)"])
    duration = st.selectbox("⏱️ Durée visée :", ["Flash (15 - 30 sec)", "Standard Short (30 - 60 sec)", "Long Short (60 - 90 sec)", "Format Long (3 - 5 min)"])

with col2:
    st.subheader("2. Cible & Psychologie")
    target_persona = st.text_input("👥 Audience Cible (Exemple) :", placeholder="ex: Entrepreneurs, Étudiants, Sportifs, Clients e-commerce...")
    audience_frustration = st.text_input("💢 Frustration / Problème (Exemple) :", placeholder="ex: Manque de temps, manque de budget, manque d'organisation...")
    tone = st.selectbox("🎭 Ambiance & Énergie :", ["Dynamique & Énergique", "Cash, Provocateur & Sans Filtre", "Éducatif, Clair & Expert", "Luxe, Sombre & Futuriste", "Storytelling Émotionnel"])

with col3:
    st.subheader("3. Rétention & Structure")
    hook_style = st.selectbox("🪝 Type d'accroche (Hook 0-3s) :", ["Question choc / Provocation", "Statistique / Chiffre dingue", "Mise en garde / Erreur grave", "Scénario 'Imagine si...'", "Mythe populaire à briser"])
    pacing = st.selectbox("⚡ Rythme de montage :", ["Ultra-rapide (Cuts < 1.2s + SFX)", "Modéré & Captivant (Rythme parlé fluide)", "Analytique & Posé"])
    structure = st.selectbox("🏗️ Framework narratif :", ["PAS (Problème -> Agitation -> Solution)", "3 Piliers / Astuces pas-à-pas", "Avant / Après (Transformation)", "Récit / Storytelling dramatique"])

with col4:
    st.subheader("4. Conversion & Style")
    cta_type = st.selectbox("🎯 Call To Action (CTA) :", ["Commenter un mot-clé (Automation)", "S'abonner pour la partie 2", "Cliquer sur le lien en bio", "Enregistrer & Partager"])
    music_genre = st.text_input("🎵 Ambiance Sonore (Exemple) :", placeholder="ex: Musique dynamique motivante, Ambiance cinématique, Aucune musique...")
    extra_details = st.text_area("⚙️ Éléments Imposés (Exemple) :", placeholder="ex: Mentionner un tarif promotionnel, insérer un graphique explicatif, décor moderne...")

st.divider()

if st.button("🚀 Générer le Plan de Production & Script d'Élite (-1 crédit)", type="primary", use_container_width=True):
    if st.session_state.credits <= 0 and st.session_state.user.email != ADMIN_EMAIL:
        st.error("❌ Crédits insuffisants. Veuillez recharger votre solde dans la barre latérale.")
    else:
        is_ia_mode = (creator_type == "Générée par IA (Automation / Faceless)")
        
        prompt = f"""
        Tu es le Meilleur Directeur Artistique, Réalisateur Vidéo et Master Copywriter au Monde.
        Rédige un SCRIPT BIBLE EXHAUSTIF, HYPER LONG, DÉTAILLÉ SÉQUENCE PAR SÉQUENCE, AU MOT PRÈS.

        NE SOIS PAS SYNTHÉTIQUE. DÉTAILLE TOUT. Rédige chaque réplique intégrale sans résumé ni '...'.
        NE CITE AUCUN NOM D'APPLICATION NI DE LOGICIEL TIERS.
        ADAPTE-TOI STRICTEMENT À LA NICHE ET AU SUJET FOURNI PAR L'UTILISATEUR.

        --- CONFIGURATION DE PRODUCTION ---
        - Sujet : {topic}
        - Mode de production : {creator_type}
        - Plateforme : {platform}
        - Durée : {duration}
        - Persona / Audience Cible : {target_persona if target_persona else 'Grand public'}
        - Frustration majeure : {audience_frustration if audience_frustration else 'Non spécifiée'}
        - Ton & Ambiance : {tone}
        - Hook (0-3s) : {hook_style}
        - Rythme de montage : {pacing}
        - Framework narratif : {structure}
        - CTA : {cta_type}
        - Style sonore/musical : {music_genre if music_genre else 'Inconnu'}
        - Exigences : {extra_details if extra_details else 'Aucune'}

        --- FORMAT DE RÉPONSE EXIGÉ (Markdown d'Élite) ---

        # 🎬 BIBLE DE PRODUCTION & SCRIPT ULTRA-DÉTAILLÉ

        ### 📋 1. DIRECTION ARTISTIQUE & SETUP DÉTAILLÉ
        - **Format & Ratio** : 9:16 Vertical
        - **Palette de couleurs & Ambiance lumineuse** : [Détails ultra-précis des teintes, ombres et réflecteurs]
        - **Sound Design & Ambiance audio** : [Style sonore, moments de coupure audio, rythme]
        - **Règles Typographiques (Sous-titres)** : [Police, taille, couleur active/inactive, effets de pop-up]
        - **Stratégie de Rétention algorithmique** : [Découpage des micro-hooks à 3s, 10s et 25s]

        ---

        ### 🪝 2. L'ACCROCHE ULTIME (HOOK - 00:00 à 00:03)
        * **Timecode** : `00:00 - 00:03`
        * **Voix-off / Dialogues exacts (Word-for-word)** : "..."
        * **Intonation & Tonalité** : [Ex: Ton provocateur, hausse de voix à la fin]
        * **Visuel Direction / {"Prompt Visuel Brut en Anglais (8K, Cinematic)" if is_ia_mode else "Mouvement de caméra & Jeu du présentateur"}** : {"`...`" if is_ia_mode else "[Explication exacte du geste et du plan de caméra]"}
        * **Incrustation Texte à l'écran** : "..." [Couleur, effet d'apparition]
        * **Sound Effect (SFX)** : [Bruitage précis]

        ---

        ### 🎬 3. DÉCOUPAGE EXHAUSTIF SÉQUENCE PAR SÉQUENCE (MINUTÉ & MOT À MOT)

        Fournis 5 à 7 séquences hyper détaillées adaptées au sujet. Chaque dialogue doit être rédigé au mot près.

        #### 🔹 SÉQUENCE 1 : Agitation de la Frustration (`00:03 - 00:12`)
        * **Timecode** : `00:03 - 00:12`
        * **Dialogues / Voix-off intégrale** : "..."
        * **Intonation & Pauses** : [Consignes vocales]
        * **Visual Direction / {"Prompt Visuel Brut (Anglais)" if is_ia_mode else "Plan B-Roll & Cadrage"}** : {"`...`" if is_ia_mode else "[Description du B-Roll exact à insérer]"}
        * **Incrustation Texte / Graphisme** : [Texte affiché]
        * **SFX & Ambiance** : [Bruitage / Effet sonore]

        #### 🔹 SÉQUENCE 2 : Déconstruction de l'Erreur Courante (`00:12 - 00:25`)
        * **Timecode** : `00:12 - 00:25`
        * **Dialogues / Voix-off intégrale** : "..."
        * **Intonation & Pauses** : [Consignes vocales]
        * **Visual Direction / {"Prompt Visuel Brut (Anglais)" if is_ia_mode else "Plan B-Roll & Cadrage"}** : {"`...`" if is_ia_mode else "[Description du plan]"}
        * **Incrustation Texte / Graphisme** : [Graphique / Animation]
        * **SFX** : [Bruitage]

        #### 🔹 SÉQUENCE 3 : La Révélation de la Solution (`00:25 - 00:40`)
        * **Timecode** : `00:25 - 00:40`
        * **Dialogues / Voix-off intégrale** : "..."
        * **Visual Direction / {"Prompt Visuel Brut (Anglais)" if is_ia_mode else "Plan B-Roll & Cadrage"}** : {"`...`" if is_ia_mode else "[Description du plan]"}
        * **Incrustation Texte / Graphisme** : [Puces explicatives]
        * **SFX** : [Bruitage]

        #### 🔹 SÉQUENCE 4 : Application Pratique Pas-à-Pas (`00:40 - 00:55`)
        * **Timecode** : `00:40 - 00:55`
        * **Dialogues / Voix-off intégrale** : "..."
        * **Visual Direction / {"Prompt Visuel Brut (Anglais)" if is_ia_mode else "Plan B-Roll & Cadrage"}** : {"`...`" if is_ia_mode else "[Démonstration]"}
        * **Incrustation Texte / Graphisme** : [Étapes 1, 2, 3]

        #### 🔹 SÉQUENCE 5 : Preuve de Résultat & Impact (`01:10 - Fin`)
        * **Timecode** : `01:10 - Fin`
        * **Dialogues / Voix-off intégrale** : "..."
        * **Visual Direction / {"Prompt Visuel Brut (Anglais)" if is_ia_mode else "Plan B-Roll & Cadrage"}** : {"`...`" if is_ia_mode else "[Résultat final]"}

        ---

        ### 🎯 4. CONCLUSION & CALL TO ACTION (CONVERSION)
        * **Timecode** : `Fin de vidéo`
        * **Dialogues / Voix-off intégrale** : "..."
        * **Action Visuelle & Incrustation** : [Flèche vers le profil, bouton follow, mot-clé à commenter]
        * **Outro Audio** : [Fondu de musique]

        ---

        ### 🤖 5. SCRIPT AUTO-PROMPT CLÉ EN MAIN (À COPIER-COLLER POUR L'IA GÉNÉRATRICE DE VIDÉO)
        C'EST UNE SECTION OBLIGATOIRE. Rédige tout en bas un bloc de code unique (```) en Anglais technique, ultra-clair et structuré, prêt à être directement copié-collé dans n'importe quelle IA génératrice de vidéo.
        Inclus obligatoirement :
        1. **Global Topic, Mood & Style Directive** (Cinematic, 8K, 9:16 Aspect Ratio, Lighting).
        2. **Full Voiceover Script** (Mot à mot en français ou anglais selon la cible, sans résumé).
        3. **Scene-by-Scene Visual Generation Prompts** (Horodatés de 0s à la fin).
        4. **Audio & On-Screen Text Overlay Directives**.
        """

        with st.spinner("🎬 Production du script ultra-détaillé et du Master-Prompt IA..."):
            try:
                response = groq_client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[{"role": "user", "content": prompt}]
                )
                script = response.choices[0].message.content

                # Décrémenter les crédits uniquement si ce n'est pas l'administrateur
                if st.session_state.user.email != ADMIN_EMAIL:
                    new_credits = st.session_state.credits - 1
                    supabase.table("profiles").update({"credits": new_credits}).eq("id", st.session_state.user.id).execute()
                    st.session_state.credits = new_credits

                st.success("✨ Bible de production & Master-Prompt IA générés avec succès !")
                st.markdown(script)

            except Exception as e:
                st.error(f"Erreur lors de la génération : {e}")
