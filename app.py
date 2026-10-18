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
    st.success("⚡ **Mode Document Massif (Format 10 Pages)**")
    st.divider()
    st.markdown("### 🎯 Objectif")
    st.write("Générez un contenu ultra-approfondi en plusieurs blocs pour obtenir un dossier de tournage géant et complet.")

# ---------------------------------------------------------
# 4. INTERFACE PRINCIPALE DE CONFIGURATION
# ---------------------------------------------------------
st.title("🎬 AutoClip AI — Studio de Directing & Scripting Expert (Format Long)")
st.markdown("Renseignez les paramètres ci-dessous. Pour atteindre l'équivalent de 10 pages, générez la Partie 1 puis la Partie 2.")

st.divider()

col_part = st.columns(1)[0]
with col_part:
    partie_selectionnee = st.selectbox(
        "📄 Choisissez la partie du dossier à générer (pour un total de 10 pages) :",
        ["Partie 1 : Stratégie, Psychologie de la cible & Bible de tournage (Pages 1 à 5)", 
         "Partie 2 : Script mot-à-mot ultra-détaillé, Séquences & Kit Viral (Pages 6 à 10)"]
    )

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
# 5. GÉNÉRATION DU CONTENU EN FORMAT GÉANT
# ---------------------------------------------------------
if st.button("🚀 Générer cette partie du dossier massif", type="primary", use_container_width=True):
    if not topic:
        st.warning("⚠️ Veuillez préciser le sujet exact de la vidéo.")
    else:
        if "Partie 1" in partie_selectionnee:
            prompt = f"""
            Tu es le Directeur Artistique et Growth Hacker le plus exigeant au monde. Rédige la PREMIÈRE PARTIE (équivalent de 5 pages textuelles denses et rédigées) d'un dossier de production vidéo ultra-complet pour le client.
            Écris énormément de texte, développe chaque concept en profondeur, sans jamais faire court. Rédige de grands paragraphes d'analyse.
            Matériel 100% smartphone et lumière naturelle de fenêtre (pas de studio cher). Style 100% humain, naturel, sans jargon robotique.
            
            Sujet : {topic} | Marque : {brand_name or 'Non spécifié'} | Cible : {target_persona or 'Grand public'} | Frustration : {audience_frustration or 'Non spécifiée'} | Ton : {tone}

            STRUCTURE EXIGÉE POUR CETTE PARTIE 1 (Développe chaque point sur de longs paragraphes) :
            # DOSSIER DE PRODUCTION - PARTIE 1 : STRATÉGIE ET BIBLE DE TOURNAGE
            ## 1. Analyse approfondie de la cible et psychologie du prospect
            ## 2. Définition de l'angle marketing et de la promesse unique
            ## 3. Guide pratique du tournage au smartphone et gestion de la lumière naturelle à la maison
            ## 4. Habillage sonore, choix de la musique et accessoires visuels
            ## 5. Découpage stratégique et intention de chaque séquence de la vidéo
            """
        else:
            prompt = f"""
            Tu es le Directeur Artistique et Growth Hacker le plus exigeant au monde. Rédige la SECONDE PARTIE (équivalent de 5 pages textuelles denses et rédigées) d'un dossier de production vidéo ultra-complet pour le client.
            Écris énormément de texte, développe chaque réplique mot-à-mot sans aucun résumé ni point de suspension.
            Matériel 100% smartphone et lumière naturelle de fenêtre. Style 100% humain et naturel.

            Sujet : {topic} | Marque : {brand_name or 'Non spécifié'} | Accroche : {hook_style} | CTA : {cta_type} | Ton : {tone}

            STRUCTURE EXIGÉE POUR CETTE PARTIE 2 (Développe chaque point en détail) :
            # DOSSIER DE PRODUCTION - PARTIE 2 : SCRIPT MOT-À-MOT ET KIT DE PUBLICATION
            ## 1. L'Accroche décortiquée seconde par seconde (0 à 3s) : Posture, intonation et texte exact
            ## 2. Le Script intégral de la vidéo (Séquence par séquence, répliques complètes au mot près, actions et consignes de jeu d'acteur)
            ## 3. Appel à l'action (CTA) et stratégie de conversion finale
            ## 4. Kit de publication complet : Légende longue optimisée pour l'algorithme et sélection de hashtags
            ## 5. Lexique simple pour le client (Explication claire des termes de montage comme SFX ou Cut)
            """

        with st.spinner(f"🎬 Rédaction intensive du contenu (Format long)..."):
            try:
                response = groq_client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[{"role": "user", "content": prompt}]
                )
                script = response.choices[0].message.content

                st.success("✨ Partie générée avec succès ! Copie ce texte dans ton document, puis sélectionne l'autre partie pour compléter ton dossier de 10 pages.")
                
                # Zone de texte large et propre avec bouton de copie intégré
                st.code(script, language="markdown")

            except Exception as e:
                st.error(f"Erreur lors de la génération : {e}")
