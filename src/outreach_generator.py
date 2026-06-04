from __future__ import annotations

import json

from .lead_filter_ai import summarize_prospect
from .llm import invoke_json
from .prompts import OUTREACH_PROMPT


def _fallback_outreach(lead: dict, offer: str, tone: str, sender_name: str) -> dict:
    company = lead.get("company") or "your team"
    location = lead.get("address") or lead.get("source") or "your area"
    subject = f"AI growth ideas for {company}"
    cold_email = (
        f"Hi {company} Team,\n\n"
        f"As a business in {location}, I noticed your online presence and thought {offer} could help "
        "you capture more qualified customers while saving time on manual follow-up.\n\n"
        "Would you be open to a quick conversation this week?\n\n"
        f"Best regards,\n{sender_name}"
    )
    return {
        "subject": subject,
        "cold_email": cold_email,
        "linkedin_message": (
            f"Hi {company} Team, I came across your business and had an idea for using {offer} "
            "to improve lead capture and customer follow-up. Open to a quick chat?"
        ),
        "follow_up": (
            f"Hi {company} Team, just following up on my note. I believe {offer} could create "
            "a practical growth win for your business. Would a short call make sense?"
        ),
        "tone": tone,
    }


def generate_outreach(lead: dict, offer: str, tone: str = "Professional", sender_name: str = "Amna") -> dict:
    fallback = _fallback_outreach(lead, offer, tone, sender_name)
    summary = summarize_prospect(lead, offer)
    lead_json = json.dumps(lead, indent=2, ensure_ascii=False)
    prompt = OUTREACH_PROMPT.format(
        lead=lead_json,
        offer=offer,
        tone=tone,
        sender_name=sender_name,
        lead_summary=summary,
    )
    result = invoke_json(prompt, fallback)
    cold_email = result.get("cold_email", fallback["cold_email"])

    if isinstance(cold_email, dict):
        cold_email = (
            f"{cold_email.get('greeting', '')}\n\n"
            f"{cold_email.get('body', '')}\n\n"
            f"{cold_email.get('signature', '')}"
        )

    return {
        **lead,
        "subject": result.get("subject", fallback["subject"]),
        "cold_email": cold_email,
        "linkedin_message": result.get("linkedin_message", fallback["linkedin_message"]),
        "follow_up": result.get("follow_up", fallback["follow_up"]),
        "prospect_summary": summary,
    }


def generate_bulk_outreach(
    leads: list[dict],
    offer: str,
    tone: str = "Professional",
    sender_name: str = "Amna",
) -> list[dict]:
    return [generate_outreach(lead, offer, tone, sender_name) for lead in leads]
