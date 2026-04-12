# 🌾 Edge-Agri
### Offline, Dialect-Aware Multilingual Agricultural Advisory System

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Deploy on Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)

> An offline, voice-based agricultural advisory framework for smallholder farmers in developing nations — powered by RAG, Dialect-Aware ASR, and edge-deployable LLMs.

**Languages:** বাংলা 🇧🇩 | 中文 🇨🇳 | English 🇬🇧

---

## 🚀 Live Demo

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/YOUR_USERNAME/edge-agri/main/app.py)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 💬 **RAG Chatbot** | BRRI knowledge base powered Q&A in 3 languages |
| 🔬 **Disease Detection** | PlantVillage-based plant disease identification |
| 🌐 **Trilingual** | বাংলা / 中文 / English |
| 🔐 **Admin Panel** | Separate admin dashboard (users cannot access) |
| 📊 **Analytics** | Query logs, detection history, stats |
| 📶 **Offline Ready** | SQLite database, no cloud dependency |

---

## 🧠 Architecture

```
Farmer Query (Voice/Text/Image)
        ↓
Language Detection → RAG Controller
        ↓
FAISS / SQLite Knowledge Index (BRRI Docs)
        ↓
Quantized LLM Response (DeepSeek-R1-Distill-Llama-8B)
        ↓
Grounded Answer + Source Citation + TTS Output
```

---

## 🖥️ Screenshots

| Home | Chatbot | Disease Detection | Admin |
|------|---------|------------------|-------|
| Stats dashboard | 3-language RAG | PlantVillage AI | Secure login |

---

## 🚀 Deploy to Streamlit Cloud (Free)

### Step 1: Fork & Push to GitHub
```bash
git clone https://github.com/YOUR_USERNAME/edge-agri.git
cd edge-agri
git add .
git commit -m "Initial commit"
git push origin main
```

### Step 2: Deploy on Streamlit Cloud
1. Go to **[share.streamlit.io](https://share.streamlit.io)**
2. Click **"New app"**
3. Select your repository: `YOUR_USERNAME/edge-agri`
4. Main file: `app.py`
5. Click **"Deploy"** ✅

---

## 💻 Run Locally

```bash
git clone https://github.com/YOUR_USERNAME/edge-agri.git
cd edge-agri
pip install -r requirements.txt
streamlit run app.py
```
Open: `http://localhost:8501`

---

## 📁 Project Structure

```
edge-agri/
├── app.py                    # Main Streamlit app (all pages)
├── requirements.txt          # Python dependencies
├── .streamlit/
│   └── config.toml          # Theme configuration
├── utils/
│   ├── database.py          # SQLite DB + all CRUD operations
│   ├── translations.py      # বাংলা / 中文 / English strings
│   ├── rag_engine.py        # RAG query pipeline
│   └── disease_detector.py  # PlantVillage disease detection
├── data/                    # SQLite DB (auto-created)
└── .github/
    └── workflows/ci.yml     # GitHub Actions CI
```

---

## 🔐 Admin Access

| Username | Password |
|----------|----------|
| `admin` | `admin123` |

> ⚠️ Change password after first login in production.

---

## 🌿 Supported Plants (Disease Detection)

Apple · Blueberry · Cherry · Corn · Grape · Orange · Peach · Pepper · Potato · Raspberry · Soybean · Squash · Strawberry · Tomato

---

## 📊 Tech Stack

| Component | Technology |
|-----------|-----------|
| Framework | Streamlit |
| LLM (future) | DeepSeek-R1-Distill-Llama-8B (4-bit) |
| RAG | SQLite + keyword retrieval |
| Disease AI | PlantVillage heuristic model |
| Database | SQLite (portable, offline) |
| Auth | bcrypt password hashing |
| Language | Python 3.11 |

---

## 🎯 Performance Targets

| Metric | Target |
|--------|--------|
| Domain Accuracy | > 90% |
| Response Latency | < 2 seconds |
| Hallucination Rate | < 5% |
| Dialect Support | Chattgaiya, Sylheti, Standard Bangla |

---

## 📚 Knowledge Sources
- Bangladesh Rice Research Institute (BRRI) Manuals
- Krishi Batayan Government Portal
- Expert Interview Transcripts

## 📞 Agricultural Helpline: **16123**

## 📄 License: MIT
