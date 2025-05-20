
# 🚀 AI Career Counselor

![AI Career Counselor](streamlit_app/assets/logo.png) <!-- Replace with actual logo if available -->

> An intelligent, all-in-one career guidance platform powered by AI — helping users discover the right career path, identify skill gaps, and plan their future with confidence.

---

## 📌 Table of Contents

- [✨ Features](#-features)
- [🧠 How It Works](#-how-it-works)
- [🛠️ Tech Stack](#-tech-stack)
- [⚙️ Installation](#️-installation)
- [📁 Project Structure](#-project-structure)
- [🙌 Acknowledgements](#-acknowledgements)
- [📝 License](#-license)

---

## ✨ Features

🔍 **Career Prediction**  
Predicts the most suitable career options based on your resume and personality quiz using a custom-trained ML model.

📄 **Resume Parsing**  
Automatically extracts skills, experience, and education from uploaded resumes (PDF format).

🧠 **Personality Quiz**  
Assesses personality traits using a GPT-based text generation model to personalize career recommendations.

📊 **Skills Gap Filler**  
Highlights missing skills for a selected career path and recommends relevant upskilling areas.

💬 **AI Chatbot Counselor**  
Chat with an AI assistant for guidance, FAQs, and personalized advice.

📥 **Downloadable Reports**  
Generate and download a complete PDF report of your career prediction, quiz results, and skill gaps.

🎨 **Modern UI**  
Beautiful, responsive, and interactive Streamlit interface with animations and dynamic effects.

---

## 🧠 How It Works

1. **Upload Resume** → Skills extracted using NLP and regex.
2. **Take Personality Quiz** → GPT-based generation + scoring logic.
3. **Career Prediction** → ML model predicts best-fit careers.
4. **Chatbot** → LLM-powered career Q&A system.
5. **Skills Gap Analysis** → Compares your skills with ideal role requirements.
6. **PDF Report** → All outputs are saved and downloadable in a neat PDF format.

---

## 🛠️ Tech Stack

| Category       | Tools Used |
|----------------|------------|
| Frontend       | Streamlit, Lottie |
| Backend        | Python, FastAPI (optional) |
| AI/ML          | Scikit-learn, Transformers (Hugging Face), GPT-2 / Open-source LLM |
| NLP            | spaCy, PyMuPDF (fitz) |
| PDF Generation | FPDF + DejaVuSans (Unicode font) |
| Deployment     | Streamlit Cloud / Local |
| Miscellaneous  | base64, io, re, json |

---

## ⚙️ Installation

### 🔧 Prerequisites

- Python 3.8+
- pip or conda
- Git

### 🔌 Clone the Repository

```bash
git clone https://github.com/yourusername/ai-career-counselor.git
cd ai-career-counselor
```

### 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

> ⚠️ Ensure you have PyTorch installed for transformers:
```bash
pip install torch
```

### ▶️ Run the App

```bash
streamlit run streamlit_app/app.py
```

---

## 📁 Project Structure

```
ai-career-counselor/
│
├── streamlit_app/
│   ├── app.py                    # Main Streamlit application
│   ├── chatbot.py                # LLM chatbot logic (free API or OpenAI)
│   ├── predictor.py              # ML model for career prediction
│   ├── resume_parser.py          # Resume skills extractor using PyMuPDF & spaCy
│   ├── personality_quiz.py       # Quiz logic + GPT generation
│   ├── utils.py                  # Helper functions
│   ├── fonts/
│   │   └── DejaVuSans.ttf        # Unicode font for PDF generation
│   └── assets/
│       └── animations.json       # Lottie animations
│
├── requirements.txt              # All required dependencies
└── README.md                     # You're here!
```

---

## 🙌 Acknowledgements

- [Streamlit](https://streamlit.io/) – For the rapid UI development.
- [Hugging Face Transformers](https://huggingface.co/transformers/) – Text generation and NLP pipelines.
- [FPDF2](https://pyfpdf.github.io/fpdf2/) – PDF report generation.
- [Together.ai / OpenAI / Ollama](https://together.ai/) – For free/paid chatbot APIs.

---

 

## 💡 Future Enhancements

- User authentication and dashboard
- Database integration (MongoDB/Firebase)
- Real-time resume scoring
- API-based job matching system

---

Made with ❤️ by [Hardik](https://github.com/hardikkothari2023)
