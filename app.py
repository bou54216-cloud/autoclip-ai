import streamlit as st
from groq import Groq

# ---------------------------------------------------------
# 1. CONFIGURATION PAGE ET DESIGN CSS
# ---------------------------------------------------------
st.set_page_config(
    page_title="AutoClip Studio — Production de Scripts Vidéo",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp { background-color: #0E1117; }
    div[data-testid="stVerticalBlock"] > div { border-radius: 10px; }
    .stButton>button { border-radius: 8px; font-weight: 600; transition: all 0.3s ease; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. INITIALISATION GROQ API
# ---------------------------------------------------------
@st.cache_resource
def init_groq():
    return Groq(api_key=st.secrets["GROQ_API_KEY"])

groq_client = init_groq()

# ---------------------------------------------------------
# 3. BARRE LATÉRALE (SIDEBAR)
# ---------------------------------------------------------
with st.sidebar:
    st.title("🎬 AutoClip Studio")
    st.success("⚡ **Mode Texte Simple & Accessible Actif**")
    st.divider()
    st.markdown("### 🎯 Objectif")
    st.write("Générez un script ultra-clair, sans jargon technique, prêt à être copié pour vos clients.")

# ---------------------------------------------------------
# 4. INTERFACE PRINCIPALE DE CONFIGURATION
# ---------------------------------------------------------
st.title("🎬 AutoClip AI — Studio de Directing & Scripting Expert")
st.markdown("Renseignez les paramètres ci-dessous pour générer un script 100 % compréhensible, sans termes techniques complexes.")

st.divider()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.subheader("1. Concept & Marque")
    topic = st.text_input("🎯 Sujet exact de la vidéo :", placeholder="ex: Comment négocier son prêt immobilier")
    brand_name = st.text_input("🏷️ Nom de la Marque / Produit :", placeholder="ex: Immobiz...")
    usp = st.text_input("⚡ Élément différenciateur (USP) :", placeholder="ex: Méthode sans apport")
    competitor = st.text_input("🥊 Concurrent direct à cibler :", placeholder="ex: Les banques traditionnelles...")
    platform = st.selectbox("📱 Plateforme cible :", ["TikTok", "Instagram Reels", "YouTube Shorts", "LinkedIn Video"])
    duration = st.selectbox("⏱️ Durée visée :", ["Flash (15 - 30 sec)", "Standard Short (30 - 60 sec)", "Long Short (60 - 90 sec)"])

with col2:
    st.subheader("2. Cible & Psychologie")
    target_persona = st.text_input("👥 Audience Cible (Persona) :", placeholder="ex: Primo-accédants...")
    audience_frustration = st.text_input("💢 Frustration / Problème actuel :", placeholder="ex: Refus de prêt...")
    desired_result = st.text_input("✨ Résultat rêvé du prospect :", placeholder="ex: Obtenir les clés en 3 mois")
    main_objection = st.text_input("🛑 Objection majeure :", placeholder="ex: 'Je n'ai pas assez d'épargne'")
    target_emotion = st.selectbox("🔥 Émotion clé à provoquer :", ["Curiosité & Choc", "Peur de rater (FOMO)", "Espoir & Inspiration", "Indignation / Colère"])
    proof_social = st.text_input("🏆 Preuve Sociale / Chiffre clé :", placeholder="ex: +150 dossiers acceptés")

with col3:
    st.subheader("3. Rétention & Style")
    hook_style = st.selectbox("🪝 Type d'accroche (Hook 0-3s) :", ["Question choc / Provocation", "Statistique / Chiffre dingue", "Mise en garde / Erreur grave", "Scénario 'Imagine si...'"])
    pacing = st.selectbox("⚡ Rythme de montage :", ["Ultra-rapide (Cuts dynamiques + SFX)", "Modéré & Captivant (Rythme fluide)", "Analytique & Posé"])
    structure = st.selectbox("🏗️ Framework narratif :", ["PAS (Problème -> Agitation -> Solution)", "3 Piliers / Astuces pas-à-pas", "Avant / Après (Transformation)"])
    tone = st.selectbox("🎭 Ambiance & Énergie :", ["Dynamique & Énergique", "Cash, Provocateur & Sans Filtre", "Éducatif, Clair & Expert"])
    speaker_energy = st.selectbox("🎙️ Style de personnalité :", ["Calme, Posé & Rassurant", "Enthousiaste, Énergique & Motivant", "Direct, Brut & Sans langue de bois"])
    vocab_style = st.selectbox("💬 Registre de langage :", ["Accessible & Courant", "Technique & Expert", "Cash & Codes Réseaux"])

with col4:
    st.subheader("4. Conversion & Tournage")
    cta_type = st.selectbox("🎯 Call To Action (CTA) :", ["Commenter un mot-clé", "S'abonner pour la partie 2", "Cliquer sur le lien en bio", "Enregistrer & Partager"])
    urgency_trigger = st.text_input("⏳ Levier d'urgence :", placeholder="ex: Offre valable jusqu'à dimanche")
    shooting_location = st.text_input("🏠 Décor / Lieu de tournage :", placeholder="ex: Bureau moderne, extérieur...")
    key_props = st.text_input("🎬 Accessoire visuel :", placeholder="ex: Tenir des clés, un contrat...")
    forbidden_words = st.text_input("🚫 Mots interdits :", placeholder="ex: argent facile...")
    music_genre = st.text_input("🎵 Ambiance Sonore :", placeholder="ex: Musique dynamique...")
    extra_details = st.text_area("⚙️ Consignes Spécifiques :", placeholder="ex: Insérer un graphique...")

st.divider()

# ---------------------------------------------------------
# 5. GÉNÉRATION DU SCRIPT SANS JARGON TECHNIQUE
# ---------------------------------------------------------
if st.button("🚀 Générer le Script Accessible au Client", type="primary", use_container_width=True):
    if not topic:
        st.warning("⚠️ Veuillez préciser le sujet exact de la vidéo.")
    else:
        prompt_template = """
        Tu es le Meilleur Directeur Artistique et Master Copywriter au Monde.
        Rédige un SCRIPT VIDÉO ET UNE BIBLE DE TOURNAGE conçus spécifiquement pour un client grand public. 
        REGLE ABSOLUE : INTERDICTION TOTALE D'UTILISER DU JARGON TECHNIQUE DE MONTAGE OU DU CINÉMA (interdit d'utiliser les termes 'SFX', 'cut', 'cut dynamique', 'jump cut', 'étalonnage', 'sound design', 'script', etc.). 
        Utilise à la place des mots simples que tout le monde comprend (ex: au lieu de 'SFX crack', écris 'Bruitage sonore de craquement' ; au lieu de 'cut rapide', écris 'Changement rapide d'image').
        Rédige chaque réplique intégrale au mot près, sans résumé ni '...'.
        NE CITE AUCUN NOM D'APPLICATION NI DE LOGICIEL TIERS.

        - Sujet exact : {topic}
        - Marque / Offre : {brand_name}
        - USP : {usp}
        - Concurrent : {competitor}
        - Plateforme : {platform}
        - Durée : {duration}
        - Persona : {target_persona}
        - Frustration : {audience_frustration}
        - Résultat rêvé : {desired_result}
        - Objection : {main_objection}
        - Émotion : {target_emotion}
        - Preuve sociale : {proof_social}
        - Urgence : {urgency_trigger}
        - Énergie du créateur : {speaker_energy}
        - Langage : {vocab_style}
        - Ton : {tone}
        - Décor : {shooting_location}
        - Accessoires : {key_props}
        - Mots interdits : {forbidden_words}
        - Hook : {hook_style}
        - Rythme : {pacing}
        - Structure : {structure}
        - CTA : {cta_type}
        - Musique : {music_genre}
        - Consignes : {extra_details}

        Format de réponse exigé en Markdown clair, simple et 100% accessible :
        # GUIDE DE TOURNAGE POUR LA VIDEO
        ## 1. AMBIANCE ET DECOR
        ## 2. LA PHRASE D'ACCROCHE (Les 3 premières secondes)
        ## 3. CE QU'IL FAUT DIRE ET FAIRE (Séquence par séquence avec des mots simples)
        ## 4. COMMENT TERMINER LA VIDEO (Appel à l'action)
        ## 5. TEXTE À ÉCRIRE SOUS LA VIDÉO (Légende et hashtags)
        """

        prompt = prompt_template.format(
            topic=topic, brand_name=brand_name or 'Non spécifié', usp=usp or 'Non spécifié',
            competitor=competitor or 'Non spécifié', platform=platform, duration=duration,
            target_persona=target_persona or 'Grand public', audience_frustration=audience_frustration or 'Non spécifiée',
            desired_result=desired_result or 'Non spécifié', main_objection=main_objection or 'Aucune',
            target_emotion=target_emotion, proof_social=proof_social or 'Aucune', urgency_trigger=urgency_trigger or 'Aucun',
            speaker_energy=speaker_energy, vocab_style=vocab_style, tone=tone,
            shooting_location=shooting_location or 'Non spécifié', key_props=key_props or 'Aucun',
            forbidden_words=forbidden_words or 'Aucun', hook_style=hook_style, pacing=pacing,
            structure=structure, cta_type=cta_type, music_genre=music_genre or 'Inconnu', extra_details=extra_details or 'Aucune'
        )

        with st.spinner("🎬 Rédaction d'un script simple et compréhensible par tous..."):
            try:
                response = groq_client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[{"role": "user", "content": prompt}]
                )
                script = response.choices[0].message.content

                st.success("✨ Script généré avec succès ! Aucun terme technique n'est présent, c'est parfaitement clair pour ton client :")
                
                # Zone de texte propre avec bouton de copie intégré
                st.code(script, language="markdown")

            except Exception as e:
                st.error(f"Erreur lors de la génération : {e}")
