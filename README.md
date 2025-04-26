# 🤖 AI-Powered Resume Analyzer

An intelligent web app that analyzes resumes against a given job description to determine the best fit, suggest improvements, and provide detailed insights using AI and Natural Language Processing (NLP).

Built with **FastAPI**, **Streamlit**, and **Plotly** for a smooth and interactive experience.

---

## 🚀 Features

- 🔍 Upload **multiple resumes** (PDF, DOCX)
- 📝 Upload a **job description** (PDF, DOCX, TXT)
- 📈 Get **Fit Scores** for each resume
- 🔥 Identify **missing skills** and receive **improvement suggestions**
- 🏆 See **Best Matches** (85%+ Fit Score)
- 📊 View **Summary Insights** (Average, Above Average, Weak Matches)
- 📉 Interactive **bar and pie charts** (Plotly)
- 📥 Download full **analysis reports** and **CSV summary**

---

## 🛠️ Tech Stack

| Tech | Description |
|:---|:---|
| [FastAPI](https://fastapi.tiangolo.com/) | Backend API for resume and job description analysis |
| [Streamlit](https://streamlit.io/) | Frontend interface for uploading and viewing results |
| [Plotly](https://plotly.com/python/) | Beautiful, interactive charts |
| [Python Libraries] | NLP and parsing (e.g., PyMuPDF, docx, spaCy) |

---

## 📂 Project Structure

```plaintext
ai-resume-analyzer/
├── backend/
│   ├── main.py        # FastAPI application
│   ├── services/
│   │   ├── resume_parser.py
│   │   ├── job_description_parser.py
│   │   └── analysis.py
│   └── utils/
│       └── skill_extractor.py
├── frontend/
│   └── app.py         # Streamlit frontend
├── README.md
├── requirements.txt
└── LICENSE
```

---

## 📦 Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/ai-resume-analyzer.git
cd ai-resume-analyzer
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## 🖥️ Running the App Locally

### Start the Backend (FastAPI)
```bash
cd backend
uvicorn main:app --reload
```

FastAPI will run at [http://localhost:8000](http://localhost:8000)

---

### Start the Frontend (Streamlit)
In a new terminal:

```bash
cd frontend
streamlit run app.py
```

Streamlit will run at [http://localhost:8501](http://localhost:8501)

---

## 📸 Screenshots



---

## ✨ Future Improvements

- ✅ Better semantic matching (not just keyword-based)
- ✅ Use AI embeddings (e.g., OpenAI, HuggingFace) for more intelligent fit scoring
- ✅ Email notifications for candidates
- ✅ Mobile responsive frontend
- ✅ Dockerize for production deployment

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!  
Feel free to open a pull request or create an issue.

---

## 📜 License

Distributed under the MIT License.  
See `LICENSE` for more information.

---

## 🙌 Acknowledgements

- [Streamlit](https://streamlit.io/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [spaCy](https://spacy.io/)
- [Plotly](https://plotly.com/)

---
