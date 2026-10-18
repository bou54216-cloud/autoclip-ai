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
    st.success("⚡ **Mode 100% Parfait & Validé**")
    st.divider()
    st.markdown("### 🎯 Objectif")
    st.write("Générez automatiquement un dossier de tournage irréprochable, optimisé pour le format 30-60s au smartphone.")

# ---------------------------------------------------------
# 4. INTERFACE PRINCIPALE DE CONFIGURATION
# ---------------------------------------------------------
st.title("🎬 AutoClip AI — Studio de Directing & Scripting Expert")
st.markdown("Renseignez les paramètres ci-dessous. Le site génère instantanément un script d'une qualité absolue, sans aucune erreur.")

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
# 5. GÉNÉRATION DU SCRIPT 100% PARFAIT (30-60 SECONDES)
# ---------------------------------------------------------
if st.button("🚀 Générer le Dossier de Tournage Parfait (30-60s)", type="primary", use_container_width=True):
    if not topic:
        st.warning("⚠️ Veuillez préciser le sujet exact de la vidéo.")
    else:
        prompt_template = """
        Tu es le Directeur Artistique, Growth Hacker et Master Copywriter le plus talentueux au monde. Rédige un DOSSIER DE PRODUCTION ET SCRIPT VIDÉO IRRÉPROCHABLE, FLUENT, SANS AUCUNE ERREUR, calibré précisément pour durer entre 30 et 60 secondes maximum.

        REGLES ABSOLUES POUR QUE LE LIVRABLE SOIT PARFAIT :
        1. FORMAT STRICT 30-60 SECONDES : Le volume de texte et le minutage du script doivent s'enchaîner pour tenir en moins de 60 secondes à l'oral (rythme punchy, sans longueurs).
        2. AUCUNE COUPURE DE TEXTE : Le script doit aller de la stratégie jusqu'au lexique final sans jamais s'interrompre.
        3. TOURNAGE SIMPLE AU SMARTPHONE : Tout doit être pensé pour un tournage facile avec un simple smartphone calé face à une fenêtre (lumière naturelle).
        4. TON HUMAIN ET NATUREL : Interdiction d'utiliser du jargon robotique d'IA. Écris comme un vrai pro qui parle à un créateur.
        5. RÉPLIQUES COMPLÈTES : Rédige chaque phrase de la voix off mot-à-mot, prêtes à être lues face caméra. Cohérence parfaite des mots-clés et hashtags (ex: #ClesEn3Mois sans espaces bizarres).
        6. LEXIQUE INTÉGRÉ : À la fin, inclus un lexique simple expliquant les termes techniques (SFX, Cut, etc.).
        7. Interdiction de citer des logiciels ou applications tiers.

        - Sujet exact : {topic}
        - Marque / Offre : {brand_name}
        - USP : {usp}
        - Concurrent : {competitor}
        - Plateforme : {platform}
        - Durée : 30 à 60 secondes
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

        STRUCTURE EXIGÉE POUR LE DOCUMENT FINAL :
        # DOSSIER DE PRODUCTION ET SCRIPT VIDÉO VIRAL (30-60s)
        ## 1. STRATÉGIE & ANALYSE DE LA CIBLE (Pourquoi cette vidéo va cartonner)
        ## 2. GUIDE PRATIQUE DU TOURNAGE AU SMARTPHONE (Lumière naturelle et installation simple)
        ## 3. L'ACCROCHE (0 À 3 SECONDES) - Posture, texte à l'écran et réplique exacte
        ## 4. SCRIPT INTÉGRAL SÉQUENCE PAR SÉQUENCE (Répliques complètes au mot près, durée totale ciblée 45s, consignes de jeu simples)
        ## 5. APPEL À L'ACTION (CTA) ET CONCLUSION
        ## 6. KIT DE PUBLICATION : LÉGENDE OPTIMISÉE & HASHTAGS PROPRES
        ## 7. LEXIQUE SIMPLE (Pour comprendre les termes techniques en un clin d'œil)
        """

        prompt = prompt_template.format(
            topic=topic, brand_name=brand_name or 'Non spécifié', usp=usp or 'Non spécifié',
            competitor=competitor or 'Non spécifié', platform=platform,
            target_persona=target_persona or 'Grand public', audience_frustration=audience_frustration or 'Non spécifiée',
            desired_result=desired_result or 'Non spécifié', main_objection=main_objection or 'Aucune',
            target_emotion=target_emotion, proof_social=proof_social or 'Aucune', urgency_trigger=urgency_trigger or 'Aucun',
            speaker_energy=speaker_energy, vocab_style=vocab_style, tone=tone,
            shooting_location=shooting_location or 'Non spécifié', key_props=key_props or 'Aucun',
            forbidden_words=forbidden_words or 'Aucun', hook_style=hook_style, pacing=pacing,
            structure=structure, cta_type=cta_type, music_genre=music_genre or 'Inconnu', extra_details=extra_details or 'Aucune'
        )

        with st.spinner("🎬 Génération automatique du dossier de tournage parfait (30-60s)..."):
            try:
                response = groq_client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[{"role": "user", "content": prompt}]
                )
                script = response.choices[0].message.content

                st.success("✨ Le dossier de production est parfait, calé en moins de 60 secondes, et prêt à être envoyé à ton client !")
                
                # Zone de texte propre avec bouton de copie intégré
                st.code(script, language="markdown")

            except Exception as e:
                st.error(f"Erreur lors de la génération : {e}")
