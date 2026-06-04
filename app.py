from __future__ import annotations

import plotly.express as px
import streamlit as st

from src.analytics import ai_recommendations, build_metrics, location_dataframe, status_dataframe
from src.exporter import export_csv_bytes, export_excel_bytes
from src.lead_filter_ai import qualify_leads
from src.lead_scorer import score_leads
from src.outreach_generator import generate_bulk_outreach
from src.scrape_leads import scrape_leads
from src.utils import to_dataframe


st.set_page_config(page_title="LeadForge AI", page_icon="LF", layout="wide")


CUSTOM_CSS = """
<style>
:root {
    --cream: #fffaf0;
    --cream-2: #fffdf6;
    --pista: #d7ead2;
    --pista-2: #8fbd88;
    --ink: #20312a;
    --muted: #627469;
    --line: #dfe8d8;
}

.stApp {
    background:
        radial-gradient(circle at top right, rgba(215, 234, 210, 0.82), transparent 34rem),
        linear-gradient(135deg, #fffaf0 0%, #fbf8ee 48%, #edf6e8 100%);
    color: var(--ink);
}

[data-testid="stHeader"] {
    background: rgba(255, 250, 240, 0.72);
    border-bottom: 1px solid rgba(223, 232, 216, 0.8);
}

.block-container {
    max-width: 1500px;
    padding: 1.4rem 2rem 2rem;
}

h1, h2, h3, p, label, .stCaptionContainer {
    color: var(--ink) !important;
    letter-spacing: 0;
}

.control-panel {
    position: sticky;
    top: 5rem;
    background: rgba(255, 250, 240, 0.96);
    border: 1px solid #c8d8c1;
    border-right: 2px solid #8fb985;
    border-radius: 8px;
    padding: 18px;
    box-shadow: 18px 0 34px rgba(70, 92, 67, 0.16), 0 18px 45px rgba(70, 92, 67, 0.10);
}

.brand-card {
    background: linear-gradient(135deg, #d7ead2, #fffdf6);
    border: 1px solid #cfe1c8;
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 18px;
}

.brand-mark {
    width: 42px;
    height: 42px;
    display: grid;
    place-items: center;
    background: #20312a;
    color: #fffaf0;
    border-radius: 8px;
    font-weight: 900;
    margin-bottom: 12px;
}

.brand-card h2 {
    font-size: 1.35rem;
    margin: 0 0 6px 0;
}

.brand-card p {
    color: var(--muted) !important;
    margin: 0;
    font-size: 0.92rem;
}

.hero {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.96), rgba(244, 250, 239, 0.9));
    border: 1px solid rgba(156, 200, 154, 0.34);
    border-radius: 8px;
    padding: 28px 32px;
    box-shadow: 0 18px 45px rgba(70, 92, 67, 0.12);
}

.hero h1 {
    font-size: clamp(2.3rem, 4.4vw, 4rem);
    line-height: 1.02;
    margin: 0 0 0.65rem 0;
}

.hero p {
    color: var(--muted) !important;
    max-width: 960px;
    margin: 0;
    font-size: 1.04rem;
}

.metric-card, .section-shell {
    background: rgba(255, 255, 255, 0.9);
    border: 1px solid var(--line);
    border-radius: 8px;
    box-shadow: 0 14px 34px rgba(70, 92, 67, 0.09);
}

.metric-card {
    padding: 15px 16px;
    min-height: 104px;
}

.metric-card span {
    color: var(--muted);
    font-size: 0.86rem;
}

.metric-card strong {
    display: block;
    color: var(--ink);
    font-size: 1.9rem;
    margin-top: 8px;
}

.section-shell {
    padding: 18px;
}

.insight {
    border-left: 4px solid var(--pista-2);
    background: rgba(215, 234, 210, 0.44);
    border-radius: 8px;
    padding: 12px 14px;
    color: var(--ink);
    margin-bottom: 10px;
}

.status-pill {
    display: inline-block;
    padding: 5px 10px;
    border-radius: 999px;
    background: var(--pista);
    color: var(--ink);
    font-weight: 700;
    font-size: 0.8rem;
}

.empty-state {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.94), rgba(244, 250, 239, 0.86));
    border: 1px dashed #9fc99a;
    border-radius: 8px;
    padding: 34px;
    min-height: 300px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    box-shadow: 0 14px 34px rgba(70, 92, 67, 0.08);
}

.empty-state h2 {
    margin: 0 0 10px 0;
    font-size: 1.8rem;
}

.empty-state p {
    color: var(--muted) !important;
    max-width: 740px;
    margin: 0;
    font-size: 1rem;
}

.stButton > button, .stDownloadButton > button {
    background: #d7ead2;
    color: #15241c;
    border: 1px solid #9fc99a;
    border-radius: 8px;
    font-weight: 700;
    min-height: 42px;
}

.stButton > button:hover, .stDownloadButton > button:hover {
    background: #c4e0bf;
    color: #0f1d16;
    border-color: #8fbd88;
}

div[data-testid="stFormSubmitButton"] button {
    background: #d7ead2 !important;
    color: #20312a !important;
    border: 1px solid #9fc99a !important;
    box-shadow: 0 10px 22px rgba(70, 92, 67, 0.10) !important;
}

div[data-testid="stFormSubmitButton"] button:hover {
    background: #c4e0bf !important;
    border-color: #8fbd88 !important;
    color: #20312a !important;
}

div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea,
div[data-baseweb="select"] > div,
div[data-baseweb="input"] input {
    background: #fffdf6 !important;
    color: #20312a !important;
    border: 1px solid #d7e4cf !important;
    border-radius: 8px !important;
    box-shadow: none !important;
}

div[data-baseweb="select"] span,
div[data-baseweb="select"] svg {
    color: #20312a !important;
    fill: #20312a !important;
}

span[data-baseweb="tag"] {
    background: #d7ead2 !important;
    color: #20312a !important;
    border: 1px solid #bfd9ba !important;
    border-radius: 8px !important;
}

span[data-baseweb="tag"] span {
    color: #20312a !important;
}

[data-testid="stDataFrame"] {
    border: 1px solid var(--line);
    border-radius: 8px;
}

@media (max-width: 980px) {
    .control-panel {
        position: static;
    }
    .block-container {
        padding: 1rem;
    }
}
</style>
"""


