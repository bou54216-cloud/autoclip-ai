import streamlit as st
from groq import Groq
from fpdf import FPDF

# ---------------------------------------------------------
# 1. CONFIGURATION PAGE ET DESIGN CSS
# ---------------------------------------------------------
st.set_page_config(
    page_title="AutoClip Studio — Production & Brief Client",
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
# 3. MOTEURS PDF (SCRIPT & BRIEF CLIENT)
# ---------------------------------------------------------
class ScriptPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(220, 53, 69)
        self.multi_cell(0, 10, 'AUTOCLIP AI - BIBLE DE TOURNAGE & SCRIPT', align='C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

def generer_pdf_script(titre_video, contenu_markdown):
    pdf = ScriptPDF()
    pdf.set_margins(left=15, top=15, right=15)
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    titre_propre = (titre_video or "Script_Video").replace('—', '-').replace('–', '-').replace('’', "'").replace('«', '"').replace('»', '"')
        
    pdf.set_font("Helvetica", 'B', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 8, f"Sujet : {titre_propre}")
    pdf.ln(5)
    
    lignes = contenu_markdown.split('\n')
    for ligne in lignes:
        ligne_nettoyee = (ligne or "").replace('—', '-').replace('–', '-').replace('’', "'").replace('«', '"').replace('»', '"').replace('•', '*')
        ligne_propre = ligne_nettoyee.encode('latin-1', 'replace').decode('latin-1')
        
        if ligne.startswith('# '):
            pdf.set_font("Helvetica", 'B', 14)
            pdf.multi_cell(0, 10, ligne_propre.replace('# ', ''))
        elif ligne.startswith('## '):
            pdf.set_font("Helvetica", 'B', 12)
            pdf.multi_cell(0, 8, ligne_propre.replace('## ', ''))
        elif ligne.startswith('### '):
            pdf.set_font("Helvetica", 'B', 10)
            pdf.multi_cell(0, 6, ligne_propre.replace('### ', ''))
        else:
            pdf.set_font("Helvetica", size=9)
            pdf.multi_cell(0, 5, ligne_propre)
            
    return bytes(pdf.output())


class ClientBriefPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 10, 'CAHIER DES CHARGES - BRIEF VIDEO CLIENT', align='C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

def generer_pdf_brief_client(data):
    pdf = ClientBriefPDF()
    pdf.set_margins(left=15, top=15, right=15)
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    sections = [
        ("INFORMATIONS GENERALES", [
            ("Nom de la marque ou du projet", data.get("brand_name")),
            ("Sujet principal de la video", data.get("topic")),
            ("Duree souhaitee de la video", data.get("duration")),
            ("Plateforme de diffusion", data.get("platform")),
        ]),
        ("OBJECTIFS ET CIBLE", [
            ("Audience cible (A qui s'adresse la video ?)", data.get("target_persona")),
            ("Probleme ou frustration principale du client", data.get("audience_frustration")),
            ("Element unique ou avantage cle (USP)", data.get("usp")),
            ("Action attendue du spectateur (Appel a l'action)", data.get("cta_type")),
        ])
    ]
    
    for section_title, fields in sections:
        pdf.set_font("Helvetica", 'B', 11)
        pdf.set_text_color(180, 40, 40)
        pdf.multi_cell(0, 8, section_title)
        pdf.set_text_color(0, 0, 0)
        
        for label, val in fields:
            val_str = str(val) if val else "Non renseigne"
            clean_str = val_str.replace('—', '-').replace('–', '-').replace('’', "'").replace('«', '"').replace('»', '"')
            clean_str = clean_str.encode('latin-1', 'replace').decode('latin-1')
            
            pdf.set_font("Helvetica", 'B', 9)
            pdf.write(5, f"- {label} :\n  ")
            pdf.set_font("Helvetica", size=9)
            pdf.multi_cell(0, 5, f"  {clean_str}\n")
        pdf.ln(3)
        
    return bytes(pdf.output())

# ---------------------------------------------------------
# 4. NAVIGATION ENTRE LES MODULES (SIDEBAR)
# ---------------------------------------------------------
with st.sidebar:
    st.title("🎬 AutoClip Studio")
    st.success("⚡ **Mode Studio Privé Actif**")
    st.divider()
    app_mode = st.radio("Navigation", ["Générateur de Script & Bible", "Générateur de Brief Client (PDF)"])
    st.divider()
    st.markdown("### 💡 Astuce")
    st.write("Utilisez le **Brief Client** pour générer un PDF propre à envoyer à vos clients, puis utilisez le **Générateur de Script** pour produire la vidéo finale.")

# =========================================================
# MODULE 1 : GÉNÉRATEUR DE SCRIPT & BIBLE DE TOURNAGE
# =========================================================
if app_mode == "Générateur de Script & Bible":
    st.title("🎬 AutoClip AI — Studio de Directing & Scripting Expert")
    st.markdown("Remplissez ce questionnaire pour générer une bible de production complète, les hashtags viraux et la description optimisée.")

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

    if st.button("🚀 Générer le Plan de Production & Script d'Élite", type="primary", use_container_width=True):
        if not topic:
            st.warning("⚠️ Veuillez préciser le sujet exact de la vidéo.")
        else:
            prompt_template = """
            Tu es le Meilleur Directeur Artistique, Réalisateur Vidéo, Growth Hacker et Master Copywriter au Monde.
            Rédige un SCRIPT BIBLE EXHAUSTIF, HYPER LONG, DÉTAILLÉ SÉQUENCE PAR SÉQUENCE, AU MOT PRÈS (Personne physique en face-cam).
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

            Format de réponse exigé en Markdown d'Élite (Bible de production, Hook, Séquence par séquence minutée, CTA, Hashtags viraux, Script complet).
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

            with st.spinner("🎬 Production du script d'élite et de la bible..."):
                try:
                    response = groq_client.chat.completions.create(
                        model="openai/gpt-oss-120b",
                        messages=[{"role": "user", "content": prompt}]
                    )
                    script = response.choices[0].message.content

                    st.success("✨ Script généré avec succès !")
                    st.markdown(script)

                    pdf_data = generer_pdf_script(topic, script)
                    st.download_button(
                        label="📄 Télécharger le Script & Bible de Tournage en PDF",
                        data=pdf_data,
                        file_name=f"Script_{topic.replace(' ', '_')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"Erreur lors de la génération : {e}")

# =========================================================
# MODULE 2 : GÉNÉRATEUR DE BRIEF CLIENT (PDF SIMPLIFIÉ)
# =========================================================
elif app_mode == "Générateur de Brief Client (PDF)":
    st.title("📄 Générateur de Brief Client Simplifié")
    st.markdown("Remplissez rapidement les informations ci-dessous pour générer un PDF propre, sans émoji, à envoyer directement à votre client.")

    st.divider()

    with st.form("form_brief_client"):
        st.subheader("1. Informations Générales")
        brand_name = st.text_input("Nom de la marque ou du projet :", placeholder="ex: Nom de votre entreprise")
        topic = st.text_input("Sujet principal de la vidéo :", placeholder="ex: Présenter notre nouveau service")
        duration = st.text_input("Durée souhaitée de la vidéo :", placeholder="ex: 45 secondes / 1 minute")
        platform = st.selectbox("Plateforme de diffusion principale :", ["TikTok", "Instagram Reels", "YouTube Shorts", "LinkedIn", "Autre"])

        st.divider()

        st.subheader("2. Objectifs et Cible")
        target_persona = st.text_input("À qui s'adresse cette vidéo (votre client idéal) ?", placeholder="ex: Entrepreneurs, salariés...")
        audience_frustration = st.text_input("Quel est le problème principal de votre audience ?", placeholder="ex: Manque de temps, budget limité...")
        usp = st.text_input("Quel est votre principal avantage ou élément unique (USP) ?", placeholder="ex: Solution rapide sans engagement")
        cta_type = st.selectbox("Quelle action le spectateur doit-il faire à la fin ?", ["S'abonner", "Cliquer sur le lien en bio", "Commenter un mot clé", "Visiter le site web"])

        st.divider()

        submitted = st.form_submit_button("Générer le PDF du Brief Client", type="primary", use_container_width=True)

    if submitted:
        if not topic or not brand_name:
            st.warning("Veuillez renseigner au moins le nom de la marque et le sujet de la vidéo.")
        else:
            donnees_client = {
                "brand_name": brand_name, "topic": topic, "duration": duration,
                "platform": platform, "target_persona": target_persona,
                "audience_frustration": audience_frustration, "usp": usp, "cta_type": cta_type
            }
            
            pdf_bytes = generer_pdf_brief_client(donnees_client)
            
            st.success("Le brief client a été généré avec succès !")
            st.download_button(
                label="📥 Télécharger le PDF du Brief Client",
                data=pdf_bytes,
                file_name=f"Brief_Video_{brand_name.replace(' ', '_')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
