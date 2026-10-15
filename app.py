import streamlit as st
from groq import Groq

# Configuration de la page
st.set_page_config(page_title="AutoClip AI", page_icon="🚀")
st.title("🚀 AutoClip AI")
st.caption("Générateur automatique de hooks et scripts viraux pour TikTok & Reels")

# Formulaire utilisateur
sujet = st.text_input("1. Quel est le sujet ou l'idée de ta vidéo ?", placeholder="ex: Mes conseils pour produire de la house music")
style = st.selectbox("2. Quel est le style / format ?", ["Éducatif / Conseil", "Storytelling", "Promotion Musique / Art", "Divertissement"])

# Bouton d'action
if st.button("Générer mon script viral 🔥"):
    if not sujet:
        st.warning("Pense à entrer un sujet avant de lancer la génération !")
    else:
        with st.spinner("L'IA prépare tes hooks et ton script..."):
            # Connexion à l'API Groq
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            
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
            
            completion = client.chat.completions.create(
            model="llama-3.1-8b-instant"
            messages=[{"role": "user", "content": prompt}]
        )
            
            # Affichage du résultat
            st.success("C'est prêt !")
            st.markdown(completion.choices[0].message.content)