st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

APP_STATE_VERSION = "leadforge-empty-dynamic-v2"


def build_fast_preview_leads() -> list[dict]:
    raw = scrape_leads(niche="Fitness Gym", location="USA", limit=12, source="Demo")
    preview = []
    for lead in raw:
        relevant = bool(lead.get("website") and lead.get("email"))
        preview.append(
            {
                **lead,
                "relevant": relevant,
                "qualification_reason": "Matches target filters." if relevant else "Missing website or email.",
            }
        )

    scored = score_leads(preview)
    enriched = []
    for lead in scored:
        company = lead.get("company", "your team")
        enriched.append(
            {
                **lead,
                "prospect_summary": (
                    f"{company} has useful contact signals and looks suitable for AI-powered "
                    "marketing automation and lead follow-up."
                ),
                "subject": f"AI growth ideas for {company}",
                "cold_email": (
                    f"Hi {company} Team,\n\n"
                    "I noticed your business online and believe AI-powered marketing automation "
                    "could help you capture more qualified customers and improve follow-up.\n\n"
                    "Would you be open to a quick conversation this week?\n\n"
                    "Best regards,\nAmna"
                ),
                "linkedin_message": (
                    f"Hi {company} Team, I came across your business and had an idea for improving "
                    "lead capture and customer follow-up with AI automation. Open to a quick chat?"
                ),
                "follow_up": (
                    f"Hi {company} Team, just following up on my note. I think there is a practical "
                    "growth opportunity here. Would a short call make sense?"
                ),
            }
        )
    return enriched


