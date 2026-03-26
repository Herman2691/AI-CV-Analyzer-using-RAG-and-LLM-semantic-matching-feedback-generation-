"""
CHECK CV - Version Finale Corrigée & Optimisée
Correction de la SyntaxError + Design Gemini + Texte Blanc Lisible
"""

from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from mistralai.client import MistralClient
import json
from typing import List, Dict, Any
import io
import base64

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="CHECK CV - Analyseur Pro",
    page_icon="✨",
    layout="wide"
)

# --- STYLE CSS (DESIGN GEMINI + TEXTE BLANC) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&family=Inter:wght@300;400;500;600&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #f8f9fa; }
    
    .professional-header {
        background: white; 
        padding: 40px; 
        border-radius: 24px; 
        margin-bottom: 30px; 
        border: 1px solid #e3e3e3; 
        text-align: center;
    }
    .professional-header h1 { color: #1f1f1f; font-size: 2.5em; font-weight: 500; margin: 0; }

    .upload-card, .result-card {
        background: white; 
        border-radius: 24px; 
        padding: 25px;
        border: 1px solid #e3e3e3; 
        margin-bottom: 20px;
    }

    .score-number { 
        font-size: 3em; 
        font-weight: 500; 
        color: #0b57d0; 
        line-height: 1; 
    }

    /* SECTIONS DE RÉSULTATS - FORÇAGE BLANC */
    .analysis-section {
        border-radius: 16px; 
        padding: 20px; 
        margin-top: 15px;
        height: 100%; 
        color: #ffffff !important;
    }
    .section-strengths { background-color: #1a73e8; border-color: #174ea6; } 
    .section-improvements { background-color: #f9ab00; border-color: #b06000; }
    .section-recommendations { background-color: #34a853; border-color: #2e7d32; }

    .analysis-section h4 { 
        color: #ffffff !important; 
        text-transform: uppercase; 
        font-size: 0.9em; 
        letter-spacing: 1px; 
        margin-bottom: 15px; 
    }
    
    /* On s'assure que Streamlit n'écrase pas le blanc */
    .analysis-section p, .analysis-section li, .analysis-section div { 
        color: #ffffff !important; 
        font-size: 0.95em; 
        line-height: 1.5;
    }

    .stButton > button {
        background-color: #0b57d0 !important; 
        color: white !important;
        border-radius: 100px !important; 
        padding: 12px 30px !important;
        width: 100%; 
        border: none !important; 
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

# --- LOGIQUE MISTRAL ---

@st.cache_resource
def init_mistral():
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        st.error("Clé API manquante dans les variables d'environnement.")
        st.stop()
    return MistralClient(api_key=api_key)

def extract_text(file) -> str:
    try:
        if file.type == "application/pdf":
            import PyPDF2
            reader = PyPDF2.PdfReader(io.BytesIO(file.getvalue()))
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            import docx
            doc = docx.Document(io.BytesIO(file.getvalue()))
            return "\n".join([p.text for p in doc.paragraphs])
        else:
            return file.getvalue().decode("utf-8")
    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier {file.name}: {e}")
        return ""

def analyze_cv(client, job_txt, cv_txt, name):
    prompt = f"""Tu es un expert en recrutement. Analyse ce CV pour le poste donné.
    Réponds UNIQUEMENT en format JSON valide.
    
    Format attendu :
    {{
      "nom_complet": "Nom du candidat",
      "score": 85,
      "points_forts": ["phrase 1", "phrase 2"],
      "points_amelioration": ["phrase 1", "phrase 2"],
      "recommandations": ["phrase 1", "phrase 2"]
    }}

    Poste : {job_txt}
    CV ({name}) : {cv_txt}
    """
    
    try:
        from mistralai.models.chat_completion import ChatMessage
        messages = [ChatMessage(role="user", content=prompt)]
        resp = client.chat(model="mistral-large-latest", messages=messages, temperature=0.1)
        content = resp.choices[0].message.content
        
        # Nettoyage du JSON si Mistral ajoute des balises ```
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].strip()
            
        return json.loads(content)
    except Exception as e:
        st.error(f"Erreur lors de l'analyse de {name} : {str(e)}")
        return None

def format_item(item: Any) -> str:
    """Transforme un dictionnaire complexe en chaîne de caractères lisible."""
    if isinstance(item, str):
        return item
    if isinstance(item, dict):
        # Cherche les clés courantes dans les objets complexes renvoyés par l'IA
        if 'details' in item:
            val = item['details']
            return " ".join(val) if isinstance(val, list) else str(val)
        if 'action' in item:
            return str(item['action'])
        if 'categorie' in item:
            return f"{item['categorie']}: {item.get('details', '')}"
        return str(item)
    return str(item)

# --- INTERFACE UTILISATEUR ---

def main():
    st.markdown('<div class="professional-header"><h1>CHECK CV</h1><p>Analyse intelligente de candidatures par IA</p></div>', unsafe_allow_html=True)
    client = init_mistral()

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown('<div class="upload-card"><h3>📄 Offre d\'emploi</h3>', unsafe_allow_html=True)
        job_f = st.file_uploader("Upload Job", type=["pdf", "txt", "docx"], label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="upload-card"><h3>👥 CV des candidats</h3>', unsafe_allow_html=True)
        cv_fs = st.file_uploader("Upload CVs", type=["pdf", "txt", "docx"], accept_multiple_files=True, label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🚀 LANCER L'ANALYSE") and job_f and cv_fs:
        job_text = extract_text(job_f)
        results = []
        bar = st.progress(0)
        status = st.empty()
        
        for i, f in enumerate(cv_fs):
            status.text(f"Analyse en cours : {f.name}...")
            res = analyze_cv(client, job_text, extract_text(f), f.name)
            if res:
                res['filename'] = f.name
                results.append(res)
            bar.progress((i + 1) / len(cv_fs))
            
        status.empty()
        st.session_state['results'] = sorted(results, key=lambda x: x['score'], reverse=True)
        st.rerun()

    if 'results' in st.session_state:
        st.markdown("<h2 style='text-align:center;'>📊 Tableaux des Résultats</h2>", unsafe_allow_html=True)
        
        for r in st.session_state['results']:
            st.markdown(f"""
            <div class="result-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h2 style="margin:0; color:#1f1f1f;">{r.get('nom_complet', 'Candidat')}</h2>
                        <small style="color:#666;">Fichier : {r.get('filename', 'Inconnu')}</small>
                    </div>
                    <div style="text-align:right">
                        <div class="score-number">{r.get('score', 0)}%</div>
                        <b style="color:#0b57d0;">MATCH SCORE</b>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

            res_cols = st.columns(3)
            
            # Définition des sections pour l'affichage
            config = [
                (res_cols[0], "points_forts", "section-strengths", "✅ Points Forts"),
                (res_cols[1], "points_amelioration", "section-improvements", "⚠️ À Améliorer"),
                (res_cols[2], "recommandations", "section-recommendations", "💡 Conseils")
            ]

            for col, key, css_class, title in config:
                with col:
                    st.markdown(f'<div class="analysis-section {css_class}"><h4>{title}</h4>', unsafe_allow_html=True)
                    items = r.get(key, [])
                    if items:
                        for item in items:
                            st.write(f"• {format_item(item)}")
                    else:
                        st.write("Aucune donnée disponible.")
                    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
