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
# 3. MOTEUR EXPORT PDF CORRIGÉ (SANS ERREUR D'ESPACE)
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
    pdf.set_margins(left=15, top=15, right=15) # Marges sécurisées
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
    st.markdown("### 💡 Astuce Virale")
    st.write("Remplis le maximum de détails pour générer non seulement la bible de tournage, mais aussi les **hashtags ciblés** et la **description optimisée** pour l'algorithme.")

# ---------------------------------------------------------
# 5. MODULE DE CONFIGURATION DU SCRIPT (BOMBARDEMENT DE QUESTIONS)
# ---------------------------------------------------------
st.title("🎬 AutoClip AI — Studio de Directing & Scripting Expert")
st.markdown("Réponds à ce questionnaire approfondi pour générer une bible de production complète, les hashtags viraux et la description optimisée.")

st.divider()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.subheader("1. Concept & Marque")
    topic = st.text_input("🎯 Sujet exact de la vidéo :", placeholder="ex: Comment négocier son prêt immobilier")
    brand_name = st.text_input("🏷️ Nom de la Marque / Produit :", placeholder="ex: Immobiz, Programme FitMaster...")
    usp = st.text_input("⚡ Élément différenciateur (USP) :", placeholder="ex: Seule méthode garantie sans apport")
    competitor = st.text_input("🥊 Concurrent direct à cibler / contrer :", placeholder="ex: Les banques traditionnelles, les méthodes classiques...")
    creator_type = st.radio("👤 Format de production :", ["Personne Réelle (Face Cam / Tournage réel)", "Générée par IA (Automation / Faceless)"])
    platform = st.selectbox("📱 Plateforme cible :", ["TikTok", "Instagram Reels", "YouTube Shorts", "YouTube Format Long", "LinkedIn Video", "Publicité vidéo (Meta/TikTok)"])
    duration = st.selectbox("⏱️ Durée visée :", ["Flash (15 - 30 sec)", "Standard Short (30 - 60 sec)", "Long Short (60 - 90 sec)", "Format Long (3 - 5 min)"])

with col2:
    st.subheader("2. Cible & Psychologie")
    target_persona = st.text_input("👥 Audience Cible (Persona) :", placeholder="ex: Primo-accédants, Entrepreneurs...")
    audience_frustration = st.text_input("💢 Frustration / Problème actuel :", placeholder="ex: Refus de prêt, taux d'intérêt élevés...")
    desired_result = st.text_input("✨ Résultat rêvé du prospect :", placeholder="ex: Obtenir les clés de sa maison en 3 mois")
    main_objection = st.text_input("🛑 Objection majeure à désamorcer :", placeholder="ex: 'Je n'ai pas assez d'épargne', 'C'est trop cher'...")
    target_emotion = st.selectbox("🔥 Émotion clé à provoquer :", ["Curiosité & Choc", "Peur de rater (FOMO)", "Espoir & Inspiration", "Indignation / Colère", "Rire / Humour décalé"])
    proof_social = st.text_input("🏆 Preuve Sociale / Chiffre clé :", placeholder="ex: +150 dossiers acceptés, 5 ans d'expérience...")

with col3:
    st.subheader("3. Rétention & Style")
    hook_style = st.selectbox("🪝 Type d'accroche (Hook 0-3s) :", ["Question choc / Provocation", "Statistique / Chiffre dingue", "Mise en garde / Erreur grave", "Scénario 'Imagine si...'", "Mythe populaire à briser"])
    pacing = st.selectbox("⚡ Rythme de montage :", ["Ultra-rapide (Cuts < 1.2s + SFX)", "Modéré & Captivant (Rythme parlé fluide)", "Analytique & Posé"])
    structure = st.selectbox("🏗️ Framework narratif :", ["PAS (Problème -> Agitation -> Solution)", "3 Piliers / Astuces pas-à-pas", "Avant / Après (Transformation)", "Récit / Storytelling dramatique"])
    tone = st.selectbox("🎭 Ambiance & Énergie :", ["Dynamique & Énergique", "Cash, Provocateur & Sans Filtre", "Éducatif, Clair & Expert", "Luxe, Sombre & Futuriste", "Storytelling Émotionnel"])
    speaker_energy = st.selectbox("🎙️ Style de personnalité du créateur :", ["Calme, Posé & Rassurer", "Enthousiaste, Énergique & Motivant", "Direct, Brut & Sans langue de bois"])
    vocab_style = st.selectbox("💬 Registre de langage :", ["Accessible & Courant", "Technique & Expert", "Cash & Codes Réseaux", "Formel & Soigné"])

