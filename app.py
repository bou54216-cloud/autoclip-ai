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
            st.warning("⚠️ Veuillez renseigner un sujet.")
        else:
            with st.spinner("🌌 Orchestration de la création du kit..."):
                prompt = f"""
                Tu es le Directeur Artistique suprême pour {plateforme}.
                Génère un Kit de Production de niveau supérieur pour une vidéo de {duree} sur : '{sujet_clip}' (Style: {style_clip}, Ton: {ton_clip}).
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
                        st.toast("⚡ Kit de production généré avec succès !", icon="🚀")
                        st.markdown(contenu)
                        st.divider()
                        st.code(contenu, language="markdown")
                    else:
                        st.error("Erreur de génération.")
                except Exception as e:
                    st.error(f"Erreur : {e}")

# ==========================================
# 2. LYRICPULSE AI (Paroles & Clips d'Élite)
# ==========================================
elif "LyricPulse" in choix_outil:
    st.markdown("### 🎵 LyricPulse AI — Division Musicale & Artistique")
    st.caption("Conception artistique sur-mesure : écriture millimétrée, structure des émotions et storyboard de clip.")
    
    c1, c2 = st.columns(2)
    with c1:
        genre_musique = st.selectbox("🎹 Genre Musical", ["House / Deep House", "Tech House", "Synthwave / Electronic", "Hip-Hop / Trap", "Pop / Commercial", "RnB / Lo-Fi"])
        structure_morceau = st.selectbox("🎼 Structure Souhaitée", ["Standard (Intro > Couplet > Refrain > Pont > Outro)", "Club Extended (Grosse intro, drop massif, break, second drop)", "Court / Formateur (Direct au refrain / Idéal TikTok)"])
        langue_chant = st.selectbox("🌍 Langue des Paroles", ["Anglais (Standard international)", "Français (Moderne & Poétique)", "Anglais avec phrasé FR / Bilingue"])
    with c2:
        ambiance_paroles = st.selectbox("🎙️ Style / Vibe Vocale", ["Vocaux anglais captivants & groovy (Style House)", "Énergique & Euphorique (Festival / Club)", "Mélancolique & Nocturne", "Hypnotique & Planant"])
        style_voix = st.selectbox("🗣️ Texture Vocale", ["Vocaux pitchés & rythmés (Staccato)", "Voix aérienne & éthérée (Reverb prononcée)", "Spoken Word / Chant parlé intense", "Mélodie entraînante et entêtante (Earworm)"])

    theme_morceau = st.text_area("💡 Histoire, concept précis ou mots-clés à intégrer", placeholder="ex: Une nuit blanche d'été à Ibiza, l'adrénaline du dancefloor, la sensation de liberté au moment du drop...")
    ref_artiste = st.text_input("🎧 Artistes de référence (Optionnel)", placeholder="ex: CH@NC3, Fred again.., Fisher, Daft Punk...")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🎹 Composer l'Œuvre Musicale & Visuelle"):
        if not theme_morceau:
            st.warning("⚠️ Veuillez indiquer le concept ou l'histoire du morceau.")
        else:
            with st.spinner("🎵 Analyse harmonique et rédaction artistique en cours..."):
                prompt = f"""
                Tu es un Producer, Auteur-Compositeur et Réalisateur de clips de renommée internationale.
                Crée une œuvre musicale et visuelle d'une précision absolue basée sur les critères suivants :
                - Genre : {genre_musique}
                - Structure : {structure_morceau}
                - Langue : {langue_chant}
                - Vibe / Émotion : {ambiance_paroles}
                - Texture Vocale : {style_voix}
                - Concept / Histoire : '{theme_morceau}'
                - Références artistiques : {ref_artiste if ref_artiste else "Libre"}
                
                Structure ta réponse de manière ultra-détaillée :
                ### 🎼 1. Analyse & Direction Artistique du Morceau
                - BPM conseillé, choix des accords principaux et design sonore global.
                
                ### 🎤 2. Paroles Intégrales (Section par Section)
                - Écris l'intégralité des paroles ({langue_chant}) avec les indications de placement rythmique et les effets sur la voix (ex: [Effet radio], [Écho lourd sur le mot...]).
                
                ### 🎥 3. Storyboard & Concept du Clip Vidéo (Scène par Scène)
                - Description minutieuse du clip : colorimétrie, lumières stroboscopiques ou douces, tenues, jeu d'acteur, mouvements de caméra et synchronisation exacte des images avec le drop ou les temps forts.
                
                ### 🚀 4. Stratégie de Teasing & Sortie
                - 3 idées de concepts de vidéos courtes pour teaser le son sur TikTok/Reels avant la sortie.
                """
                
                headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
                payload = {"model": "openai/gpt-oss-120b", "messages": [{"role": "user", "content": prompt}]}
                
                try:
                    res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, data=json.dumps(payload)).json()
                    if "choices" in res:
                        contenu = res["choices"][0]["message"]["content"]
                        st.toast("🎵 Œuvre musicale et visuelle générée avec succès !", icon="🎶")
                        st.markdown(contenu)
                        st.divider()
                        st.code(contenu, language="markdown")
                    else:
                        st.error("Erreur de composition.")
                except Exception as e:
                    st.error(f"Erreur : {e}")

# ==========================================
# 3. BIOCRAFT AI (Identité Pro & Stratégie)
# ==========================================
elif "BioCraft" in choix_outil:
    st.markdown("### 💼 BioCraft AI — Division Identité & Rayonnement")
    st.caption("Architecture d'image de marque : positionnement, bios magnétiques et messages de conversion.")
    
    c1, c2 = st.columns(2)
    with c1:
        plateforme_bio = st.selectbox("🌐 Plateforme Principale", ["TikTok / Instagram (Créateur / Artiste)", "LinkedIn (Professionnel / Corporate)", "Spotify / SoundCloud (Musicien)", "Site Web / Portfolio (Landing Page)"])
        ton_bio = st.selectbox("🎯 Posture de Marque", ["Autoritaire & Visionnaire (Expert incontesté)", "Mystérieux & Énigmatique (Génère la curiosité)", "Accessible & Pédagogue (Proche de sa communauté)", "Audacieux & Disruptif (Casqueur de codes)"])
        objectif_bio = st.selectbox("📈 Objectif Numéro 1", ["Attirer des opportunités B2B / Partenariats", "Convertir les visiteurs en abonnés fidèles", "Vendre un produit, service ou une œuvre musicale", "Établir une crédibilité instantanée"])
    with c2:
        longueur_bio = st.selectbox("📏 Format de la Bio", ["Ultra-court & Percutant (Ligne par ligne)", "Narratif & Inspirant (Mini-histoire)", "À puces / Chiffré (Preuve sociale forte)"])
        style_emojis = st.selectbox("✨ Utilisation des Émojis", ["Minimaliste & Chic (1 ou 2 max)", "Dynamique & Thématique (En lien avec la niche)", "Aucun (Pur style minimaliste strict)"])

    # Texte pré-rempli sur mesure direct
    parcours_default = "Étudiant passionné en droit des affaires et futur avocat d'affaires. Parallèlement producteur de house music indépendant et créateur de contenu sur TikTok. Je combine la rigueur juridique et la créativité artistique pour bâtir des projets innovants."
    
    parcours_pro = st.text_area("✍️ Votre parcours, vos compétences clés ou vos accomplissements", value=parcours_default, height=120)
    mots_cles_cles = st.text_input("🔑 Mots-clés ou termes incontournables à placer (Optionnel)", value="Droit des Affaires, House Music, TikTok, Innovation")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("✨ Forger l'Identité de Marque"):
        if not parcours_pro:
            st.warning("⚠️ Veuillez renseigner votre parcours ou vos réalisations.")
        else:
            with st.spinner("💼 Calcul du positionnement et forgeage des bios..."):
                prompt = f"""
                Tu es un Directeur de Stratégie en Image de Marque et Personal Branding pour célébrités et entrepreneurs d'élite.
                Conçois une architecture d'identité numérique d'une puissance redoutable basée sur :
                - Plateforme : {plateforme_bio}
                - Posture : {ton_bio}
                - Objectif : {objectif_bio}
                - Format : {longueur_bio}
                - Style d'émojis : {style_emojis}
                - Parcours et réalisations : '{parcours_pro}'
                - Mots-clés obligatoires : {mots_cles_cles}
                
                Structure ta réponse de manière exhaustive :
                ### 🎯 1. Analyse du Positionnement & de l'Angle d'Attaque
                - Définition de la promesse unique et de la psychologie de l'audience vis-à-vis du profil.
                
                ### ✍️ 2. Les 4 Options de Bios Magnétiques (Prêtes à copier)
                - Fournis 4 variations distinctes selon l'angle (ex: L'autoritaire, Le provocateur de curiosité, Le minimaliste chic, Le factuel axé résultats).
                
                ### 🔗 3. Stratégie de Lien (Call-to-Action)
                - 3 formules irrésistibles pour inciter au clic sur le lien en bio (selon l'objectif : {objectif_bio}).
                
                ### 💬 4. Le Message d'Accueil / Premier Contact (DM ou Section À Propos)
                - Un texte d'introduction percutant qui convertit instantanément un visiteur en allié ou en client.
                """
                
                headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
                payload = {"model": "openai/gpt-oss-120b", "messages": [{"role": "user", "content": prompt}]}
                
                try:
                    res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, data=json.dumps(payload)).json()
                    if "choices" in res:
                        contenu = res["choices"][0]["message"]["content"]
                        st.toast("💼 Identité de marque forgée avec succès !", icon="👑")
                        st.markdown(contenu)
                        st.divider()
                        st.code(contenu, language="markdown")
                    else:
                        st.error("Erreur de génération.")
                except Exception as e:
                    st.error(f"Erreur : {e}")

st.markdown("<br><hr><p style='text-align: center; color: #64748b; font-size: 0.85rem;'>The Imperial Suite — Propulsé pour les Maîtres du Jeu.</p>", unsafe_allow_html=True)