@st.cache_data(show_spinner=False)
def run_pipeline(
    niche: str,
    location: str,
    lead_count: int,
    source: str,
    requirements: list[str],
    offer: str,
    tone: str,
    sender_name: str,
) -> list[dict]:
    scraper_source = "Yellow Pages" if source == "Live Directory" else "Demo"
    raw = scrape_leads(niche=niche, location=location, limit=lead_count, source=scraper_source)
    qualified = qualify_leads(raw, niche=niche, location=location, requirements=requirements)
    scored = score_leads(qualified)
    return generate_bulk_outreach(scored, offer=offer, tone=tone, sender_name=sender_name)


if st.session_state.get("app_state_version") != APP_STATE_VERSION:
    st.session_state.app_state_version = APP_STATE_VERSION
    st.session_state.leads = []


control_col, dashboard_col = st.columns([0.28, 1], gap="large")

with control_col:
    st.markdown('<div class="control-panel">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="brand-card">
            <div class="brand-mark">LF</div>
            <h2>LeadForge AI</h2>
            <p>Find, qualify, score, and export B2B leads.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("lead_controls"):
        niche = st.text_input("Niche", placeholder="Example: Fitness gyms, dentists, real estate agents")
        location = st.text_input("Location", placeholder="Example: New York, USA")
        lead_count = st.slider("Lead Count", min_value=5, max_value=50, value=12, step=1)
        source = st.selectbox("Lead Source", ["Live Directory", "Demo Fallback"], index=0)
        requirements = st.multiselect(
            "Qualification Filters",
            ["Active Website", "Email Available", "Phone Available"],
            default=["Active Website", "Email Available"],
        )
        offer = st.text_area(
            "Offer",
            placeholder="Example: AI-powered marketing automation for local businesses",
            height=92,
        )
        tone = st.selectbox("Outreach Tone", ["Professional", "Friendly", "Sales", "Corporate"], index=0)
        sender_name = st.text_input("Sender Name", placeholder="Example: Amna")
        run_button = st.form_submit_button("Generate Leads", use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

if run_button:
    if not niche.strip() or not location.strip() or not offer.strip() or not sender_name.strip():
        st.warning("Please enter niche, location, offer, and sender name to generate leads.")
    else:
        with st.spinner("Scraping, qualifying, scoring, and writing outreach..."):
            st.session_state.leads = run_pipeline(
                niche=niche,
                location=location,
                lead_count=lead_count,
                source=source,
                requirements=requirements,
                offer=offer,
                tone=tone,
                sender_name=sender_name,
            )

leads = st.session_state.leads
has_leads = bool(leads)
metrics = build_metrics(leads)
frame = to_dataframe(leads)

if has_leads and source == "Live Directory":
    yellow_pages_count = sum(1 for lead in leads if lead.get("source") == "Yellow Pages")
    fallback_count = len(leads) - yellow_pages_count
    if yellow_pages_count == 0:
        st.warning(
            "Live Directory lookup did not return any Yellow Pages leads. "
            "It may be falling back to demo data due to website blocking or environment restrictions."
        )
    elif fallback_count > 0:
        st.info(
            f"Live Directory returned {yellow_pages_count} Yellow Pages leads and "
            f"{fallback_count} fallback leads."
        )
    else:
        st.success("Live Directory returned real Yellow Pages leads.")

with dashboard_col:
    st.markdown(
        """
        <div class="hero">
            <h1>LeadForge AI</h1>
            <p>Scrape prospects, qualify them with AI, score buying intent, generate personalized outreach, and export a polished lead report for sales teams and agencies.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not has_leads:
        st.write("")
        st.markdown(
            """
            <div class="empty-state">
                <h2>Start a New Lead Search</h2>
                <p>Enter your target niche, location, qualification filters, offer, and sender name from the left panel. Your analytics, qualified leads, outreach messages, and exports will appear here after generation.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.stop()

    st.write("")
    metric_cols = st.columns(6)
    metric_labels = {
        "Total Leads": "Total Leads",
        "Qualified Leads": "Qualified",
        "Hot Leads": "Hot Leads",
        "Warm Leads": "Warm Leads",
        "Cold Leads": "Cold Leads",
        "Average Score": "Avg Score",
    }
    for col, (label, value) in zip(metric_cols, metrics.items()):
        with col:
            st.markdown(
                f"""<div class="metric-card"><span>{metric_labels.get(label, label)}</span><strong>{value}</strong></div>""",
                unsafe_allow_html=True,
            )

    st.write("")
    chart_left, chart_right = st.columns([1, 1])
    with chart_left:
        st.markdown('<div class="section-shell">', unsafe_allow_html=True)
        st.subheader("Lead Pipeline")
        status_df = status_dataframe(leads)
        fig = px.pie(
            status_df,
            names="status",
            values="count",
            hole=0.58,
            color="status",
            color_discrete_map={
                "Hot Lead": "#7eb77f",
                "Warm Lead": "#e9c46a",
                "Cold Lead": "#c8c8bd",
            },
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#20312a",
            margin=dict(l=10, r=10, t=10, b=10),
            legend_title_text="",
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with chart_right:
        st.markdown('<div class="section-shell">', unsafe_allow_html=True)
        st.subheader("Location Quality")
        loc_df = location_dataframe(leads)
        bar = px.bar(
            loc_df,
            x="location",
            y="average_score",
            color="average_score",
            color_continuous_scale=["#f2ead6", "#d7ead2", "#85b77f"],
        )
        bar.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#20312a",
            margin=dict(l=10, r=10, t=10, b=10),
            coloraxis_showscale=False,
            xaxis_title="",
            yaxis_title="Avg Score",
        )
        st.plotly_chart(bar, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    table_col, insight_col = st.columns([1.55, 0.85])
    with table_col:
        st.markdown('<div class="section-shell">', unsafe_allow_html=True)
        st.subheader("Qualified Lead Table")
        visible = frame[
            [
                "company",
                "website",
                "email",
                "phone",
                "address",
                "source",
                "score",
                "status",
                "qualification_reason",
            ]
        ].rename(
            columns={
                "company": "Company",
                "website": "Website",
                "email": "Email",
                "phone": "Phone",
                "address": "Address",
                "score": "Score",
                "status": "Status",
                "qualification_reason": "AI Reason",
            }
        )
        st.dataframe(visible, use_container_width=True, hide_index=True, height=420)

        export_a, export_b = st.columns(2)
        with export_a:
            st.download_button(
                "Download CSV",
                data=export_csv_bytes(leads),
                file_name="leadforge_ai_leads.csv",
                mime="text/csv",
                use_container_width=True,
            )
        with export_b:
            st.download_button(
                "Download Excel",
                data=export_excel_bytes(leads),
                file_name="leadforge_ai_leads.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    with insight_col:
        st.markdown('<div class="section-shell">', unsafe_allow_html=True)
        st.subheader("AI Insights")
        for item in ai_recommendations(leads):
            st.markdown(f'<div class="insight">{item}</div>', unsafe_allow_html=True)

        hot_leads = frame[frame["status"] == "Hot Lead"]
        default_index = 0
        if not hot_leads.empty:
            default_company = hot_leads.iloc[0]["company"]
            default_index = int(frame.index[frame["company"].eq(default_company)][0])

        selected_company = st.selectbox("Outreach Preview", frame["company"].tolist(), index=default_index)
        selected = next((lead for lead in leads if lead.get("company") == selected_company), leads[0] if leads else {})
        st.markdown(f'<span class="status-pill">{selected.get("status", "Lead")}</span>', unsafe_allow_html=True)
        st.write("")
        st.caption("Prospect Summary")
        st.write(selected.get("prospect_summary", ""))
        st.caption("Subject")
        st.write(selected.get("subject", ""))
        st.caption("Cold Email")
        st.text_area("Cold Email", value=selected.get("cold_email", ""), height=220, label_visibility="collapsed")
        st.caption("LinkedIn Message")
        st.text_area("LinkedIn", value=selected.get("linkedin_message", ""), height=120, label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)
