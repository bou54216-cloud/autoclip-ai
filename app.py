import streamlit as st
import requests
import json

# 1. Configuration de la page
st.set_page_config(
    page_title="The Empire Studio — Executive Content Suite",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Design Ultra-Futuriste & Cartes de Sélection (Glassmorphism CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Arrière-plan Spatial / Cyber */
    .stApp {
        background: radial-gradient(circle at 50% -20%, #1e1b4b 0%, #0f172a 45%, #020617 100%);
        color: #f8fafc;
    }

    /* En-tête Principal */
    .hero-container {
        text-align: center;
        padding: 30px 20px 10px 20px;
    }
    
    .hero-badge {
        background: linear-gradient(90deg, rgba(168, 85, 247, 0.2), rgba(59, 130, 246, 0.2));
        border: 1px solid rgba(168, 85, 247, 0.4);
        color: #c084fc;
        padding: 6px 18px;
        border-radius: 30px;
        font-size: 0.85rem;
        font-weight: 800;
        letter-spacing: 2px;
        text-transform: uppercase;
        display: inline-block;
        margin-bottom: 15px;
        box-shadow: 0 0 20px rgba(168, 85, 247, 0.3);
    }

    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 20%, #c084fc 60%, #38bdf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
        line-height: 1.1;
    }

    .hero-subtitle {
        font-size: 1.1rem;
        color: #94a3b8;
        max-width: 600px;
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
        border-color: #a855f7 !important;
        box-shadow: 0 0 15px rgba(168, 85, 247, 0.4) !important;
    }

    /* Le Bouton Futuriste */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #8b5cf6 0%, #d946ef 50%, #06b6d4 100%);
        background-size: 200% auto;
        color: white;
        font-weight: 800;
        font-size: 1.1rem;
        border-radius: 14px;
        padding: 16px 24px;
        border: none;
        box-shadow: 0 0 25px rgba(217, 70, 239, 0.4);
        cursor: pointer;
        transition: all 0.4s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .stButton>button:hover {
        background-position: right center;
        transform: translateY(-3px) scale(1.01);
        box-shadow: 0 0 35px rgba(217, 70, 239, 0.7);
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# En-tête
st.markdown("""
    <div class="hero-container">
        <span class="hero-badge">⚡ The Empire Studio v3.5</span>
        <h1 class="hero-title">Choisissez Votre Division</h1>
        <p class="hero-subtitle">Cliquez sur la division souhaitée pour déployer l'architecture de création dédiée.</p>
    </div>
""", unsafe_allow_html=True)

# Clé API Groq
GROQ_API_KEY = "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"

# Variable de session pour retenir le choix du module
if "module_choisi" not in st.session_state:
    st.session_state["module_choisi"] = None

# --- ÉCRAN D'ACCUEIL : 2 AFFICHES (Gauche: AutoClip / Droite: BioCraft) ---
col_gauche, col_droite = st.columns(2, gap="medium")

with col_gauche:
    st.markdown("""
        <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(168, 85, 247, 0.3); border-radius: 16px; padding: 20px; text-align: center;">
            <h2 style="color: #c084fc; font-size: 1.6rem; margin-bottom: 8px;">⚡ AutoClip AI</h2>
            <p style="color: #94a3b8; font-size: 0.9rem;">Génération de Scripts Vidéo, Hooks Viraux, Titres & Kits pour TikTok, Reels & Shorts.</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Sélectionner AutoClip AI 🎬", key="btn_autoclip"):
        st.session_state["module_choisi"] = "AutoClip"

with col_droite:
    st.markdown("""
        <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(56, 189, 248, 0.3); border-radius: 16px; padding: 20px; text-align: center;">
            <h2 style="color: #38bdf8; font-size: 1.6rem; margin-bottom: 8px;">💼 BioCraft AI</h2>
            <p style="color: #94a3b8; font-size: 0.9rem;">Architecture d'Identité de Marque, Bios Magnétiques & Positionnement d'Élite.</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Sélectionner BioCraft AI 💼", key="btn_biocraft"):
        st.session_state["module_choisi"] = "BioCraft"

st.markdown("---")

# =========================================================
# 1. QUESTIONNAIRE AUTOCLIP AI (Si sélectionné à gauche)
# =========================================================
if st.session_state["module_choisi"] == "AutoClip":
    st.markdown("### 🎬 AutoClip AI — Configuration Vidéo")
    st.caption("Remplissez les paramètres pour obtenir directement votre rendu.")
    
    sujet_clip = st.text_input("🎯 Quel est le sujet ou le concept de la vidéo ?", placeholder="ex: 3 erreurs à éviter pour composer une Bassline House")
    
    c1, c2 = st.columns(2)
    with c1:
        plateforme = st.selectbox("📱 Plateforme Cible", ["TikTok", "Instagram Reels", "YouTube Shorts"])
        style_clip = st.selectbox("🎨 Style de Format", ["Éducatif / Conseil", "Storytelling", "Promotion Musique / Art", "Divertissement"])
        type_rendu_autoclip = st.selectbox("📌 Type de Résultat Souhaité", ["Texte final directement utilisable pour publication", "Script / Prompt de consignes pour une IA vidéo (InVideo/CapCut)"])
    with c2:
        ton_clip = st.selectbox("🎙️ Ton Souhaité", ["Énergique & Rythmé", "Humoristique & Décalé", "Cash & Direct", "Professionnel & Inspirant"])
        duree = st.selectbox("⏱️ Durée Estimée", ["15 secondes", "30 secondes", "45 secondes", "1 minute", "1 minute 30 secondes"])
        
    methode = st.selectbox(
        "🎬 Méthode de Réalisation", 
        [
            "Tournage Humain (Visage caméra + B-roll)", 
            "Génération IA (InVideo / CapCut Script-to-Video)"
        ]
    )
    
    ambiance_musique = st.text_input("🎵 Ambiance Sonore / BPM (Optionnel)", placeholder="ex: House 126 BPM, Drop puissant à 15s...")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 Générer le Kit Vidéo AutoClip"):
        if not sujet_clip:
            st.warning("⚠️ Veuillez préciser un sujet.")
        else:
            with st.spinner("⚡ Génération du contenu en cours..."):
                prompt = f"""
                Tu es un expert mondial en création de contenu viral sur {plateforme}.
                Génère un Kit de Production Complet ({type_rendu_autoclip}) pour une vidéo de {duree} sur : '{sujet_clip}' (Style: {style_clip}, Ton: {ton_clip}).
                Méthode : {methode}. Ambiance sonore : {ambiance_musique}.
                
                Exigence : Rédige un texte extrêmement détaillé, complet et prêt à être utilisé directement sans bavardage.
                
                Format de sortie :
                ### 🎬 Titres & Couverture
                - 2 Titres ultra-viraux & Texte Vignette.
                ### 🪝 Script de Production ({duree})
                - Accroche, développement séquencé et appel à l'action.
                ### 📝 Description & Hashtags SEO
                - Description engageante et hashtags ciblés.
                """
                
                headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
                payload = {"model": "openai/gpt-oss-120b", "messages": [{"role": "user", "content": prompt}]}
                
                try:
                    res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, data=json.dumps(payload)).json()
                    if "choices" in res:
                        contenu = res["choices"][0]["message"]["content"]
                        st.toast("⚡ Contenu généré avec succès !", icon="🚀")
                        
                        st.markdown("### 📋 Votre texte prêt à l'emploi :")
                        st.code(contenu, language="markdown")
                    else:
                        st.error("Erreur de génération.")
                except Exception as e:
                    st.error(f"Erreur : {e}")

# =========================================================
# 2. QUESTIONNAIRE BIOCRAFT AI (Si sélectionné à droite)
# =========================================================
elif st.session_state["module_choisi"] == "BioCraft":
    st.markdown("### 💼 BioCraft AI — Architecture d'Identité")
    st.caption("Remplissez les détails pour obtenir votre positionnement de marque.")
    
    c1, c2 = st.columns(2)
    with c1:
        plateforme_bio = st.selectbox("🌐 Plateforme Principale", ["TikTok / Instagram (Créateur / Artiste)", "LinkedIn (Professionnel / Corporate)", "Spotify / SoundCloud (Musicien)", "Site Web / Portfolio (Landing Page)"])
        ton_bio = st.selectbox("🎯 Posture de Marque", ["Autoritaire & Visionnaire (Expert incontesté)", "Mystérieux & Énigmatique (Génère la curiosité)", "Accessible & Pédagogue (Proche de sa communauté)", "Audacieux & Disruptif (Casseur de codes)"])
        type_rendu_bio = st.selectbox("📌 Type de Résultat Souhaité", ["Texte final prêt à être publié (Bios & CTA)", "Script / Prompt de consignes pour une IA spécialisée en branding"])
    with c2:
        objectif_bio = st.selectbox("📈 Objectif Principal", ["Attirer des opportunités B2B / Partenariats", "Convertir les visiteurs en abonnés fidèles", "Vendre un produit, service ou une œuvre musicale", "Établir une crédibilité instantanée"])
        longueur_bio = st.selectbox("📏 Format de la Bio", ["Ultra-court & Percutant (Ligne par ligne)", "Narratif & Inspirant (Mini-histoire)", "À puces / Chiffré (Preuve sociale forte)"])
        style_emojis = st.selectbox("✨ Style d'Émojis", ["Minimaliste & Chic (1 ou 2 max)", "Dynamique & Thématique", "Aucun (Pur style minimaliste)"])

    parcours_pro = st.text_area("✍️ Votre parcours, compétences clés ou accomplissements", placeholder="Renseignez votre parcours, vos diplômes, votre art ou vos réussites ici...", height=120)
    mots_cles_cles = st.text_input("🔑 Mots-clés incontournables à placer (Optionnel)", placeholder="ex: Droit des Affaires, House Music, Innovation...")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("✨ Forger l'Identité BioCraft"):
        if not parcours_pro:
            st.warning("⚠️ Veuillez renseigner votre parcours ou accomplissements.")
        else:
            with st.spinner("💼 Forgerie de votre identité en cours..."):
                prompt = f"""
                Tu es un expert mondial en stratégie de marque et personal branding d'élite.
                Génère un contenu complet ({type_rendu_bio}) basé sur :
                - Plateforme : {plateforme_bio}
                - Posture : {ton_bio}
                - Objectif : {objectif_bio}
                - Format : {longueur_bio}
                - Émojis : {style_emojis}
                - Parcours : '{parcours_pro}'
                - Mots-clés : {mots_cles_cles}
                
                Rédige directement un texte extrêmement détaillé, propre et prêt à copier sans bavardage.
                
                Format de sortie :
                ### 🎯 Analyse du Positionnement
                ### ✍️ 4 Options de Bios Prêtes à Copier
                ### 🔗 Formules d'Appel à l'Action (CTA)
                ### 💬 Message d'Accueil / Premier Contact
                """
                
                headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
                payload = {"model": "openai/gpt-oss-120b", "messages": [{"role": "user", "content": prompt}]}
                
                try:
                    res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, data=json.dumps(payload)).json()
                    if "choices" in res:
                        contenu = res["choices"][0]["message"]["content"]
                        st.toast("💼 Identité forgée avec succès !", icon="✨")
                        
                        st.markdown("### 📋 Votre texte prêt à l'emploi :")
                        st.code(contenu, language="markdown")
                    else:
                        st.error("Erreur de génération.")
                except Exception as e:
                    st.error(f"Erreur : {e}")

st.markdown("<br><hr><p style='text-align: center; color: #64748b; font-size: 0.85rem;'>The Empire Studio — All Rights Reserved.</p>", unsafe_allow_html=True)
