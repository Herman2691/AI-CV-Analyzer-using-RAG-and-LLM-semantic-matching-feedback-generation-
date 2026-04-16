# 🎯AI CV Analyzer using RAG and LLM (semantic matching + feedback generation)
#Projet réaliser par HERMAN KANDOLO chercheur en IA

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

Une application web moderne et professionnelle qui utilise l'intelligence artificielle (Mistral AI) pour analyser et classer automatiquement des CV par rapport à une offre d'emploi.

## ✨ Fonctionnalités

- 🤖 **Analyse IA avancée** : Utilise Mistral AI pour une évaluation précise des candidatures
- 📊 **Scoring intelligent** : Attribution d'un score de 0 à 100% pour chaque candidat
- 🎨 **Interface moderne** : Design professionnel avec animations et effets visuels
- 📈 **Classement automatique** : Tri des candidats par score décroissant
- 📑 **Analyse détaillée** : Points forts, axes d'amélioration et recommandations pour chaque CV
- 📥 **Export multi-format** : Téléchargement des résultats en JSON et PDF
- 📊 **Statistiques en temps réel** : Dashboard avec métriques de l'analyse
- 🚀 **Traitement par lots** : Analyse jusqu'à 100 CV simultanément

## 🛠️ Technologies utilisées

- **Frontend** : Streamlit avec CSS personnalisé
- **IA** : Mistral AI (modèle mistral-large-latest)
- **Traitement de fichiers** : PyPDF2, python-docx
- **Génération PDF** : ReportLab
- **Backend** : Python 3.8+

## 📋 Prérequis

- Python 3.8 ou supérieur
- Clé API Mistral AI (gratuite sur [console.mistral.ai](https://console.mistral.ai))
- pip (gestionnaire de paquets Python)

## 🚀 Installation

### 1. Cloner le projet

```bash
git clone https://github.com/Herman2691/check-cv.git
cd check-cv
```

### 2. Créer un environnement virtuel

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configuration de l'API

Créez un fichier `.env` à la racine du projet :

```env
MISTRAL_API_KEY=votre_cle_api_mistral
```

Pour obtenir votre clé API :
1. Créez un compte sur [console.mistral.ai](https://console.mistral.ai)
2. Accédez à la section "API Keys"
3. Générez une nouvelle clé
4. Copiez-la dans le fichier `.env`

## 📦 Fichier requirements.txt

```txt
streamlit==1.29.0
mistralai==0.1.0
python-dotenv==1.0.0
PyPDF2==3.0.1
python-docx==1.1.0
reportlab==4.0.7
```

## 💻 Utilisation

### Lancer l'application

```bash
streamlit run HeckCV_pro.py
```

L'application s'ouvrira automatiquement dans votre navigateur à l'adresse `http://localhost:8501`

### Guide d'utilisation

1. **Charger l'offre d'emploi** : Uploadez le fichier de l'offre (TXT, PDF ou DOCX)
2. **Charger les CV** : Uploadez les CV des candidats (jusqu'à 100 fichiers)
3. **Lancer l'analyse** : Cliquez sur le bouton "🚀 LANCER L'ANALYSE"
4. **Consulter les résultats** : Visualisez les candidats classés par score
5. **Exporter** : Téléchargez les résultats en JSON ou PDF

## 📊 Formats de fichiers supportés

- **TXT** : Fichiers texte brut
- **PDF** : Documents PDF (extraction automatique du texte)
- **DOCX** : Documents Microsoft Word

## 🎯 Système de notation

L'application attribue un score de 0 à 100% basé sur :

- ✅ **Excellent (80-100%)** : Candidat hautement qualifié
- ✔️ **Bon (60-79%)** : Bon profil avec quelques ajustements
- ○ **Moyen (40-59%)** : Profil acceptable nécessitant des améliorations
- ⚠️ **Faible (0-39%)** : Profil peu adapté au poste

## 📁 Structure du projet

```
heck-cv/
│
├── HeckCV_pro.py          # Application principale
├── .env                    # Configuration (clé API)
├── requirements.txt        # Dépendances Python
├── README.md              # Documentation
│
└── exports/               # Dossier des exports (créé automatiquement)
    ├── json/
    └── pdf/
```

## 🔧 Fonctionnalités avancées

### Analyse détaillée

Chaque CV analysé reçoit :
- Un score d'adéquation global
- 3 à 5 points forts identifiés
- 3 à 5 axes d'amélioration
- 3 à 5 recommandations concrètes

### Export PDF

Le rapport PDF inclut :
- Résumé de l'analyse avec statistiques
- Détails pour chaque candidat
- Mise en page professionnelle
- Données triées par score décroissant

### Export JSON

Format structuré incluant :
- Date et heure de l'analyse
- Nombre total de candidats
- Résultats détaillés pour chaque CV

## 🐛 Résolution de problèmes

### Erreur "API Key not found"

Vérifiez que :
- Le fichier `.env` existe à la racine du projet
- La clé API est correctement formatée : `MISTRAL_API_KEY=votre_cle`
- Il n'y a pas d'espaces avant ou après le signe `=`

### Erreur lors de la lecture de PDF

Installez ou mettez à jour PyPDF2 :
```bash
pip install --upgrade PyPDF2
```

### Problème d'encodage

Assurez-vous que vos fichiers sont en UTF-8.

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Forkez le projet
2. Créez une branche (`git checkout -b feature/amelioration`)
3. Committez vos changements (`git commit -m 'Ajout d'une fonctionnalité'`)
4. Pushez vers la branche (`git push origin feature/amelioration`)
5. Ouvrez une Pull Request

## 📝 Roadmap

- [ ] Support de plus de formats (ODT, RTF)
- [ ] Analyse multilingue avancée
- [ ] Comparaison directe entre candidats
- [ ] Génération automatique de lettres de refus/acceptation
- [ ] Intégration avec les ATS (Applicant Tracking Systems)
- [ ] API REST pour intégration externe

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👤 Auteur

**Votre Nom: KANDOLO HERMAN
- GitHub: [Herman2691](https://github.com/Herman269)
- LinkedIn: [Votre Profil](https://linkedin.com/in/votre-profil)
- lien pour tester l'application: https://checkcv2-2025.streamlit.app
## 🙏 Remerciements

- [Mistral AI](https://mistral.ai) pour leur excellent modèle d'IA
- [Streamlit](https://streamlit.io) pour le framework d'application web
- La communauté open source pour les bibliothèques utilisées

## 📞 Support

Pour toute question ou problème :
- Ouvrez une issue sur GitHub
- Contactez-moi par email : votre.email@example.com

---

⭐ Si ce projet vous aide, n'oubliez pas de lui donner une étoile sur GitHub !
