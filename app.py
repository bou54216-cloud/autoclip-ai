import streamlit as st
import requests
import json

st.set_page_config(page_title="AutoClip AI Pro", page_icon="🚀")
st.title("🚀 AutoClip AI - Studio Créateur Pro")
st.caption("Générateur tout-en-un optimisé pour l'humain ou l'IA !")

# Entrées utilisateur
sujet = st.text_input("1. Quel est le sujet ou l'idée de ta vidéo ?", placeholder="ex: Mes conseils pour produire de la house viral")
plateforme = st.selectbox("2. Sur quelle plateforme vas-tu publier ?", ["TikTok", "Instagram Reels", "YouTube Shorts"])
style = st.selectbox("3. Quel est le style / format ?", ["Éducatif / Conseil", "Storytelling", "Promotion Musique / Art", "Divertissement"])
ton = st.selectbox("4. Quel est le ton souhaité ?", ["Énergique & Rythmé", "Humoristique & Décalé", "Cash & Direct", "Professionnel & Inspirant"])
duree = st.selectbox("5. Quelle est la durée souhaitée de ta vidéo ?", ["15 secondes", "30 secondes", "45 secondes", "1 minute", "1 minute 30 secondes"])

# --- NOUVEAU : Choix de la méthode de création ---
methode = st.selectbox(
    "6. Comment vas-tu créer cette vidéo ?", 
    [
        "Tournage humain (Je me filme / face caméra)", 
        "IA Text-to-Video (Pour InVideo / CapCut Script-to-Video)"
    ]
)

if st.button("Générer mon kit complet de vidéo 🔥"):
    if not sujet:
        st.warning("Pense à entrer un sujet avant de lancer la génération !")
    else:
        with st.spinner(f"L'intelligence artificielle prépare ton kit adapté pour : {methode}..."):
            
            GROQ_API_KEY = "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"
            
            # Adaptation du prompt selon la méthode choisie
            instructions_methode = ""
            if "Tournage humain" in methode:
                instructions_methode = "Le script doit être rédigé pour une personne qui se filme elle-même, avec des indications précises de mise en scène, de texte à l'écran et de ton à adopter face caméra."
            else:
                instructions_methode = "Le script doit être ultra-descriptif et structuré pour être copié-collé directement dans une IA de génération vidéo (comme InVideo ou CapCut). Inclus des descriptions claires des visuels et des scènes à générer par l'IA pour chaque passage."

            prompt = f"""
            Tu es un expert en marketing digital et en création de contenu viral pour {plateforme}.
            Génère un kit complet pour une vidéo de {duree} sur le sujet suivant : '{sujet}' (Style: {style}, Ton: {ton}).
            Méthode de production choisie : {instructions_methode}
            
            Structure ta réponse exactement avec les sections suivantes :
            
            ### 🎬 1. Idées de Titres & Textes pour la Miniature (Thumbnail)
            - 3 propositions de titres accrocheurs pour {plateforme}
            - 1 texte court (3-4 mots max) à afficher directement sur la miniature / couverture de la vidéo.

            ### 🪝 2. Le Script Vidéo Structuré ({duree})
            - **L'Accroche (0 - 5s)** : Visuel, texte à l'écran et phrase choc.
            - **Le Développement** : Le contenu structuré pour tenir exactement en {duree}.
            - **L'Appel à l'Action / Outro** : Invitation claire à interagir.

            ### 📝 3. Description & Hashtags SEO
            - Une description engageante optimisée pour le référencement (SEO) avec une question pour inciter aux commentaires.
            - 5 à 8 hashtags ultra-pertinents et ciblés.
            ---
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
                    st.success("Ton kit complet est prêt !")
                    st.markdown(kit_genere)
                    
                    st.markdown("### 📋 Copier tout le kit")
                    st.code(kit_genere, language="markdown")
                else:
                    st.error(f"Erreur API Groq : {result.get('error', {}).get('message', 'Erreur inconnue')}")
            except Exception as e:
                st.error(f"Erreur de connexion : {e}")
