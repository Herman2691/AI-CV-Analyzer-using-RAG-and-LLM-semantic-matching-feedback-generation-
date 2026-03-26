from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from mistralai.client import MistralClient
import json
from typing import List, Dict
import io
from datetime import datetime
import time

# ---------------- CONFIG ----------------
st.set_page_config(page_title="CHECK CV", layout="wide")

# ---------------- INIT MISTRAL ----------------
@st.cache_resource
def init_mistral():
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        st.error("Clé API manquante")
        st.stop()
    return MistralClient(api_key=api_key)

# ---------------- EXTRACT TEXT ----------------
def extract_text_from_file(uploaded_file):
    try:
        if uploaded_file.type == "application/pdf":
            import PyPDF2
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.getvalue()))
            return "".join([p.extract_text() for p in pdf_reader.pages])
        else:
            return uploaded_file.getvalue().decode("utf-8")
    except:
        return ""

# ---------------- ANALYSE MISTRAL ----------------
def analyze_cv_with_mistral(client, job_description, cv_content, cv_name):

    prompt = f"""
Analyse ce CV et retourne UNIQUEMENT un JSON :

Offre:
{job_description}

CV:
{cv_content}

Format:
{{
"nom_complet": "",
"score": 0,
"points_forts": [],
"points_amelioration": [],
"recommandations": []
}}
"""

    try:
        # ✅ CORRECTION ICI
        response = client.chat(
            model="mistral-large-latest",
            messages=[{"role": "user", "content": prompt}]
        )

        content = response.choices[0].message["content"]

        if "```" in content:
            content = content.replace("```json", "").replace("```", "").strip()

        result = json.loads(content)

        return result

    except Exception as e:
        st.error(f"Erreur {cv_name}: {str(e)}")
        return None

# ---------------- MAIN ----------------
def main():

    st.title("CHECK CV")

    client = init_mistral()

    job_file = st.file_uploader("Offre", type=["txt", "pdf"])
    cv_files = st.file_uploader("CVs", accept_multiple_files=True)

    if st.button("Analyser"):

        job_text = extract_text_from_file(job_file)
        results = []

        for cv in cv_files:
            cv_text = extract_text_from_file(cv)

            res = analyze_cv_with_mistral(client, job_text, cv_text, cv.name)

            if res:
                results.append(res)

        st.write(results)

if __name__ == "__main__":
    main()
