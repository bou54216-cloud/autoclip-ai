import streamlit as st
import requests
import json

st.set_page_config(page_title="AutoClip AI", page_icon="🚀")
st.title("🚀 AutoClip AI")
st.caption("Générateur automatique de hooks et scripts viraux pour TikTok & Reels")

sujet = st.text_input("1. Quel est le sujet ou l'idée de ta vidéo ?", placeholder="ex: Mes conseils pour produire de la house viral")
style = st.selectbox("2. Quel est le style / format ?", ["Éducatif / Conseil", "Storytelling", "Promotion Musique / Art", "Divertissement"])
ton = st.selectbox("3. Quel est le ton souhaité ?", ["Énergique & Rythmé", "Humoristique & Décalé", "Cash & Direct", "Professionnel & Inspirant"])

# Menu déroulant complet avec toutes les durées
duree = st.selectbox(
    "4. Quelle est la durée souhaitée de ta vidéo ?", 
    ["15 secondes", "30 secondes", "45 secondes", "1 minute", "1 minute 30 secondes"]
)

if st.button("Générer mon script viral 🔥"):
    if not sujet:
        st.warning("Pense à entrer un sujet avant de lancer la génération !")
    else:
        with st.spinner(f"L'IA prépare ton script personnalisé de {duree}..."):
            
            GROQ_API_KEY = "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"
            
            prompt = f"""
            Tu es un expert en marketing viral TikTok et Reels.
            Génère un script vidéo complet d'une durée exacte de {duree} sur le sujet suivant : '{sujet}' (Style: {style}, Ton: {ton}).
            
            Structure la réponse exactement comme ceci :
            ---
            ### 🪝 1. L'Accroche (0 - 5 secondes)
            - **Visuel & Texte à l'écran** : [Ce qu'on voit et le texte écrit]
            - **Ce que tu dis** : [La phrase choc pour stopper le scroll]

            ### 🧱 2. Le Développement (Adapté pour tenir exactement en {duree})
            - **Visuel** : [Exemple de plan B-roll / Illustration]
            - **Ce que tu dis** : [Le contenu structuré pour correspondre à cette durée]

            ### 🎯 3. L'Appel à l'Action / Outro
            - **Visuel** : [Retour caméra]
            - **Ce que tu dis** : [Invitation à s'abonner, commenter ou agir]

            ### 🏷️ 4. 5 Hashtags stratégiques
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
                    script_genere = result["choices"][0]["message"]["content"]
                    st.success("C'est prêt !")
                    st.markdown(script_genere)
                    
                    st.markdown("### 📋 Copier ton script")
                    st.code(script_genere, language="markdown")
                else:
                    st.error(f"Erreur API Groq : {result.get('error', {}).get('message', 'Erreur inconnue')}")
            except Exception as e:
                st.error(f"Erreur de connexion : {e}")
