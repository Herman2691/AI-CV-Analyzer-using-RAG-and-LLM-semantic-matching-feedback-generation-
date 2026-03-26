"""
CHECK CV - Version Intégrale avec Export PDF & JSON
Basé sur l'architecture RAG / LLM Mistral & ReportLab
"""

from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from mistralai.client import MistralClient
import json
from typing import List, Dict, Any
import io
from datetime import datetime

# Import pour la génération PDF (ReportLab)
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

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
        background: white; padding: 40px; border-radius: 24px; 
        margin-bottom: 30px; border: 1px solid #e3e3e3; text-align: center;
    }
    .professional-header h1 { color: #1f1f1f; font-size: 2.5em; font-weight: 500; margin: 0; }

    .upload-card, .result-card {
        background: white; border-radius: 24px; padding: 25px;
        border: 1px solid #e3e3e3; margin-bottom: 20px;
    }

    .score-number { font-size: 3em; font-weight: 500; color: #0b57d0; line-height: 1; }

    .analysis-section {
        border-radius: 16px; padding: 20px; margin-top: 15px;
        height: 100%; color: #ffffff !important;
    }
    .section-strengths { background-color: #1a73e8; } 
    .section-improvements { background-color: #f9ab00; }
    .section-recommendations { background-color: #34a853; }

    .analysis-section h4 { color: #ffffff !important; text-transform: uppercase; font-size: 0.9em; letter-spacing: 1px; margin-bottom: 15px; }
    .analysis-section p, .analysis-section li, .analysis-section div { color: #ffffff !important; font-size: 0.95em; line-height: 1.5; }

    .stButton > button {
        background-color: #0b57d0 !important; color: white !important;
        border-radius: 100px !important; padding: 12px 30px !important;
        width: 100%; border: none !important; font-weight: 500;
    }
    .export-container { display: flex; gap: 10px; justify-content: center; margin-bottom: 30px; }
    </style>
""", unsafe_allow_html=True)

# --- LOGIQUE MISTRAL ---

@st.cache_resource
def init_mistral():
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        st.error("Clé API Mistral manquante.")
        st.stop()
    return MistralClient(api_key=api_key)

def extract_text(file) -> str:
    try:
        if file.type == "application/pdf":
            import PyPDF2
            reader = PyPDF2.PdfReader(io.BytesIO(file.getvalue()))
            return "\n".join([p.extract_text() for p in reader.pages])
        elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            import docx
            doc = docx.Document(io.BytesIO(file.getvalue()))
            return "\n".join([p.text for p in doc.paragraphs])
        return file.getvalue().decode("utf-8")
    except Exception as e:
        return f"Erreur lecture: {str(e)}"

def analyze_cv(client, job_txt, cv_txt, name):
    prompt = f"""Expert RH. Analyse ce CV pour le poste. Réponds en JSON uniquement.
    Format : {{
      "nom_complet": "Nom", "score": 85,
      "points_forts": ["..."], "points_amelioration": ["..."], "recommandations": ["..."]
    }}
    Poste: {job_txt} | CV: {cv_txt}"""
    
    try:
        from mistralai.models.chat_completion import ChatMessage
        resp = client.chat(model="mistral-large-latest", messages=[ChatMessage(role="user", content=prompt)], temperature=0.1)
        content = resp.choices[0].message.content
        if "
