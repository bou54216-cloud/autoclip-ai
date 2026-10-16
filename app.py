import streamlit as st
import requests
import json

# 1. Configuration de la page
st.set_page_config(
    page_title="AutoClip AI — Next-Gen Content Studio",
    page_icon="⚡",
    layout="wide",
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
        padding: 40px 20px 20px 20px;
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
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 20%, #c084fc 60%, #38bdf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
        line-height: 1.1;
    }

    .hero-subtitle {
        font-size: 1.2rem;
        color: #94a3b8;
        max-width: 650px;
        margin: 0 auto 40px auto;
    }

    /* Effet Glassmorphism pour les blocs */
    div[data-testid="stVerticalBlock"] > div {
        border-radius: 16px;
    }
    
    .stTextInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: #f8fafc !important;
        backdrop-filter: blur(12px);
        transition: all 0.3s ease;
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
        <h1 class="hero-title">Créez des Vidéos Virales à la Vitesse de la Lumière</h1>
        <p class="hero-subtitle">Générez des scripts captivants, des titres explosifs et des kits réseaux parfaits pour l'humain et les IA vidéo.</p>
    </div>
""", unsafe_allow_html=True)

# Colonnes principales
col_left, col_right = st.columns([1, 1.2], gap="large")

with col_left:
    st.markdown("### 🎛️ Configuration du Studio")
    
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
