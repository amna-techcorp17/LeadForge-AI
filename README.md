# LeadForge AI

LeadForge AI is an AI-powered lead generation and qualification dashboard for agencies, sales teams, B2B SaaS startups, freelancers, real estate teams, recruiters, and client-demo portfolios.

It scrapes or generates business leads, filters them against target requirements, scores prospects, writes personalized outreach, exports CSV/Excel reports, and shows a modern pista and cream-white Streamlit dashboard.

## Features

- Business lead scraping with demo data and Yellow Pages support
- Company, website, email, phone, address, and source extraction
- AI lead qualification through Groq and LangChain
- Offline heuristic fallback when no API key is available
- Lead scoring with Hot, Warm, and Cold categories
- Website quality signal analysis
- AI prospect summaries
- Personalized cold email, LinkedIn message, and follow-up generation
- Bulk outreach generation
- Lead deduplication
- CSV and Excel export
- Analytics cards, pipeline chart, location quality chart, lead table, and insight panel

## Tech Stack

- Python
- Streamlit
- Selenium
- BeautifulSoup
- Pandas
- Openpyxl
- LangChain
- Groq API
- Plotly

## Project Structure

```text
leadforge-ai/
├── app.py
├── requirements.txt
├── .env.example
├── README.md
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
```

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Add your Groq key to `.env`:

```env
GROQ_API_KEY=your_api_key_here
```

Run the app:

```bash
streamlit run app.py
```

## Usage

1. Enter a niche, such as `Fitness Gym`.
2. Enter a location, such as `USA`.
3. Select requirements like `Active Website` and `Email Available`.
4. Choose the lead count and source.
5. Click `Generate Leads`.
6. Review scores, AI insights, and outreach.
7. Export CSV or Excel.

## Notes

The app works without a Groq API key using deterministic demo and heuristic logic, which makes it useful for Upwork and portfolio demonstrations. Add `GROQ_API_KEY` when you want real AI qualification and outreach generation.
