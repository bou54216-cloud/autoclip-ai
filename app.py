import streamlit as st
import requests
import json

st.set_page_config(page_title="AutoClip AI", page_icon="🚀")
st.title("🚀 AutoClip AI")
st.caption("Générateur automatique de hooks et scripts viraux pour TikTok & Reels")

sujet = st.text_input("1. Quel est le sujet ou l'idée de ta vidéo ?", placeholder="ex: Mes conseils pour produire de la house viral")
style = st.selectbox("2. Quel est le style / format ?", ["Éducatif / Conseil", "Storytelling", "Promotion Musique / Art", "Divertissement"])

if st.button("Générer mon script viral 🔥"):
    if not sujet:
        st.warning("Pense à entrer un sujet avant de lancer la génération !")
    else:
        with st.spinner("L'IA prépare tes hooks et ton script..."):
            
            
            GROQ_API_KEY = "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"
            
            prompt = f"""
            Tu es un expert en marketing viral TikTok et Reels.
            Génère un contenu optimisé pour le sujet suivant : '{sujet}' (Style: {style}).
            
            Structure la réponse exactement comme ceci :
            ---
            ### 🪝 3 Hooks Accrocheurs (0-3 secondes)
            1. [Hook visuel + textuel 1]
            2. [Hook visuel + textuel 2]
            3. [Hook visuel + textuel 3]

            ### 📝 Script de la vidéo (15-30s)
            - **[00:00 - 00:03]** : [Action / Phrase]
            - **[00:03 - 00:10]** : [Corps du sujet / B-roll recommandé]
            - **[00:10 - 00:15]** : [Appel à l'action / Fin]

            ### 🏷️ 5 Hashtags stratégiques
            ---
            """
            
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "openai/gpt-oss-20b"
                "messages": [{"role": "user", "content": prompt}]
            }
            
            try:
                response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, data=json.dumps(payload))
                result = response.json()
                
                if response.status_code == 200:
                    script_genere = result["choices"][0]["message"]["content"]
                    st.success("C'est prêt !")
                    st.markdown(script_genere)
                else:
                    st.error(f"Erreur API Groq : {result.get('error', {}).get('message', 'Erreur inconnue')}")
            except Exception as e:
                st.error(f"Erreur de connexion : {e}")
