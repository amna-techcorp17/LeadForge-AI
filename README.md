# 🚀 LeadForge AI — Intelligent Lead Generation & Sales Automation Engine

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-AI%20Dashboard-red)
![LangChain](https://img.shields.io/badge/LangChain-LLM%20Pipeline-green)
![Groq](https://img.shields.io/badge/Groq-LLM%20API-purple)
![Status](https://img.shields.io/badge/Status-Portfolio%20Ready-brightgreen)

---

## 🧠 Overview

LeadForge AI is a next-generation AI-powered lead generation, qualification, and outreach automation system designed for modern sales workflows.

It acts as a mini sales intelligence engine that can discover or simulate business leads, enrich and clean raw data, evaluate lead quality using AI reasoning, score prospects (Hot / Warm / Cold), and generate personalized outreach campaigns inside a modern Streamlit dashboard.

It is built as a SaaS-style portfolio project demonstrating real-world AI automation used in agencies, startups, freelancers, and sales teams.

---

## ⚡ Key Features

### 🔍 Lead Intelligence
- AI-assisted lead discovery (scraping + fallback datasets)
- Company, email, phone, website, address extraction
- Deduplication and data cleaning pipeline

### 🧠 AI Qualification Engine
- Groq + LangChain powered lead analysis
- Smart scoring system (Hot / Warm / Cold)
- Website quality & intent signal detection
- AI-generated prospect summaries

### ✉️ Outreach Automation
- Personalized cold emails
- LinkedIn messages
- Follow-up sequences
- Bulk outreach generation

### 📊 Analytics Dashboard
- Interactive Streamlit UI
- Lead distribution charts
- Pipeline visualization
- Location-based insights
- CSV / Excel export support

### 🔄 Fallback Intelligence Mode
- Works without API keys using heuristic logic
- Ensures reliable demos for portfolios and clients

---

## 🏗️ System Architecture

User Input (Streamlit Dashboard)
        ↓
Lead Discovery Layer (Scraper / Demo Data / Yellow Pages)
        ↓
Data Processing Layer (Cleaning + Deduplication + Structuring)
        ↓
AI Qualification Layer (Groq + LangChain Reasoning)
        ↓
Lead Scoring Engine (Hot / Warm / Cold Classification)
        ↓
Outreach Generator (Emails + LinkedIn + Follow-ups)
        ↓
Analytics & Export Layer (Charts + CSV + Excel)

---

## 🧰 Tech Stack

- Python
- Streamlit
- Selenium
- BeautifulSoup
- Pandas
- Openpyxl
- LangChain
- Groq API
- Plotly

---

## 📁 Project Structure

leadforge-ai/
├── app.py
├── requirements.txt
├── .env.example
├── src/
│   ├── scrape_leads.py
│   ├── lead_filter_ai.py
│   ├── lead_scorer.py
│   ├── outreach_generator.py
│   ├── exporter.py
│   ├── prompts.py
│   ├── llm.py
│   ├── analytics.py
│   └── utils.py
├── output/
├── screenshots/
└── assets/

---

## 🚀 Installation & Setup

# Clone repository
git clone https://github.com/amna-techcorp17/LeadForge-AI.git
cd LeadForge-AI

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment file
copy .env.example .env

Add your API key:

GROQ_API_KEY=your_api_key_here

---

## ▶️ Run Application

streamlit run app.py

---

## 🧪 Workflow

1. User enters niche (e.g. SaaS, Fitness, Real Estate)
2. System collects leads via scraping or dataset
3. Data is cleaned and deduplicated
4. AI evaluates lead quality and intent
5. Leads are scored into Hot / Warm / Cold
6. Personalized outreach messages are generated
7. Dashboard shows analytics and export options

---

## 📊 Dashboard Features

- Lead scoring visualization
- Funnel analytics (Hot / Warm / Cold)
- AI insights panel
- Location-based analysis
- Export system (CSV / Excel)
- Clean SaaS-style UI

---

## 🔄 Current Version

- Intelligent lead discovery with fallback datasets for reliable demos
- AI-powered qualification with heuristic backup system
- Fully working outreach automation pipeline

---

## 🔮 Future Enhancements

- Google Places API integration
- Apollo.io integration
- Real-time business discovery
- Email verification system
- CRM integrations (HubSpot / Salesforce)
- Advanced AI enrichment using live web signals

---

## 💡 Why This Project Matters

LeadForge AI demonstrates a complete AI SaaS workflow combining:

- Data scraping and engineering
- AI-based decision making
- LLM-powered automation
- Business intelligence analytics
- Sales outreach automation

It is a production-level simulation of modern AI-driven sales systems.

---


---

## 👨‍💻 Author

Amna Chaudhary 

"Agentic AI Engineer"

---

## 📜 License

For educational and portfolio use only.

---

⭐ If you like this project, give it a star!
