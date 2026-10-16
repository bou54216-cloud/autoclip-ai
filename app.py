import streamlit as st
import requests
import json

# 1. Configuration de la page
st.set_page_config(
    page_title="AutoClip AI — Next-Gen Content Studio",
    page_icon="⚡",
    layout="centered", # Centré pour un meilleur rendu de haut en bas
    initial_sidebar_state="collapsed"
)

# 2. Design Ultra-Futuriste (Glassmorphism + Neon Glow)
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

    /* En-tête Principal WOW */
    .hero-container {
        text-align: center;
        padding: 30px 20px 10px 20px;
    }
    
    .hero-badge {
        background: linear-gradient(90deg, rgba(168, 85, 247, 0.2), rgba(59, 130, 246, 0.2));
        border: 1px solid rgba(168, 85, 247, 0.4);
        color: #c084fc;
        padding: 6px 16px;
        border-radius: 30px;
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        display: inline-block;
        margin-bottom: 15px;
        box-shadow: 0 0 15px rgba(168, 85, 247, 0.3);
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
    .stTextInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: rgba(15, 23, 42, 0.7) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: #f8fafc !important;
        backdrop-filter: blur(12px);
    }
    
    .stTextInput input:focus, .stSelectbox div[data-baseweb="select"]:focus-within {
        border-color: #a855f7 !important;
        box-shadow: 0 0 15px rgba(168, 85, 247, 0.4) !important;
    }

    /* Le Bouton WOW Ultra-Futuriste */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #8b5cf6 0%, #d946ef 50%, #06b6d4 100%);
        background-size: 200% auto;
        color: white;
        font-weight: 800;
        font-size: 1.2rem;
        border-radius: 14px;
        padding: 18px 24px;
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

# Hero Section
st.markdown("""
    <div class="hero-container">
        <span class="hero-badge">✨ AutoClip Engine v3.0</span>
        <h1 class="hero-title">Créez des Vidéos Virales</h1>
        <p class="hero-subtitle">Générez des scripts captivants, des titres explosifs et des kits réseaux parfaits de haut en bas.</p>
    </div>
""", unsafe_allow_html=True)

# --- TOUT EN HAUT DE BAS (Formulaire vertical) ---
st.markdown("### 🎛️ 1. Configuration du Studio")

sujet = st.text_input("🎯 Quel est le sujet de ta vidéo ?", placeholder="ex: 3 astuces pour composer une Bassline House incroyable")

c1, c2 = st.columns(2)
with c1:
    plateforme = st.selectbox("📱 Plateforme Cible", ["TikTok", "Instagram Reels", "YouTube Shorts"])
    style = st.selectbox("🎨 Style de Format", ["Éducatif / Conseil", "Storytelling", "Promotion Musique / Art", "Divertissement"])
with c2:
    ton = st.selectbox("🎙️ Ton & Ambiance", ["Énergique & Rythmé", "Humoristique & Décalé", "Cash & Direct", "Professionnel & Inspirant"])
    duree = st.selectbox("⏱️ Durée Estimée", ["15 secondes", "30 secondes", "45 secondes", "1 minute", "1 minute 30 secondes"])
    
methode = st.selectbox(
    "🎬 Méthode de Réalisation", 
    [
        "Tournage Humain (Visage caméra + B-roll)", 
        "IA Text-to-Video (Pour InVideo / CapCut)"
    ]
)

ambiance_musique = st.text_input(
    "🎵 Musique & Synchro Sonore (Optionnel)", 
    placeholder="ex: House 126 BPM, Drop puissant à 15s, Bassline groovy..."
)

st.markdown("<br>", unsafe_allow_html=True)
btn_generer = st.button("⚡ Générer le Kit Studio Pro")

st.markdown("---")

# --- SECTION RÉSULTAT EN DESSOUS ---
st.markdown("### 🚀 2. Rendu de Votre Kit Studio")

if btn_generer:
    if not sujet:
        st.warning("⚠️ Merci d'entrer un sujet pour lancer la génération !")
    else:
        with st.spinner("🌌 L'IA fusionne les algorithmes pour composer votre kit d'exception..."):
            
            GROQ_API_KEY = "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"
            
            instructions_methode = (
                "Rédige le script pour une personne réelle face caméra avec indications d'acting, d'expressions et d'angles."
                if "Tournage Humain" in methode else
                "Rédige le script sous forme de prompts ultra-descriptifs prêts à coller dans une IA vidéo (InVideo/CapCut)."
            )
            
            instruction_musique = f"Intègre des repères de synchronisation calés sur le rythme de cette musique/ambiance : '{ambiance_musique}'." if ambiance_musique else ""

            prompt = f"""
            Tu es un Director Creative Viral mondialement reconnu sur {plateforme}.
            Génère un Kit de Production Complet de niveau Masterclass pour une vidéo de {duree} sur : '{sujet}' (Style: {style}, Ton: {ton}).
            
            Directives :
            - {instructions_methode}
            - {instruction_musique}
            
            Format de sortie attendu :
            
            ### 🎬 1. Titres Explosifs & Couverture
            - **Option Titre A** : [Titre ultra-viral]
            - **Option Titre B** : [Alternative accrocheuse]
            - **Texte Vignette (Thumbnail)** : [3 à 4 mots max]

            ### 🪝 2. Script de Production Mètre-Ruban ({duree})
            - **[00:00 - 00:05] Accroche Dévastatrice** : [Hook visuel + Texte écran + Phrase choc + Synchro son]
            - **[Développement Séquencé]** : [Plans détaillés avec visuels B-roll, paroles exactes et variations de son/beat]
            - **[Outro & Conversion]** : [Appel à l'action irrésistible]

            ### 📝 3. Optimisation SEO & Réseaux
            - **Description** : [Texte captivant avec question ouverte d'engagement]
            - **Hashtags Ciblés** : [5 à 8 hashtags stratégiques pour la niche]
            """
            
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "openai/gpt-oss-120b",
                "messages": [{"role": "user", "content": prompt}]
            }
            
            try:
                response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, data=json.dumps(payload))
                result = response.json()
                
                if response.status_code == 200:
                    kit_genere = result["choices"][0]["message"]["content"]
                    st.balloons()
                    st.success("🔥 Votre kit d'élite a été créé avec succès !")
                    
                    st.markdown(kit_genere)
                    
                    st.divider()
                    st.markdown("##### 📋 Copier tout le Kit en 1-Clic")
                    st.code(kit_genere, language="markdown")
                else:
                    st.error(f"Erreur API : {result.get('error', {}).get('message', 'Erreur inconnue')}")
            except Exception as e:
                st.error(f"Erreur de connexion : {e}")
else:
    st.info("⚡ **Prêt à frapper fort ?** Remplis le formulaire ci-dessus et clique sur le bouton pour voir la magie opérer en dessous.")
