import streamlit as st
from groq import Groq
from fpdf import FPDF

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
# 3. MOTEUR EXPORT PDF COMPLET ET STRUCTURÉ
# ---------------------------------------------------------
class ScriptPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(220, 53, 69)
        self.cell(0, 8, 'AUTOCLIP AI - BIBLE DE PRODUCTION & SCRIPT', 0, 1, 'C')
        self.ln(3)

    def footer(self):
        self.set_y(-12)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 8, f'Page {self.page_no()}', 0, 0, 'C')

def generer_pdf_script(titre_video, contenu_markdown):
    pdf = ScriptPDF(orientation='P', unit='mm', format='A4')
    pdf.set_margins(left=10, top=10, right=10)
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    titre_propre = (titre_video or "Script_Video")\
        .replace('—', '-').replace('–', '-').replace('’', "'").replace('«', '"').replace('»', '"')
    titre_propre = titre_propre.encode('latin-1', 'replace').decode('latin-1')
    
    pdf.set_font("Helvetica", 'B', 11)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 6, f"Sujet : {titre_propre}")
    pdf.ln(3)
    
    largeur_utile = 190
    
    texte_nettoye = (contenu_markdown or "")\
        .replace('—', '-').replace('–', '-').replace('’', "'")\
        .replace('«', '"').replace('»', '"').replace('•', '*')\
        .replace('🎬', '').replace('📋', '').replace('🪝', '').replace('🔹', '')\
        .replace('🎯', '').replace('📈', '').replace('🤖', '').replace('✨', '')\
        .replace('🔥', '').replace('⚡', '').replace('💬', '').replace('⏱️', '')\
        .replace('<br>', '\n').replace('<b>', '').replace('</b>', '')
        
    lignes = texte_nettoye.split('\n')
    for ligne in lignes:
        ligne_propre = ligne.encode('latin-1', 'replace').decode('latin-1')
        
        if ligne.startswith('# '):
            pdf.set_font("Helvetica", 'B', 12)
            pdf.set_text_color(220, 53, 69)
            pdf.ln(3)
            pdf.multi_cell(largeur_utile, 6, ligne_propre.replace('# ', ''))
            pdf.set_text_color(0, 0, 0)
        elif ligne.startswith('## '):
            pdf.set_font("Helvetica", 'B', 10)
            pdf.set_text_color(40, 40, 40)
            pdf.ln(2)
            pdf.multi_cell(largeur_utile, 5, ligne_propre.replace('## ', ''))
            pdf.set_text_color(0, 0, 0)
        elif ligne.startswith('### '):
            pdf.set_font("Helvetica", 'B', 9)
            pdf.ln(2)
            pdf.multi_cell(largeur_utile, 5, ligne_propre.replace('### ', ''))
        else:
            pdf.set_font("Helvetica", size=8.5)
            if ligne.strip() == "":
                pdf.ln(2)
            else:
                pdf.multi_cell(largeur_utile, 4.5, ligne_propre)
            
    return bytes(pdf.output())

# ---------------------------------------------------------
# 4. BARRE LATÉRALE (SIDEBAR)
# ---------------------------------------------------------
with st.sidebar:
    st.title("🎬 AutoClip Studio")
    st.success("⚡ **Mode Studio Privé Actif**")
    st.divider()
    st.markdown("### 🎯 Objectif")
    st.write("Générez des scripts de haute rétention et téléchargez directement votre PDF complet et structuré pour vos clients.")

# ---------------------------------------------------------
# 5. INTERFACE PRINCIPALE DE CONFIGURATION DU SCRIPT
# ---------------------------------------------------------
st.title("🎬 AutoClip AI — Studio de Directing & Scripting Expert")
st.markdown("Renseignez les paramètres ci-dessous pour générer directement la bible de tournage et le script complet dans votre fichier PDF.")

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
# 6. GÉNÉRATION & TÉLÉCHARGEMENT EXCLUSIF EN PDF
# ---------------------------------------------------------
if st.button("🚀 Générer et Télécharger la Bible & le Script en PDF", type="primary", use_container_width=True):
    if not topic:
        st.warning("⚠️ Veuillez préciser le sujet exact de la vidéo.")
    else:
        prompt_template = """
        Tu es le Meilleur Directeur Artistique, Réalisateur Vidéo, Growth Hacker et Master Copywriter au Monde.
        Rédige un SCRIPT BIBLE EXHAUSTIF, HYPER CLAIR, NET, PRÉCIS ET COMPRÉHENSIBLE PAR UN CLIENT, SÉQUENCE PAR SÉQUENCE, AU MOT PRÈS (Personne physique en face-cam).
        NE SOIS PAS SYNTHÉTIQUE. DÉTAILLE TOUT. Rédige chaque réplique intégrale sans résumé ni '...'.
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

        Format de réponse exigé en Markdown clair, net et structuré :
        1. BIBLE DE PRODUCTION (Ambiance, Décor, Ton, Règles)
        2. ACCROCHE (0-3s avec mots exacts, intonation, texte écran)
        3. DECOUPAGE SEQUENCE PAR SEQUENCE (Minuté, répliques exactes au mot près, consignes visuelles)
        4. CONCLUSION & CALL TO ACTION
        5. LEGENDE / CAPTION & HASHTAGS VIRAUX
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

        with st.spinner("🎬 Production de la bible et compilation dans le PDF..."):
            try:
                response = groq_client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[{"role": "user", "content": prompt}]
                )
                script = response.choices[0].message.content

                pdf_data = generer_pdf_script(topic, script)
                
                st.success("✨ Le PDF complet a été généré avec succès !")
                st.download_button(
                    label="📥 Cliquer ici pour télécharger votre PDF de tournage",
                    data=pdf_data,
                    file_name=f"Script_Tournage_{topic.replace(' ', '_')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Erreur lors de la génération : {e}")
