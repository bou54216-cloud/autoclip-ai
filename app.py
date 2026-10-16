import streamlit as st
import requests
import json

st.set_page_config(page_title="AutoClip AI", page_icon="🚀")
st.title("🚀 AutoClip AI")
st.caption("Générateur automatique de hooks et scripts viraux pour TikTok & Reels (Format 1 Minute)")

sujet = st.text_input("1. Quel est le sujet ou l'idée de ta vidéo ?", placeholder="ex: Mes conseils pour produire de la house viral")
style = st.selectbox("2. Quel est le style / format ?", ["Éducatif / Conseil", "Storytelling", "Promotion Musique / Art", "Divertissement"])
ton = st.selectbox("3. Quel est le ton souhaité ?", ["Énergique & Rythmé", "Humoristique & Décalé", "Cash & Direct", "Professionnel & Inspirant"])

if st.button("Générer mon script de 1 minute 🔥"):
    if not sujet:
        st.warning("Pense à entrer un sujet avant de lancer la génération !")
    else:
        with st.spinner("L'IA prépare ton script complet de 60 secondes..."):
            
            GROQ_API_KEY = "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"
            
            # Prompt optimisé pour un script d'une minute bien structuré
            prompt = f"""
            Tu es un expert en marketing viral TikTok et Reels.
            Génère un script vidéo complet d'une durée d'exactement 1 minute (environ 130 à 150 mots) sur le sujet suivant : '{sujet}' (Style: {style}, Ton: {ton}).
            
            Structure la réponse exactement comme ceci :
            ---
            ### 🪝 1. L'Accroche (0 - 5 secondes)
            - **Visuel & Texte à l'écran** : [Ce qu'on voit et le texte écrit]
            - **Ce que tu dis** : [La phrase choc pour stopper le scroll]

            ### 🧱 2. Le Problème ou le Contexte (5 - 20 secondes)
            - **Visuel** : [Exemple de plan B-roll]
            - **Ce que tu dis** : [Expliquer le problème ou introduire le sujet en détail]

            ### 💡 3. La Valeur / La Solution (20 - 45 secondes)
            - **Visuel** : [Démonstration ou explication claire]
            - **Ce que tu dis** : [Donner les conseils clés de manière très claire et compréhensible]

            ### 🎯 4. L'Appel à l'Action / Outro (45 - 60 secondes)
            - **Visuel** : [Retour caméra]
            - **Ce que tu dis** : [Ce qu'on invite l'abonné à faire, ex: s'abonner, commenter, tester]

            ### 🏷️ 5 Hashtags stratégiques
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
