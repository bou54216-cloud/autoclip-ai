import streamlit as st
import requests
import json

# 1. Configuration de la page
st.set_page_config(
    page_title="The Empire Studio — Creative Suite",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Design Minimaliste / Brutaliste & Fluide (Inspiré de l'univers créatif de Federico Valla)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Fond épuré et sophistiqué */
    .stApp {
        background: #09090b;
        color: #f4f4f5;
    }

    /* En-tête style éditorial */
    .editorial-header {
        text-align: center;
        padding: 40px 20px 20px 20px;
    }
    
    .editorial-tag {
        font-size: 0.75rem;
        font-weight: 800;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #71717a;
        margin-bottom: 10px;
        display: inline-block;
    }

    .editorial-title {
        font-size: 2.8rem;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -1px;
        margin-bottom: 10px;
        line-height: 1.1;
    }

    .editorial-subtitle {
        font-size: 1rem;
        color: #a1a1aa;
        max-width: 500px;
        margin: 0 auto;
    }

    /* Cartes interactives haut de gamme (Style Portfolio Créatif) */
    .card-wrapper {
        background: #121216;
        border: 1px solid #27272a;
        border-radius: 20px;
        padding: 35px 25px;
        text-align: left;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }

    .card-wrapper:hover {
        border-color: #3f3f46;
        transform: translateY(-4px);
        background: #18181b;
        box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.7);
    }

    .card-number {
        font-size: 0.8rem;
        font-weight: 600;
        color: #52525b;
        margin-bottom: 15px;
        font-family: monospace;
    }

    .card-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 10px;
    }

    .card-desc {
        font-size: 0.9rem;
        color: #a1a1aa;
        line-height: 1.5;
        margin-bottom: 20px;
    }

    /* Champs de saisie intégrés et propres */
    .stTextInput input, .stSelectbox div[data-baseweb="select"], .stTextArea textarea {
        background-color: #121216 !important;
        border: 1px solid #27272a !important;
        border-radius: 12px !important;
        color: #f4f4f5 !important;
    }
    
    .stTextInput input:focus, .stSelectbox div[data-baseweb="select"]:focus-within, .stTextArea textarea:focus {
        border-color: #ffffff !important;
        box-shadow: 0 0 0 1px #ffffff !important;
    }

    /* Bouton d'action principal */
    .stButton>button {
        width: 100%;
        background: #ffffff;
        color: #09090b;
        font-weight: 700;
        font-size: 0.95rem;
        border-radius: 12px;
        padding: 14px 20px;
        border: none;
        cursor: pointer;
        transition: all 0.2s ease;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .stButton>button:hover {
        background: #e4e4e7;
        color: #000000;
        transform: translateY(-1px);
    }
    </style>
""", unsafe_allow_html=True)

# Clé API Groq
GROQ_API_KEY = "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"

# Gestion de la session
if "module_choisi" not in st.session_state:
    st.session_state["module_choisi"] = None

# --- BARRE DE NAVIGATION INTERNE SI UN MODULE EST CHOISI ---
if st.session_state["module_choisi"] is not None:
    col_nav1, col_nav2 = st.columns([8, 2])
    with col_nav2:
        if st.button("← Accueil"):
            st.session_state["module_choisi"] = None
            st.rerun()

# =========================================================
# ÉCRAN D'ACCUEIL : LES DEUX CARTES ÉDITORIALES
# =========================================================
if st.session_state["module_choisi"] is None:
    st.markdown("""
        <div class="editorial-header">
            <span class="editorial-tag">Selected Works & Systems — 2026</span>
            <h1 class="editorial-title">The Empire Studio</h1>
            <p class="editorial-subtitle">Sélectionnez le module créatif à déployer.</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_gauche, col_droite = st.columns(2, gap="large")

    with col_gauche:
        st.markdown("""
            <div class="card-wrapper">
                <div class="card-number">01 // VIDEO ENGINE</div>
                <div class="card-title">AutoClip AI</div>
                <div class="card-desc">Génération de scripts vidéo, hooks viraux, titres dynamiques et structures pour TikTok, Reels et Shorts.</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Lancer AutoClip ↗", key="btn_autoclip"):
            st.session_state["module_choisi"] = "AutoClip"
            st.rerun()

    with col_droite:
        st.markdown("""
            <div class="card-wrapper">
                <div class="card-number">02 // BRAND IDENTITY</div>
                <div class="card-title">BioCraft AI</div>
                <div class="card-desc">Architecture d'identité de marque, bios magnétiques d'élite et positionnement stratégique.</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Lancer BioCraft ↗", key="btn_biocraft"):
            st.session_state["module_choisi"] = "BioCraft"
            st.rerun()

# =========================================================
# MODULE 1 : AUTOCLIP AI
# =========================================================
elif st.session_state["module_choisi"] == "AutoClip":
    st.markdown("### ⚡ AutoClip AI — Configuration Vidéo")
    st.caption("Paramétrez votre contenu pour obtenir un rendu immédiat et structuré.")
    
    sujet_clip = st.text_input("🎯 Sujet ou concept de la vidéo", placeholder="ex: 3 clés pour composer une Bassline House percutante")
    
    c1, c2 = st.columns(2)
    with c1:
        plateforme = st.selectbox("📱 Plateforme Cible", ["TikTok", "Instagram Reels", "YouTube Shorts"])
        style_clip = st.selectbox("🎨 Style de Format", ["Éducatif / Conseil", "Storytelling", "Promotion Musique / Art", "Divertissement"])
        type_rendu_autoclip = st.selectbox("📌 Type de Résultat", ["Texte final prêt à publier", "Script / Prompt de consignes pour une IA vidéo"])
    with c2:
        ton_clip = st.selectbox("🎙️ Ton Souhaité", ["Énergique & Rythmé", "Humoristique & Décalé", "Cash & Direct", "Professionnel & Inspirant"])
        duree = st.selectbox("⏱️ Durée Estimée", ["15 secondes", "30 secondes", "45 secondes", "1 minute", "1 minute 30 secondes"])
        
    methode = st.selectbox("🎬 Méthode de Réalisation", ["Tournage Humain (Visage caméra + B-roll)", "Génération IA (InVideo / CapCut)"])
    ambiance_musique = st.text_input("🎵 Ambiance Sonore / BPM (Optionnel)", placeholder="ex: House 126 BPM...")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Générer le Kit Vidéo ↗"):
        if not sujet_clip:
            st.warning("⚠️ Veuillez renseigner un sujet.")
        else:
            with st.spinner("Génération en cours..."):
                prompt = f"""
                Tu es un expert mondial en création de contenu viral sur {plateforme}.
                Génère un Kit de Production Complet ({type_rendu_autoclip}) pour une vidéo de {duree} sur : '{sujet_clip}' (Style: {style_clip}, Ton: {ton_clip}).
                Méthode : {methode}. Ambiance sonore : {ambiance_musique}.
                
                Rédige directement un texte extrêmement détaillé et prêt à l'emploi.
                Format de sortie :
                ### 🎬 Titres & Couverture
                ### 🪝 Script de Production ({duree})
                ### 📝 Description & Hashtags SEO
                """
                
                headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
                payload = {"model": "openai/gpt-oss-120b", "messages": [{"role": "user", "content": prompt}]}
                
                try:
                    res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, data=json.dumps(payload)).json()
                    if "choices" in res:
                        contenu = res["choices"][0]["message"]["content"]
                        st.toast("Contenu généré !", icon="✨")
                        st.markdown("### 📋 Votre texte prêt à l'emploi :")
                        st.code(contenu, language="markdown")
                    else:
                        st.error("Erreur de génération.")
                except Exception as e:
                    st.error(f"Erreur : {e}")

# =========================================================
# MODULE 2 : BIOCRAFT AI
# =========================================================
elif st.session_state["module_choisi"] == "BioCraft":
    st.markdown("### 💼 BioCraft AI — Architecture d'Identité")
    st.caption("Définissez votre positionnement de marque.")
    
    c1, c2 = st.columns(2)
    with c1:
        plateforme_bio = st.selectbox("🌐 Plateforme Principale", ["TikTok / Instagram (Créateur / Artiste)", "LinkedIn (Professionnel / Corporate)", "Spotify / SoundCloud (Musicien)", "Site Web / Portfolio"])
        ton_bio = st.selectbox("🎯 Posture de Marque", ["Autoritaire & Visionnaire", "Mystérieux & Énigmatique", "Accessible & Pédagogue", "Audacieux & Disruptif"])
        type_rendu_bio = st.selectbox("📌 Type de Résultat", ["Texte final prêt à publier (Bios & CTA)", "Script / Prompt de consignes pour une IA de branding"])
    with c2:
        objectif_bio = st.selectbox("📈 Objectif Principal", ["Attirer des opportunités B2B", "Convertir en abonnés fidèles", "Vendre un produit / service / musique", "Établir une crédibilité instantanée"])
        longueur_bio = st.selectbox("📏 Format de la Bio", ["Ultra-court & Percutant", "Narratif & Inspirant", "À puces / Preuve sociale"])
        style_emojis = st.selectbox("✨ Style d'Émojis", ["Minimaliste & Chic", "Dynamique & Thématique", "Aucun"])

    parcours_pro = st.text_area("✍️ Votre parcours, compétences clés ou accomplissements", placeholder="Renseignez votre parcours ici...", height=120)
    mots_cles_cles = st.text_input("🔑 Mots-clés incontournables (Optionnel)", placeholder="ex: Droit des Affaires, House Music...")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Forger l'Identité ↗"):
        if not parcours_pro:
            st.warning("⚠️ Veuillez renseigner votre parcours.")
        else:
            with st.spinner("Création en cours..."):
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
                
                Rédige directement un texte détaillé et prêt à copier.
                Format de sortie :
                ### 🎯 Analyse du Positionnement
                ### ✍️ Options de Bios Prêtes à Copier
                ### 🔗 Formules d'Appel à l'Action (CTA)
                """
                
                headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
                payload = {"model": "openai/gpt-oss-120b", "messages": [{"role": "user", "content": prompt}]}
                
                try:
                    res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, data=json.dumps(payload)).json()
                    if "choices" in res:
                        contenu = res["choices"][0]["message"]["content"]
                        st.toast("Identité forgée !", icon="✨")
                        st.markdown("### 📋 Votre texte prêt à l'emploi :")
                        st.code(contenu, language="markdown")
                    else:
                        st.error("Erreur de génération.")
                except Exception as e:
                    st.error(f"Erreur : {e}")

st.markdown("<br><hr style='border-color: #27272a;'><p style='text-align: center; color: #52525b; font-size: 0.8rem;'>The Empire Studio — All Rights Reserved.</p>", unsafe_allow_html=True)
