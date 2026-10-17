import streamlit as st
from groq import Groq
from fpdf import FPDF

# ---------------------------------------------------------
# 1. CONFIGURATION PAGE ET DESIGN CSS
# ---------------------------------------------------------
st.set_page_config(
    page_title="AutoClip AI — Studio Privé de Production Vidéo",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp { background-color: #0E1117; }
    div[data-testid="stVerticalBlock"] > div { border-radius: 10px; }
    .stButton>button { border-radius: 8px; font-weight: 600; transition: all 0.3s ease; }
    
    .script-container {
        background-color: #161B22;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #30363D;
    }
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
# 3. MOTEUR EXPORT PDF CORRIGÉ
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
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    titre_propre = (titre_video or "Script_Video")\
        .replace('—', '-')\
        .replace('–', '-')\
        .replace('’', "'")\
        .replace('«', '"')\
        .replace('»', '"')
        
    pdf.set_font("Helvetica", 'B', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 8, f"Sujet : {titre_propre}")
    pdf.ln(5)
    
    lignes = contenu_markdown.split('\n')
    for ligne in lignes:
        ligne_nettoyee = (ligne or "")\
            .replace('—', '-')\
            .replace('–', '-')\
            .replace('’', "'")\
            .replace('«', '"')\
            .replace('»', '"')\
            .replace('•', '*')
            
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

# ---------------------------------------------------------
# 4. BARRE LATÉRALE (SIDEBAR) PRIVÉE
# ---------------------------------------------------------
with st.sidebar:
    st.title("🎬 AutoClip Studio")
    st.success("⚡ **Mode Studio Privé Actif**")
    st.info("Utilisation illimitée & accès direct réservé.")
    st.divider()
    st.markdown("### 💡 Astuce Production")
    st.write("Exporte tes scripts en **PDF** pour les lire pendant tes tournages ou les envoyer directement à tes clients.")

# ---------------------------------------------------------
# 5. MODULE DE CONFIGURATION DU SCRIPT
# ---------------------------------------------------------
st.title("🎬 AutoClip AI — Studio de Directing & Scripting Privé")
st.markdown("Configure tes critères pour générer une bible de production complète, un script ultra-détaillé et le Master-Prompt IA.")

st.divider()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.subheader("1. Concept & Format")
    topic = st.text_input("🎯 Sujet exact de la vidéo :", placeholder="Entrez le sujet de votre vidéo...")
    creator_type = st.radio("👤 Format de production :", ["Personne Réelle (Face Cam / Tournage réel)", "Générée par IA (Automation / Faceless)"])
    platform = st.selectbox("📱 Plateforme cible :", ["TikTok", "Instagram Reels", "YouTube Shorts", "YouTube Format Long", "LinkedIn Video", "Publicité vidéo (Meta/TikTok)"])
    duration = st.selectbox("⏱️ Durée visée :", ["Flash (15 - 30 sec)", "Standard Short (30 - 60 sec)", "Long Short (60 - 90 sec)", "Format Long (3 - 5 min)"])

with col2:
    st.subheader("2. Cible & Psychologie")
    target_persona = st.text_input("👥 Audience Cible (Exemple) :", placeholder="ex: Entrepreneurs, Étudiants, Sportifs, Clients e-commerce...")
    audience_frustration = st.text_input("💢 Frustration / Problème (Exemple) :", placeholder="ex: Manque de temps, manque de budget, manque d'organisation...")
    tone = st.selectbox("🎭 Ambiance & Énergie :", ["Dynamique & Énergique", "Cash, Provocateur & Sans Filtre", "Éducatif, Clair & Expert", "Luxe, Sombre & Futuriste", "Storytelling Émotionnel"])

with col3:
    st.subheader("3. Rétention & Structure")
    hook_style = st.selectbox("🪝 Type d'accroche (Hook 0-3s) :", ["Question choc / Provocation", "Statistique / Chiffre dingue", "Mise en garde / Erreur grave", "Scénario 'Imagine si...'", "Mythe populaire à briser"])
    pacing = st.selectbox("⚡ Rythme de montage :", ["Ultra-rapide (Cuts < 1.2s + SFX)", "Modéré & Captivant (Rythme parlé fluide)", "Analytique & Posé"])
    structure = st.selectbox("🏗️ Framework narratif :", ["PAS (Problème -> Agitation -> Solution)", "3 Piliers / Astuces pas-à-pas", "Avant / Après (Transformation)", "Récit / Storytelling dramatique"])

with col4:
    st.subheader("4. Conversion & Style")
    cta_type = st.selectbox("🎯 Call To Action (CTA) :", ["Commenter un mot-clé (Automation)", "S'abonner pour la partie 2", "Cliquer sur le lien en bio", "Enregistrer & Partager"])
    music_genre = st.text_input("🎵 Ambiance Sonore (Exemple) :", placeholder="ex: Musique dynamique motivante, Ambiance cinématique, Aucune musique...")
    extra_details = st.text_area("⚙️ Éléments Imposés (Exemple) :", placeholder="ex: Mentionner un tarif promotionnel, insérer un graphique explicatif, décor moderne...")

st.divider()

# ---------------------------------------------------------
# 6. GÉNÉRATION & EXPORT PDF
# ---------------------------------------------------------
if st.button("🚀 Générer le Plan de Production & Script d'Élite", type="primary", use_container_width=True):
    if not topic:
        st.warning("⚠️ Veuillez préciser le sujet exact de la vidéo.")
    else:
        is_ia_mode = (creator_type == "Générée par IA (Automation / Faceless)")
        visual_label = "Prompt Visuel Brut en Anglais (8K, Cinematic)" if is_ia_mode else "Mouvement de caméra & Jeu du présentateur"
        broll_label = "Prompt Visuel Brut (Anglais)" if is_ia_mode else "Plan B-Roll & Cadrage"
        
        prompt = f"""
        Tu es le Meilleur Directeur Artistique, Réalisateur Vidéo et Master Copywriter au Monde.
        Rédige un SCRIPT BIBLE EXHAUSTIF, HYPER LONG, DÉTAILLÉ SÉQUENCE PAR SÉQUENCE, AU MOT PRÈS.

        NE SOIS PAS SYNTHÉTIQUE. DÉTAILLE TOUT. Rédige chaque réplique intégrale sans résumé ni '...'.
        NE CITE AUCUN NOM D'APPLICATION NI DE LOGICIEL TIERS.
        ADAPTE-TOI STRICTEMENT À LA NICHE ET AU SUJET FOURNI.

        --- CONFIGURATION DE PRODUCTION ---
        - Sujet : {topic}
        - Mode de production : {creator_type}
        - Plateforme : {platform}
        - Durée : {duration}
        - Persona / Audience Cible : {target_persona if target_persona else 'Grand public'}
        - Frustration majeure : {audience_frustration if audience_frustration else 'Non spécifiée'}
        - Ton & Ambiance : {tone}
        - Hook (0-3s) : {hook_style}
        - Rythme de montage : {pacing}
        - Framework narratif : {structure}
        - CTA : {cta_type}
        - Style sonore/musical : {music_genre if music_genre else 'Inconnu'}
        - Exigences : {extra_details if extra_details else 'Aucune'}

        --- FORMAT DE RÉPONSE EXIGÉ (Markdown d'Élite) ---

        # 🎬 BIBLE DE PRODUCTION & SCRIPT ULTRA-DÉTAILLÉ

        ### 📋 1. DIRECTION ARTISTIQUE & SETUP DÉTAILLÉ
        - **Format & Ratio** : 9:16 Vertical
        - **Palette de couleurs & Ambiance lumineuse** : [Détails ultra-précis des teintes, ombres et réflecteurs]
        - **Sound Design & Ambiance audio** : [Style sonore, moments de coupure audio, rythme]
        - **Règles Typographiques (Sous-titres)** : [Police, taille, couleur active/inactive, effets de pop-up]
        - **Stratégie de Rétention algorithmique** : [Découpage des micro-hooks à 3s, 10s et 25s]

        ---

        ### 🪝 2. L'ACCROCHE ULTIME (HOOK - 00:00 à 00:03)
        * **Timecode** : `00:00 - 00:03`
        * **Voix-off / Dialogues exacts (Word-for-word)** : "..."
        * **Intonation & Tonalité** : [Ex: Ton provocateur, hausse de voix à la fin]
        * **{visual_label}** : [...]
        * **Incrustation Texte à l'écran** : "..." [Couleur, effet d'apparition]
        * **Sound Effect (SFX)** : [Bruitage précis]

        ---

        ### 🎬 3. DÉCOUPAGE EXHAUSTIF SÉQUENCE PAR SÉQUENCE (MINUTÉ & MOT À MOT)

        Fournis 5 à 7 séquences hyper détaillées adaptées au sujet. Chaque dialogue doit être rédigé au mot près.

        #### 🔹 SÉQUENCE 1 : Agitation de la Frustration (`00:03 - 00:12`)
        * **Timecode** : `00:03 - 00:12`
        * **Dialogues / Voix-off intégrale** : "..."
        * **Intonation & Pauses** : [Consignes vocales]
        * **{broll_label}** : [...]
        * **Incrustation Texte / Graphisme** : [Texte affiché]
        * **SFX & Ambiance** : [Bruitage / Effet sonore]

        #### 🔹 SÉQUENCE 2 : Déconstruction de l'Erreur Courante (`00:12 - 00:25`)
        * **Timecode** : `00:12 - 00:25`
        * **Dialogues / Voix-off intégrale** : "..."
        * **Intonation & Pauses** : [Consignes vocales]
        * **{broll_label}** : [...]
        * **Incrustation Texte / Graphisme** : [Graphique / Animation]
        * **SFX** : [Bruitage]

        #### 🔹 SÉQUENCE 3 : La Révélation de la Solution (`00:25 - 00:40`)
        * **Timecode** : `00:25 - 00:40`
        * **Dialogues / Voix-off intégrale** : "..."
        * **{broll_label}** : [...]
        * **Incrustation Texte / Graphisme** : [Puces explicatives]
        * **SFX** : [Bruitage]

        #### 🔹 SÉQUENCE 4 : Application Pratique Pas-à-Pas (`00:40 - 00:55`)
        * **Timecode** : `00:40 - 00:55`
        * **Dialogues / Voix-off intégrale** : "..."
        * **{broll_label}** : [...]
        * **Incrustation Texte / Graphisme** : [Étapes 1, 2, 3]

        #### 🔹 SÉQUENCE 5 : Preuve de Résultat & Impact (`01:10 - Fin`)
        * **Timecode** : `01:10 - Fin`
        * **Dialogues / Voix-off intégrale** : "..."
        * **{broll_label}** : [...]

        ---

        ### 🎯 4. CONCLUSION & CALL TO ACTION (CONVERSION)
        * **Timecode** : `Fin de vidéo`
        * **Dialogues / Voix-off intégrale** : "..."
        * **Action Visuelle & Incrustation** : [Flèche vers le profil, bouton follow, mot-clé à commenter]
        * **Outro Audio** : [Fondu de musique]

        ---

        ### 🤖 5. SCRIPT AUTO-PROMPT CLÉ EN MAIN (À COPIER-COLLER POUR L'IA GÉNÉRATRICE DE VIDÉO)
        C'EST UNE SECTION OBLIGATOIRE. Rédige tout en bas un bloc de code unique (```) en Anglais technique, ultra-clair et structuré, prêt à être directement copié-collé dans n'importe quelle IA génératrice de vidéo.
        Inclus obligatoirement :
        1. **Global Topic, Mood & Style Directive** (Cinematic, 8K, 9:16 Aspect Ratio, Lighting).
        2. **Full Voiceover Script** (Mot à mot en français ou anglais selon la cible, sans résumé).
        3. **Scene-by-Scene Visual Generation Prompts** (Horodatés