with col4:
    st.subheader("4. Conversion & Tournage")
    cta_type = st.selectbox("🎯 Call To Action (CTA) :", ["Commenter un mot-clé (Automation)", "S'abonner pour la partie 2", "Cliquer sur le lien en bio", "Enregistrer & Partager"])
    urgency_trigger = st.text_input("⏳ Levier d'urgence (Urgency) :", placeholder="ex: Offre valable jusqu'à dimanche, 10 places dispo...")
    shooting_location = st.text_input("🏠 Décor / Lieu de tournage :", placeholder="ex: Bureau moderne, voiture, extérieur, chez soi...")
    key_props = st.text_input("🎬 Accessoire visuel à intégrer :", placeholder="ex: Montrer un contrat, tenir des clés, un téléphone...")
    forbidden_words = st.text_input("🚫 Mots / Expressions interdites :", placeholder="ex: Ne pas dire 'argent facile', pas de gros mots...")
    music_genre = st.text_input("🎵 Ambiance Sonore :", placeholder="ex: Musique dynamique motivante, Lofi neutre...")
    extra_details = st.text_area("⚙️ Consignes Spécifiques :", placeholder="ex: Insérer un graphique explicatif, ne pas mentionner de tarif...")

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
        
        prompt_template = """
        Tu es le Meilleur Directeur Artistique, Réalisateur Vidéo, Growth Hacker et Master Copywriter au Monde.
        Rédige un SCRIPT BIBLE EXHAUSTIF, HYPER LONG, DÉTAILLÉ SÉQUENCE PAR SÉQUENCE, AU MOT PRÈS.

        NE SOIS PAS SYNTHÉTIQUE. DÉTAILLE TOUT. Rédige chaque réplique intégrale sans résumé ni '...'.
        NE CITE AUCUN NOM D'APPLICATION NI DE LOGICIEL TIERS.
        ADAPTE-TOI STRICTEMENT À LA NICHE, AU CLIENT ET AU SUJET FOURNI.

        --- CONFIGURATION DE PRODUCTION CLIENT ULTRA-PRÉCISE ---
        - Sujet exact : {topic}
        - Marque / Offre du client : {brand_name}
        - Élément différenciateur (USP) : {usp}
        - Concurrent ciblé : {competitor}
        - Mode de production : {creator_type}
        - Plateforme : {platform}
        - Durée : {duration}
        - Persona / Audience Cible : {target_persona}
        - Frustration majeure : {audience_frustration}
        - Résultat rêvé par le prospect : {desired_result}
        - Objection n°1 à désamorcer : {main_objection}
        - Émotion clé visée : {target_emotion}
        - Preuve sociale / Chiffre clé : {proof_social}
        - Levier d'urgence (Urgency) : {urgency_trigger}
        - Style de personnalité du créateur : {speaker_energy}
        - Registre de langage : {vocab_style}
        - Ton & Ambiance : {tone}
        - Décor / Lieu de tournage : {shooting_location}
        - Accessoire visuel clé : {key_props}
        - Mots interdits : {forbidden_words}
        - Hook (0-3s) : {hook_style}
        - Rythme de montage : {pacing}
        - Framework narratif : {structure}
        - CTA : {cta_type}
        - Style sonore/musical : {music_genre}
        - Consignes spécifiques : {extra_details}

        --- FORMAT DE RÉPONSE EXIGÉ (Markdown d'Élite) ---

        # 🎬 BIBLE DE PRODUCTION & SCRIPT ULTRA-DÉTAILLÉ

        ### 📋 1. DIRECTION ARTISTIQUE & SETUP DÉTAILLÉ
        - **Marque / Client** : {brand_name} (USP : {usp})
        - **Format & Ratio** : 9:16 Vertical
        - **Énergie du créateur** : {speaker_energy} | Émotion ciblée : {target_emotion}
        - **Décor & Mise en scène** : {shooting_location} | Accessoires : {key_props}
        - **Palette de couleurs & Ambiance lumineuse** : [Détails ultra-précis des teintes, ombres et éclairages]
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

        Fournis 5 à 7 séquences hyper détaillées adaptées au sujet. Chaque dialogue doit être rédigé au mot près en intégrant l'USP, la preuve sociale et le désamorçage de l'objection.

        #### 🔹 SÉQUENCE 1 : Agitation de la Frustration (`00:03 - 00:12`)
        * **Timecode** : `00:03 - 00:12`
        * **Dialogues / Voix-off intégrale** : "..."
        * **Intonation & Pauses** : [Consignes vocales]
        * **{broll_label}** : [...]
        * **Incrustation Texte / Graphisme** : [Texte affiché]
        * **SFX & Ambiance** : [Bruitage / Effet sonore]

        #### 🔹 SÉQUENCE 2 : Désamorçage de l'Objection Majeure ({main_objection}) (`00:12 - 00:25`)
        * **Timecode** : `00:12 - 00:25`
        * **Dialogues / Voix-off intégrale** : "..."
        * **Intonation & Pauses** : [Consignes vocales]
        * **{broll_label}** : [...]
        * **Incrustation Texte / Graphisme** : [Graphique / Animation]
        * **SFX** : [Bruitage]

        #### 🔹 SÉQUENCE 3 : La Révélation de la Solution ({brand_name} / {usp}) (`00:25 - 00:40`)
        * **Timecode** : `00:25 - 00:40`
        * **Dialogues / Voix-off intégrale** : "..."
        * **{broll_label}** : [...]
        * **Incrustation Texte / Graphisme** : [Puces explicatives]
        * **SFX** : [Bruitage]

        #### 🔹 SÉQUENCE 4 : Preuve Sociale ({proof_social}) Pas-à-Pas (`00:40 - 00:55`)
        * **Timecode** : `00:40 - 00:55`
        * **Dialogues / Voix-off intégrale** : "..."
        * **{broll_label}** : [...]
        * **Incrustation Texte / Graphisme** : [Étapes / Preuves]

        #### 🔹 SÉQUENCE 5 : Impact & Projection vers le Résultat Rêvé ({desired_result}) (`01:10 - Fin`)
        * **Timecode** : `01:10 - Fin`
        * **Dialogues / Voix-off intégrale** : "..."
        * **{broll_label}** : [...]

        ---

        ### 🎯 4. CONCLUSION & CALL TO ACTION (CONVERSION)
        * **Timecode** : `Fin de vidéo`
        * **Dialogues / Voix-off intégrale** : "..." (Intégrant le levier d'urgence : {urgency_trigger})
        * **Action Visuelle & Incrustation** : [Flèche vers le profil, bouton follow, mot-clé à commenter]
        * **Outro Audio** : [Fondu de musique]

        ---

        ### 📈 5. STRATÉGIE DE PUBLICATION & HASHTAGS VIRAUX
        * **Légende / Caption de la publication** : [Rédige une description captivante avec un hook textuel et un CTA court]
        * **Hashtags de Niche (3-5)** : `#... #... #...`
        * **Hashtags d'Audience Cible (3-5)** : `#... #... #...`
        * **Hashtags Tendances / Viraux (3-5)** : `#... #... #...`

        ---

        ### 🤖 6. SCRIPT AUTO-PROMPT CLÉ EN MAIN (À COPIER-COLLER POUR L'IA GÉNÉRATRICE DE VIDÉO)
        C'EST UNE SECTION OBLIGATOIRE. Rédige tout en bas un bloc de code unique (```) en Anglais technique, ultra-clair et structuré, prêt à être directement copié-collé dans n'importe quelle IA génératrice de vidéo.
        Inclus obligatoirement :
        1. **Global Topic, Mood & Style Directive** (Cinematic, 8K, 9:16 Aspect Ratio, Lighting).
        2. **Full Voiceover Script** (Mot à mot en français ou anglais selon la cible, sans résumé).
        3. **Scene-by-Scene Visual Generation Prompts** (Horodatés de 0s à la fin).
        4. **Audio & On-Screen Text Overlay Directives**.
        """

        prompt = prompt_template.format(
            topic=topic,
            brand_name=brand_name if brand_name else 'Non spécifié',
            usp=usp if usp else 'Non spécifié',
            competitor=competitor if competitor else 'Non spécifié',
            creator_type=creator_type,
            platform=platform,
            duration=duration,
            target_persona=target_persona if target_persona else 'Grand public',
            audience_frustration=audience_frustration if audience_frustration else 'Non spécifiée',
            desired_result=desired_result if desired_result else 'Non spécifié',
            main_objection=main_objection if main_objection else 'Aucune',
            target_emotion=target_emotion,
            proof_social=proof_social if proof_social else 'Aucune',
            urgency_trigger=urgency_trigger if urgency_trigger else 'Aucun',
            speaker_energy=speaker_energy,
            vocab_style=vocab_style,
            tone=tone,
            shooting_location=shooting_location if shooting_location else 'Non spécifié',
            key_props=key_props if key_props else 'Aucun',
            forbidden_words=forbidden_words if forbidden_words else 'Aucun',
            hook_style=hook_style,
            pacing=pacing,
            structure=structure,
            cta_type=cta_type,
            music_genre=music_genre if music_genre else 'Inconnu',
            extra_details=extra_details if extra_details else 'Aucune',
            visual_label=visual_label,
            broll_label=broll_label
        )

        with st.spinner("🎬 Production du script d'élite, de la bible et de la stratégie virale..."):
            try:
                response = groq_client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[{"role": "user", "content": prompt}]
                )
                script = response.choices[0].message.content

                st.success("✨ Bible de production, Hashtags viraux & Script générés avec succès !")
                st.markdown(script)

                # Export PDF sécurisé
                pdf_data = generer_pdf_script(topic if topic else "Script_Video", script)
                st.download_button(
                    label="📄 Télécharger le Script & Bible de Tournage en PDF",
                    data=pdf_data,
                    file_name=f"Script_{topic.replace(' ', '_') if topic else 'Production'}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

            except Exception as e:
                st.error(f"Erreur lors de la génération : {e}")
