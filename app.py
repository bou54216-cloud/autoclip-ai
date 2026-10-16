import streamlit as st
import requests
import json

# 1. Configuration de la page
st.set_page_config(
    page_title="The Empire Studio — Imperial AI Suite",
    page_icon="👑",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Design Impérial & Animations Fluides (CSS Avancé)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Arrière-plan Spatial / Cyber Impérial */
    .stApp {
        background: radial-gradient(circle at 50% -20%, #1e1b4b 0%, #0f172a 45%, #020617 100%);
        color: #f8fafc;
    }

    /* En-tête Impérial */
    .imperial-container {
        text-align: center;
        padding: 40px 20px 20px 20px;
    }
    
    .imperial-badge {
        background: linear-gradient(90deg, rgba(234, 179, 8, 0.2), rgba(168, 85, 247, 0.2));
        border: 1px solid rgba(234, 179, 8, 0.4);
        color: #facc15;
        padding: 6px 18px;
        border-radius: 30px;
        font-size: 0.85rem;
        font-weight: 800;
        letter-spacing: 2px;
        text-transform: uppercase;
        display: inline-block;
        margin-bottom: 15px;
        box-shadow: 0 0 20px rgba(234, 179, 8, 0.2);
    }

    .imperial-title {
        font-size: 3.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 20%, #facc15 60%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
        line-height: 1.1;
    }

    .imperial-subtitle {
        font-size: 1.15rem;
        color: #94a3b8;
        max-width: 650px;
        margin: 0 auto 30px auto;
    }

    /* Champs de saisie stylisés */
    .stTextInput input, .stSelectbox div[data-baseweb="select"], .stTextArea textarea {
        background-color: rgba(15, 23, 42, 0.7) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: #f8fafc !important;
        backdrop-filter: blur(12px);
    }
    
    .stTextInput input:focus, .stSelectbox div[data-baseweb="select"]:focus-within, .stTextArea textarea:focus {
        border-color: #facc15 !important;
        box-shadow: 0 0 15px rgba(250, 204, 21, 0.3) !important;
    }

    /* Le Bouton Impérial Doré / Violet */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #d97706 0%, #eab308 50%, #9333ea 100%);
        background-size: 200% auto;
        color: white;
        font-weight: 800;
        font-size: 1.1rem;
        border-radius: 14px;
        padding: 16px 24px;
        border: none;
        box-shadow: 0 0 25px rgba(234, 179, 8, 0.3);
        cursor: pointer;
        transition: all 0.4s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .stButton>button:hover {
        background-position: right center;
        transform: translateY(-3px) scale(1.01);
        box-shadow: 0 0 35px rgba(234, 179, 8, 0.6);
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# En-tête de l'Empire
st.markdown("""
    <div class="imperial-container">
        <span class="imperial-badge">👑 The Imperial Suite — All-Access</span>
        <h1 class="imperial-title">Bienvenue dans votre Empire</h1>
        <p class="imperial-subtitle">Sélectionnez ci-dessous l'outil souverain que vous souhaitez déployer pour dominer votre marché.</p>
    </div>
""", unsafe_allow_html=True)

# Clé API Groq
GROQ_API_KEY = "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"

# --- CHOIX DE L'OUTIL (Souveraineté de l'Empereur) ---
choix_outil = st.selectbox(
    "🏛️ Choisissez votre division impériale :",
    [
        "⚡ AutoClip AI (Vidéos & Kits Viraux)", 
        "🎵 LyricPulse AI (Paroles & Concepts de Clips)", 
        "💼 BioCraft AI (Profils Pro & Bios d'Élite)"
    ]
)

st.markdown("---")

# ==========================================
# 1. AUTOCLIP AI (Vidéos & Kits Viraux)
# ==========================================
if "AutoClip" in choix_outil:
    st.markdown("### ⚡ AutoClip AI — Division Vidéo & Média")
    st.caption("Dominez les algorithmes avec des kits de production taillés sur-mesure.")
    
    sujet_clip = st.text_input("🎯 Sujet ou concept de la vidéo", placeholder="ex: 3 astuces pour composer une Bassline House incroyable")
    
    c1, c2 = st.columns(2)
    with c1:
        plateforme = st.selectbox("📱 Plateforme Cible", ["TikTok", "Instagram Reels", "YouTube Shorts"])
        style_clip = st.selectbox("🎨 Format", ["Éducatif / Conseil", "Storytelling", "Promotion Musique / Art", "Divertissement"])
    with c2:
        ton_clip = st.selectbox("🎙️ Ton Souhaité", ["Énergique & Rythmé", "Humoristique & Décalé", "Cash & Direct", "Professionnel & Inspirant"])
        duree = st.selectbox("⏱️ Durée", ["15 secondes", "30 secondes", "45 secondes", "1 minute", "1 minute 30 secondes"])
        
    methode = st.selectbox(
        "🎬 Méthode de Réalisation", 
        [
            "Tournage Humain (Visage caméra + B-roll)", 
            "IA Text-to-Video (Pour InVideo / CapCut)"
        ]
    )
    
    ambiance_musique = st.text_input("🎵 Ambiance Sonore / BPM (Optionnel)", placeholder="ex: House 126 BPM, Drop puissant à 15s...")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 Déployer le Kit AutoClip"):
        if not sujet_clip:
            st.warning("⚠️ Majesté, veuillez renseigner un sujet.")
        else:
            with st.spinner("🌌 L'Empire orchestre la création de votre kit..."):
                prompt = f"""
                Tu es le Directeur Artistique suprême de l'Empire pour {plateforme}.
                Génère un Kit de Production de niveau Impérial pour une vidéo de {duree} sur : '{sujet_clip}' (Style: {style_clip}, Ton: {ton_clip}).
                Méthode : {methode}. Ambiance sonore : {ambiance_musique}.
                
                Structure :
                ### 🎬 1. Titres Explosifs & Couverture
                - 2 Titres viraux & Texte Vignette.
                ### 🪝 2. Script de Production Mètre-Ruban ({duree})
                - Accroche, Développement séquencé et Outro de conversion.
                ### 📝 3. Optimisation SEO & Réseaux
                - Description engageante et hashtags stratégiques.
                """
                
                headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
                payload = {"model": "openai/gpt-oss-120b", "messages": [{"role": "user", "content": prompt}]}
                
                try:
                    res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, data=json.dumps(payload)).json()
                    if "choices" in res:
                        contenu = res["choices"][0]["message"]["content"]
                        st.toast("👑 Votre kit impérial est prêt !", icon="⚡")
                        st.markdown(contenu)
                        st.divider()
                        st.code(contenu, language="markdown")
                    else:
                        st.error("Erreur de génération par l'Empire.")
                except Exception as e:
                    st.error(f"Erreur : {e}")

# ==========================================
# 2. LYRICPULSE AI (Paroles & Clips)
# ==========================================
elif "LyricPulse" in choix_outil:
    st.markdown("### 🎵 LyricPulse AI — Division Musicale & Artistique")
    st.caption("Façonnez des hymnes intemporels et des concepts visuels souverains pour vos tracks.")
    
    genre_musique = st.selectbox("🎹 Genre Musical", ["House / Deep House", "Tech House", "Synthwave / Electronic", "Hip-Hop / Trap", "Pop / Commercial"])
    theme_morceau = st.text_input("💡 Thème ou Émotion du morceau", placeholder="ex: Nuit d'été en club, évasion, énergie pure, mélancolie nocturne...")
    ambiance_paroles = st.selectbox("🎙️ Style d'écriture", ["Anglais (Vocal puissant & accrocheur)", "Français (Poétique & Rythmé)", "Instru / Minimaliste (Quelques vocaux percutants)"])
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🎶 Composer l'Hymne et le Concept"):
        if not theme_morceau:
            st.warning("⚠️ Majesté, veuillez indiquer le thème du morceau.")
        else:
            with st.spinner("🎹 L'Empire compose les harmonies et structure le clip..."):
                prompt = f"""
                Tu es le Producer et Directeur Musical légendaire de l'Empire.
                Génère une œuvre musicale et visuelle complète pour un morceau de {genre_musique} axé sur : '{theme_morceau}' (Style d'écriture : {ambiance_paroles}).
                
                Structure ta réponse ainsi :
                ### 🎤 1. Paroles Impériales (Structure complète)
                - Intro / Couplet / Refrain / Pont / Outro avec instructions de voix.
                ### 🎥 2. Concept de Clip Vidéo Scène par Scène
                - Ambiance lumineuse, décors, tenues, rythme de montage et effets visuels calés sur le beat.
                ### 📢 3. Stratégie de Sortie & Teasing Réseaux
                - Idées de posts pour annoncer le son avant la sortie.
                """
                
                headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
                payload = {"model": "openai/gpt-oss-120b", "messages": [{"role": "user", "content": prompt}]}
                
                try:
                    res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, data=json.dumps(payload)).json()
                    if "choices" in res:
                        contenu = res["choices"][0]["message"]["content"]
                        st.toast("👑 Votre œuvre musicale est prête !", icon="🎵")
                        st.markdown(contenu)
                        st.divider()
                        st.code(contenu, language="markdown")
                    else:
                        st.error("Erreur de composition.")
                except Exception as e:
                    st.error(f"Erreur : {e}")

# ==========================================
# 3. BIOCRAFT AI (Profils Pro & Bios d'Élite)
# ==========================================
elif "BioCraft" in choix_outil:
    st.markdown("### 💼 BioCraft AI — Division Identité & Rayonnement")
    st.caption("Sculptez une image de marque et des profils sociaux d'une prestance absolue.")
    
    plateforme_bio = st.selectbox("🌐 Réseau Principal", ["TikTok / Instagram", "LinkedIn / Professionnel", "Spotify / SoundCloud (Artiste)"])
    parcours = st.text_area("✍️ Votre parcours, vos passions ou vos réalisations", placeholder="ex: Producteur de house music, étudiant en droit d'affaires, passionné par la tech...")
    objectif = st.selectbox("🎯 Objectif Souhaité", ["Impressionner et asseoir son autorité", "Attirer des partenariats / clients", "Générer un maximum d'abonnés curieux"])
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("👑 Forger l'Identité Impériale"):
        if not parcours:
            st.warning("⚠️ Majesté, veuillez renseigner quelques éléments sur votre parcours.")
        else:
            with st.spinner("✨ L'Empire forge votre blason numérique..."):
                prompt = f"""
                Tu es le Grand Chancelier en Image de Marque et Personal Branding pour l'élite.
                Génère un profil et des bios de niveau Impérial pour {plateforme_bio} basés sur : '{parcours}' (Objectif : {objectif}).
                
                Structure ta réponse ainsi :
                ### 🔥 1. 3 Options de Bios Souveraines (Courtes & Impactantes)
                - Option Alpha / Option Mystique / Option Directe avec émojis choisis avec parcimonie.
                ### 🔗 2. Appel à l'Action (CTA) & Liens Stratégiques
                - Formules pour inciter à cliquer sur le lien en bio.
                ### 🚀 3. Message d'Accroche / Pitch de Présentation (DM ou Accueil)
                - Un message de bienvenue percutant pour marquer les esprits dès la première seconde.
                """
                
                headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
                payload = {"model": "openai/gpt-oss-120b", "messages": [{"role": "user", "content": prompt}]}
                
                try:
                    res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, data=json.dumps(payload)).json()
                    if "choices" in res:
                        contenu = res["choices"][0]["message"]["content"]
                        st.toast("👑 Votre identité royale est forgée !", icon="💼")
                        st.markdown(contenu)
                        st.divider()
                        st.code(contenu, language="markdown")
                    else:
                        st.error("Erreur de forgeage.")
                except Exception as e:
                    st.error(f"Erreur : {e}")

st.markdown("<br><hr><p style='text-align: center; color: #64748b; font-size: 0.85rem;'>The Imperial Suite — Propulsé pour les Maîtres du Jeu.</p>", unsafe_allow_html=True)
