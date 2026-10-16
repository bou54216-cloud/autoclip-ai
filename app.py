import streamlit as st
import requests
import json

# 1. Configuration de la page
st.set_page_config(
    page_title="The Empire Studio — Creative Suite",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Design Clean & Sombre
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .stApp {
        background-color: #09090b;
        color: #f4f4f5;
    }

    .editorial-header {
        text-align: center;
        padding: 40px 10px 10px 10px;
    }

    .editorial-tag {
        font-size: 0.75rem;
        font-weight: 800;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #71717a;
        margin-bottom: 8px;
        display: inline-block;
    }

    .editorial-title {
        font-size: 2.6rem;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -1px;
        margin-bottom: 8px;
    }

    .editorial-subtitle {
        font-size: 0.95rem;
        color: #a1a1aa;
        max-width: 550px;
        margin: 0 auto 20px auto;
    }

    .card-wrapper {
        background: #121216;
        border: 1px solid #27272a;
        border-radius: 18px;
        padding: 28px 22px;
        text-align: left;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 220px;
        height: 100%;
    }

    .card-wrapper:hover {
        border-color: #3f3f46;
        transform: translateY(-4px);
        background: #18181b;
        box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.7);
    }

    .card-number {
        font-size: 0.75rem;
        font-weight: 600;
        color: #52525b;
        margin-bottom: 10px;
        font-family: monospace;
    }

    .card-title {
        font-size: 1.35rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 8px;
    }

    .card-desc {
        font-size: 0.88rem;
        color: #a1a1aa;
        line-height: 1.5;
    }

    .stTextInput input, .stSelectbox div[data-baseweb="select"], .stTextArea textarea {
        background-color: #121216 !important;
        border: 1px solid #27272a !important;
        border-radius: 12px !important;
        color: #f4f4f5 !important;
    }
    
    .stTextInput input:focus, .stSelectbox div[data-baseweb="select"]:focus-within, .stTextArea textarea:focus {
        border-color: #ffffff !important;
        box-shadow: 0 0 0 1px #ffffff !important;
    }

    .stButton>button {
        width: 100%;
        background: #ffffff;
        color: #09090b;
        font-weight: 700;
        font-size: 0.9rem;
        border-radius: 12px;
        padding: 12px 18px;
        border: none;
        cursor: pointer;
        transition: all 0.2s ease;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .stButton>button:hover {
        background: #e4e4e7;
        color: #000000;
        transform: translateY(-1px);
    }
    </style>
""", unsafe_allow_html=True)

GROQ_API_KEY = "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"

# --- SYSTÈME D'AUTHENTIFICATION GOOGLE ---
if not st.experimental_user.is_logged_in:
    st.markdown("""
        <div class="editorial-header" style="margin-top: 50px;">
            <span class="editorial-tag">Accès Sécurisé — Imperial Suite</span>
            <h1 class="editorial-title">The Empire Studio</h1>
            <p class="editorial-subtitle">Connectez-vous avec votre compte Google pour accéder à votre espace créatif.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col_a, col_b, col_c = st.columns([1, 1, 1])
    with col_b:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🌐 Se connecter avec Google"):
            st.login("google")
else:
    # L'utilisateur est connecté
    nom_utilisateur = st.experimental_user.name
    email_utilisateur = st.experimental_user.email

    # Barre supérieure de profil
    col_prof1, col_prof2 = st.columns([8, 2])
    with col_prof1:
        st.caption(f"👤 Connecté en tant que **{nom_utilisateur}** ({email_utilisateur})")
    with col_prof2:
        if st.button("Se déconnecter"):
            st.logout()

    if "module_choisi" not in st.session_state:
        st.session_state["module_choisi"] = None

    # Barre de navigation interne si un module est sélectionné
    if st.session_state["module_choisi"] is not None:
        c_space, c_nav = st.columns([8, 2])
        with c_nav:
            if st.button("← Accueil"):
                st.session_state["module_choisi"] = None
                st.rerun()

    # =========================================================
    # ÉCRAN D'ACCUEIL : LES TROIS CARTES
    # =========================================================
    if st.session_state["module_choisi"] is None:
        st.markdown("""
            <div class="editorial-header">
                <span class="editorial-tag">Selected Works & Systems — 2026</span>
                <h1 class="editorial-title">The Empire Studio</h1>
                <p class="editorial-subtitle">Sélectionnez le module créatif à déployer pour votre projet.</p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3, gap="large")

        with col1:
            st.markdown("""
                <div class="card-wrapper">
                    <div>
                        <div class="card-number">01 // VIDEO ENGINE</div>
                        <div class="card-title">AutoClip AI</div>
                        <div class="card-desc">Scripts vidéo, hooks viraux, titres dynamiques et structures optimisées pour TikTok, Reels et Shorts.</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Lancer AutoClip ↗", key="btn_autoclip"):
                st.session_state["module_choisi"] = "AutoClip"
                st.rerun()

        with col2:
            st.markdown("""
                <div class="card-wrapper">
                    <div>
                        <div class="card-number">02 // BRAND IDENTITY</div>
                        <div class="card-title">BioCraft AI</div>
                        <div class="card-desc">Architecture d'identité de marque, bios magnétiques d'élite et positionnement stratégique sur-mesure.</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Lancer BioCraft ↗", key="btn_biocraft"):
                st.session_state["module_choisi"] = "BioCraft"
                st.rerun()

        with col3:
            st.markdown("""
                <div class="card-wrapper">
                    <div>
                        <div class="card-number">03 // COPYWRITING & SALES</div>
                        <div class="card-title">CopyCraft AI</div>
                        <div class="card-desc">Rédaction persuasive, e-mails de prospection B2B, pages de vente et structures de conversion directes.</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Lancer CopyCraft ↗", key="btn_copycraft"):
                st.session_state["module_choisi"] = "CopyCraft"
                st.rerun()

    # =========================================================
    # MODULE 1 : AUTOCLIP AI
    # =========================================================
    elif st.session_state["module_choisi"] == "AutoClip":
        st.markdown("### ⚡ AutoClip AI — Configuration Vidéo")
        st.caption("Paramétrez votre contenu pour obtenir un rendu immédiat et structuré.")
        
        sujet_clip = st.text_input("🎯 Sujet ou concept de la vidéo", placeholder="ex: 3 astuces pour booster sa productivité au quotidien")
        
        c1, c2 = st.columns(2)
        with c1:
            plateforme = st.selectbox("📱 Plateforme Cible", ["TikTok", "Instagram Reels", "YouTube Shorts"])
            style_clip = st.selectbox("🎨 Style de Format", ["Éducatif / Conseil", "Storytelling", "Promotion / Business", "Divertissement"])
            type_rendu_autoclip = st.selectbox("📌 Type de Résultat", ["Texte final prêt à publier", "Script / Prompt de consignes pour une IA vidéo"])
        with c2:
            ton_clip = st.selectbox("🎙️ Ton Souhaité", ["Énergique & Rythmé", "Humoristique & Décalé", "Cash & Direct", "Professionnel & Inspirant"])
            duree = st.selectbox("⏱️ Durée Estimée", ["15 secondes", "30 secondes", "45 secondes", "1 minute", "1 minute 30 secondes"])
            
        methode = st.selectbox("🎬 Méthode de Réalisation", ["Tournage Humain (Visage caméra + B-roll)", "Génération IA (InVideo / CapCut)"])
        ambiance_musique = st.text_input("🎵 Ambiance Sonore / Style musical (Optionnel)", placeholder="ex: Lo-fi relaxant, beat dynamique...")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Générer le Kit Vidéo ↗"):
            if not sujet_clip:
                st.warning("⚠️ Veuillez renseigner un sujet.")
            else:
                with st.spinner("Génération en cours..."):
                    prompt = f"""
                    Tu es un expert mondial en création de contenu viral sur {plateforme}.
                    Génère un Kit de Production Complet ({type_rendu_autoclip}) pour une vidéo de {duree} sur : '{sujet_clip}' (Style: {style_clip}, Ton: {ton_clip}).
                    Méthode : {methode}. Ambiance sonore : {ambiance_musique}.
                    
                    Rédige directement un texte extrêmement détaillé et prêt à l'emploi.
                    Format de sortie :
                    ### 🎬 Titres & Couverture
                    ### 🪝 Script de Production ({duree})
                    ### 📝 Description & Hashtags SEO
                    """
                    
                    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
                    payload = {"model": "openai/gpt-oss-120b", "messages": [{"role": "user", "content": prompt}]}
                    
                    try:
                        res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, data=json.dumps(payload)).json()
                        if "choices" in res:
                            contenu = res["choices"][0]["message"]["content"]
                            st.toast("Contenu généré !", icon="✨")
                            st.markdown("### 📋 Votre texte prêt à l'emploi :")
                            st.code(contenu, language="markdown")
                        else:
                            st.error("Erreur de génération.")
                    except Exception as e:
                        st.error(f"Erreur : {e}")

    # =========================================================
    # MODULE 2 : BIOCRAFT AI
    # =========================================================
    elif st.session_state["module_choisi"] == "BioCraft":
        st.markdown("### 💼 BioCraft AI — Architecture d'Identité")
        st.caption("Définissez votre positionnement de marque.")
        
        c1, c2 = st.columns(2)
        with c1:
            plateforme_bio = st.selectbox("🌐 Plateforme Principale", ["TikTok / Instagram (Créateur)", "LinkedIn (Professionnel / Corporate)", "Site Web / Portfolio", "Autre"])
            ton_bio = st.selectbox("🎯 Posture de Marque", ["Autoritaire & Visionnaire", "Mystérieux & Énigmatique", "Accessible & Pédagogue", "Audacieux & Disruptif"])
            type_rendu_bio = st.selectbox("📌 Type de Résultat", ["Texte final prêt à publier (Bios & CTA)", "Script / Prompt de consignes pour une IA de branding"])
        with c2:
            objectif_bio = st.selectbox("📈 Objectif Principal", ["Attirer des opportunités B2B", "Convertir en abonnés fidèles", "Vendre un produit ou service", "Établir une crédibilité instantanée"])
            longueur_bio = st.selectbox("📏 Format de la Bio", ["Ultra-court & Percutant", "Narratif & Inspirant", "À puces / Preuve sociale"])
            style_emojis = st.selectbox("✨ Style d'Émojis", ["Minimaliste & Chic", "Dynamique & Thématique", "Aucun"])

        parcours_pro = st.text_area("✍️ Votre parcours, compétences clés ou accomplissements", placeholder="Renseignez votre parcours, vos projets ou vos réalisations ici...", height=120)
        mots_cles_cles = st.text_input("🔑 Mots-clés incontournables (Optionnel)", placeholder="ex: Innovation, Stratégie, Design...")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Forger l'Identité ↗"):
            if not parcours_pro:
                st.warning("⚠️ Veuillez renseigner votre parcours.")
            else:
                with st.spinner("Création en cours..."):
                    prompt = f"""
                    Tu es un expert mondial en stratégie de marque et personal branding d'élite.
                    Génère un contenu complet ({type_rendu_bio}) basé sur :
                    - Plateforme : {plateforme_bio}
                    - Posture : {ton_bio}
                    - Objectif : {objectif_bio}
                    - Format : {longueur_bio}
                    - Émojis : {style_emojis}
                    - Parcours : '{parcours_pro}'
                    - Mots-clés : {mots_cles_cles}
                    
                    Rédige directement un texte détaillé et prêt à copier.
                    Format de sortie :
                    ### 🎯 Analyse du Positionnement
                    ### ✍️ Options de Bios Prêtes à Copier
                    ### 🔗 Formules d'Appel à l'Action (CTA)
                    """
                    
                    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
                    payload = {"model": "openai/gpt-oss-120b", "messages": [{"role": "user", "content": prompt}]}
                    
                    try:
                        res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, data=json.dumps(payload)).json()
                        if "choices" in res:
                            contenu = res["choices"][0]["message"]["content"]
                            st.toast("Identité forgée !", icon="✨")
                            st.markdown("### 📋 Votre texte prêt à l'emploi :")
                            st.code(contenu, language="markdown")
                        else:
                            st.error("Erreur de génération.")
                    except Exception as e:
                        st.error(f"Erreur : {e}")

    # =========================================================
    # MODULE 3 : COPYCRAFT AI
    # =========================================================
    elif st.session_state["module_choisi"] == "CopyCraft":
        st.markdown("### 📝 CopyCraft AI — Copywriting & Émails de Vente")
        st.caption("Concevez des textes de vente persuasifs et des séquences d'émails haute conversion.")
        
        c1, c2 = st.columns(2)
        with c1:
            type_copy = st.selectbox("📄 Type de Contenu", ["Émail de Prospection B2B (Cold Email)", "Séquence de Lancement de Produit", "Page de Vente / Landing Page", "Publicité Social Media (Meta / Google)"])
            framework_copy = st.selectbox("⚙️ Framework de Copywriting", ["AIDA (Attention, Intérêt, Désir, Action)", "PAS (Problème, Agitation, Solution)", "BAB (Before, After, Bridge)", "Direct & Minimaliste"])
            type_rendu_copy = st.selectbox("📌 Type de Résultat", ["Texte final prêt à être envoyé / publié", "Script / Prompt de consignes pour une IA de rédaction"])
        with c2:
            ton_copy = st.selectbox("🎙️ Ton & Style", ["Convaincant & Direct", "Inspirant & Storytelling", "Professionnel & B2B", "Urgent & Offre Limité"])
            cible_copy = st.text_input("👥 Cible / Prospect (Audience)", placeholder="ex: Fondateurs de startups, Directeurs Marketing, Particuliers...")

        description_offre = st.text_area("📦 Description du produit, service ou offre", placeholder="Décrivez les bénéfices clés, le problème résolu et la valeur ajoutée...", height=120)
        cta_souhaite = st.text_input("🎯 Appel à l'Action Principal (CTA)", placeholder="ex: Réserver un appel de 15 min, Télécharger le guide, Acheter maintenant...")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Générer le Texte Copywriting ↗"):
            if not description_offre:
                st.warning("⚠️ Veuillez décrire votre offre.")
            else:
                with st.spinner("Rédaction en cours..."):
                    prompt = f"""
                    Tu es un copywriter d'élite reconnu mondialement.
                    Rédige un contenu ultra-persuasif ({type_rendu_copy}) basé sur :
                    - Type de contenu : {type_copy}
                    - Framework : {framework_copy}
                    - Ton : {ton_copy}
                    - Cible : {cible_copy}
                    - Offre : '{description_offre}'
                    - CTA : {cta_souhaite}
                    
                    Rédige directement un texte extrêmement complet, fluide et immédiatement utilisable sans explication.
                    Format de sortie :
                    ### 🎯 Objets & Accroches Striking (3 Variantes)
                    ### ✉️ Corps du Texte / Émail
                    ### 🚀 Appel à l'Action & P.S. Persuasif
                    """
                    
                    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
                    payload = {"model": "openai/gpt-oss-120b", "messages": [{"role": "user", "content": prompt}]}
                    
                    try:
                        res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, data=json.dumps(payload)).json()
                        if "choices" in res:
                            contenu = res["choices"][0]["message"]["content"]
                            st.toast("Texte généré avec succès !", icon="✨")
                            st.markdown("### 📋 Votre texte prêt à l'emploi :")
                            st.code(contenu, language="markdown")
                        else:
                            st.error("Erreur de génération.")
                    except Exception as e:
                        st.error(f"Erreur : {e}")

st.markdown("<br><hr style='border-color: #27272a;'><p style='text-align: center; color: #52525b; font-size: 0.8rem;'>The Empire Studio — All Rights Reserved.</p>", unsafe_allow_html=True)
