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

# En-tête
st.markdown("""
    <div class="imperial-container">
        <span class="imperial-badge">👑 The Imperial Suite — All-Access</span>
        <h1 class="imperial-title">Plateforme Souveraine</h1>
        <p class="imperial-subtitle">Sélectionnez ci-dessous l'outil de précision que vous souhaitez déployer.</p>
    </div>
""", unsafe_allow_html=True)

# Clé API Groq
GROQ_API_KEY = "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"

# --- CHOIX DE L'OUTIL ---
choix_outil = st.selectbox(
    "🏛️ Choisissez votre division :",
    [
        "⚡ AutoClip AI (Vidéos & Kits Viraux)", 
        "🎵 LyricPulse AI (Paroles & Concepts de Clips d'Élite)", 
        "💼 BioCraft AI (Identité Pro & Stratégie de Marque)"
    ]
)

st.markdown("---")

# ==========================================
# 1. AUTOCLIP AI
# ==========================================
