import streamlit as st
import requests
import json

# Configuration de la page
st.set_page_config(
    page_title="AutoClip AI - Studio Créateur Pro",
    page_icon="⚡",
    layout="wide"
)

# Style CSS personnalisé pour moderniser l'interface
st.markdown("""
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1E88E5;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1rem;
        color: #666;
        margin-bottom: 25px;
    }
    .stButton>button {
        width: 100%;
        background-color: #1E88E5;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 12px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #1565C0;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">⚡ AutoClip AI — Studio Créateur Pro</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Générateur automatique de scripts, hooks & kits réseaux optimisés pour l\'humain et l\'IA.</p>', unsafe_allow_html=True)

# Disposition en 2 colonnes : Gauche = Paramètres, Droite = Résultats
col_left, col_right = st.columns([1, 1.2], gap="large")

with col_left:
    st.subheader("⚙️ Configuration de la Vidéo")
    
    sujet = st.text_input("1. Sujet / Idée principale", placeholder="ex: Mes 3 astuces pour produire un synthé House")
    
    col1, col2 = st.columns(2)
    with col1:
        plateforme = st.selectbox("2. Plateforme", ["TikTok", "Instagram Reels", "YouTube Shorts"])
        style = st.selectbox("3. Style / Format", ["Éducatif / Conseil", "Storytelling", "Promotion Musique / Art", "Divertissement"])
    with col2:
        ton = st.selectbox("4. Ton souhaité", ["Énergique & Rythmé", "Humoristique & Décalé", "Cash & Direct", "Professionnel & Inspirant"])
        duree = st.selectbox("5. Durée estimée", ["15 secondes", "30 secondes", "45 secondes", "1 minute", "1 minute 30 secondes"])
    
    methode = st.selectbox(
        "6. Méthode de production", 
        [
            "Tournage humain (Je me filme / face caméra)", 
            "IA Text-to-Video (InVideo / CapCut Script-to-Video)"
        ]
    )
    
    # --- NOUVEAU : Option Musique / Synchronisation sonore ---
    ambiance_musique = st.text_input(
        "7. Ambiance sonore / Musique (Optionnel)", 
        placeholder="ex: House dynamic beat, Bassline percutante, Chill synthwave..."
    )
    
    btn_generer = st.button("🚀 Générer mon Kit Vidéo Complet")

with col_right:
    st.subheader("📌 Ton Kit Créateur")
    
    if btn_generer:
        if not sujet:
            st.warning("⚠️ Merci d'entrer un sujet avant de lancer la génération !")
        else:
            with st.spinner("⚡ L'IA génère ton kit structuré et synchronisé..."):
                
                GROQ_API_KEY = "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"
                
                instructions_methode = (
                    "Le script doit être rédigé pour une personne face caméra avec indications de jeu et de visuels."
                    if "Tournage humain" in methode else
                    "Le script doit être ultra-descriptif et prêt à être collé dans un générateur IA vidéo (InVideo/CapCut)."
                )
                
                instruction_musique = f"Intègre des indications de rythme et de synchro sonore basées sur cette musique/ambiance : '{ambiance_musique}' (ex: drop de basse, baisse de son, changement de plan au beat)." if ambiance_musique else ""

                prompt = f"""
                Tu es un expert en marketing digital et création de contenu viral sur {plateforme}.
                Génère un kit vidéo complet de {duree} sur le sujet : '{sujet}' (Style: {style}, Ton: {ton}).
                
                Instructions spécifiques :
                - {instructions_methode}
                - {instruction_musique}
                
                Structure ta réponse exactement ainsi :
                
                ### 🎬 1. Titres & Textes Thumbnail
                - **Titre 1** : [Proposition 1]
                - **Titre 2** : [Proposition 2]
                - **Texte Couverture** : [3-4 mots max]

                ### 🪝 2. Script Vidéo Détaillé ({duree})
                - **[00:00 - 00:05] Accroche** : [Visuel + Phrase choc + Synchro son]
                - **[Développement]** : [Plan par plan avec visuels B-roll, paroles et gestion du son/drop]
                - **[Outro]** : [Appel à l'action clair]

                ### 📝 3. Description & Hashtags SEO
                - **Description** : [Texte captivant avec question d'engagement]
                - **Hashtags** : [5-8 hashtags stratégiques]
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
                        st.success("✨ Kit généré avec succès !")
                        st.markdown(kit_genere)
                        
                        st.divider()
                        st.markdown("### 📋 Copier le contenu")
                        st.code(kit_genere, language="markdown")
                    else:
                        st.error(f"Erreur API Groq : {result.get('error', {}).get('message', 'Erreur inconnue')}")
                except Exception as e:
                    st.error(f"Erreur de connexion : {e}")
    else:
        st.info("👈 Remplis les informations à gauche et clique sur **Générer** pour afficher ton kit complet ici.")
