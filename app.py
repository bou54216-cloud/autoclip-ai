import streamlit as st
import requests
import json

# 1. Configuration de la page en mode Large
st.set_page_config(
    page_title="AutoClip AI — Studio Créateur Premium",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. CSS Personnalisé Haut de Gamme (Design Dark Premium)
st.markdown("""
    <style>
    /* Arrière-plan global */
    .stApp {
        background-color: #0d0e15;
        color: #f1f5f9;
    }
    
    /* Titre Principal */
    .hero-title {
        font-size: 2.8rem;
        font-weight: 900;
        background: linear-gradient(135deg, #a855f7 0%, #6366f1 50%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
        letter-spacing: -1px;
    }
    
    .hero-subtitle {
        font-size: 1.1rem;
        color: #94a3b8;
        margin-bottom: 30px;
    }
    
    /* Cartes de sections */
    .premium-card {
        background: #181a25;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
    }
    
    /* Style du bouton principal */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #a855f7 0%, #6366f1 100%);
        color: white;
        font-weight: 700;
        font-size: 1.1rem;
        border-radius: 12px;
        padding: 14px 20px;
        border: none;
        box-shadow: 0 4px 15px rgba(168, 85, 247, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(168, 85, 247, 0.6);
        color: white;
    }
    
    /* Inputs et Selectbox stylisés */
    .stTextInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: #0f1017 !important;
        border-radius: 8px !important;
        border: 1px solid #2e3248 !important;
        color: #f8fafc !important;
    }
    
    /* Badges de statut */
    .badge-pro {
        background: rgba(168, 85, 247, 0.15);
        color: #c084fc;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        border: 1px solid rgba(168, 85, 247, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

# En-tête Premium
st.markdown('<span class="badge-pro">⚡ AUTOCLIP STUDIO PRO v2.5</span>', unsafe_allow_html=True)
st.markdown('<p class="hero-title">AutoClip AI Pro</p>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">Moteur IA haute performance pour générer vos kits viraux TikTok, Reels & Shorts.</p>', unsafe_allow_html=True)

# Disposition en 2 colonnes équilibrées
col_left, col_right = st.columns([1, 1.1], gap="large")

with col_left:
    st.markdown('### ⚙️ Paramètres du Projet')
    
    sujet = st.text_input("🎯 Quel est le sujet principal ?", placeholder="ex: 3 erreurs à éviter pour mixer la house music")
    
    c1, c2 = st.columns(2)
    with c1:
        plateforme = st.selectbox("📱 Plateforme cible", ["TikTok", "Instagram Reels", "YouTube Shorts"])
        style = st.selectbox("🎨 Format & Style", ["Éducatif / Conseil", "Storytelling", "Promotion Musique / Art", "Divertissement"])
    with c2:
        ton = st.selectbox("🎙️ Ton & Ambiance", ["Énergique & Rythmé", "Humoristique & Décalé", "Cash & Direct", "Professionnel & Inspirant"])
        duree = st.selectbox("⏱️ Durée de la vidéo", ["15 secondes", "30 secondes", "45 secondes", "1 minute", "1 minute 30 secondes"])
        
    methode = st.selectbox(
        "🛠️ Méthode de création", 
        [
            "Tournage humain (Face caméra & B-roll)", 
            "IA Text-to-Video (InVideo / CapCut Script-to-Video)"
        ]
    )
    
    ambiance_musique = st.text_input(
        "🎵 Musique / BPM / Synchro (Optionnel)", 
        placeholder="ex: House 126 BPM, Drop à 15s, Bassline percutante..."
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    btn_generer = st.button("✨ Générer le Kit Vidéo Pro")

with col_right:
    st.markdown('### 💎 Espace de Génération')
    
    if btn_generer:
        if not sujet:
            st.warning("⚠️ Veuillez préciser un sujet pour lancer l'analyse de l'IA.")
        else:
            with st.spinner("🧠 Optimisation des algorithmes et création du kit en cours..."):
                
                GROQ_API_KEY = "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"
                
                instructions_methode = (
                    "Rédige le script pour une personne réelle face caméra avec indications de jeu, de découpe et de plans."
                    if "Tournage humain" in methode else
                    "Rédige le script sous forme de prompts séquentiels et descriptifs prêts à être intégrés dans une IA vidéo (InVideo/CapCut)."
                )
                
                instruction_musique = f"Intègre des repères temporels de synchronisation basés sur l'ambiance musicale suivante : '{ambiance_musique}'." if ambiance_musique else ""

                prompt = f"""
                Tu es un Director Marketing Viral senior spécialisé dans les formats courts sur {plateforme}.
                Génère un Kit de Production Complet de niveau professionnel pour une vidéo de {duree} sur : '{sujet}' (Style: {style}, Ton: {ton}).
                
                Directives :
                - {instructions_methode}
                - {instruction_musique}
                
                Format de sortie attendu :
                
                ### 🎬 1. Titres Accrocheurs & Miniature
                - **Option Titre A** : [Titre ultra-engageant]
                - **Option Titre B** : [Alternative intrigante]
                - **Texte Vignette (Thumbnail)** : [3 à 4 mots percutants max]

                ### 🪝 2. Script de Production ({duree})
                - **[00:00 - 00:05] Accroche Visuelle & Audio** : [Hook visuel + Texte écran + Phrase choc + Synchro son]
                - **[Développement Séquencé]** : [Plans détaillés avec visuels B-roll, paroles exactes et indications sonores]
                - **[Outro & Conversion]** : [Appel à l'action stratégique]

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
                        st.success("🎉 Kit Studio Pro généré avec succès !")
                        
                        # Affichage du résultat dans une carte élégante
                        st.markdown(kit_genere)
                        
                        st.divider()
                        st.markdown("##### 📋 Exporter / Copier le Kit")
                        st.code(kit_genere, language="markdown")
                    else:
                        st.error(f"Erreur API : {result.get('error', {}).get('message', 'Erreur inconnue')}")
                except Exception as e:
                    st.error(f"Erreur de connexion : {e}")
    else:
        st.info("💡 **Prêt à créer ?** Renseignez vos critères à gauche et cliquez sur **Générer** pour obtenir votre kit complet.")
