from __future__ import annotations

from .llm import invoke_json
from .prompts import QUALIFICATION_PROMPT, SUMMARY_PROMPT
from .utils import clean_text


def _heuristic_match(lead: dict, niche: str, requirements: list[str]) -> dict:
    haystack = " ".join(str(value).lower() for value in lead.values())
    niche_terms = [term for term in clean_text(niche).lower().split() if len(term) > 2]
    niche_match = not niche_terms or any(term in haystack for term in niche_terms)

    checks = {
        "Active Website": bool(lead.get("website")),
        "Email Available": bool(lead.get("email")),
        "Phone Available": bool(lead.get("phone")),
    }
    req_match = all(checks.get(req, True) for req in requirements)
    relevant = niche_match and req_match

    missing = [name for name, ok in checks.items() if name in requirements and not ok]
    reason = "Matches target niche and required contact fields."
    if missing:
        reason = f"Missing required field: {', '.join(missing)}."
    elif not niche_match:
        reason = "Business data does not strongly match the target niche."

    return {"relevant": relevant, "reason": reason, "confidence": 86 if relevant else 58}


def qualify_lead(lead: dict, niche: str, location: str, requirements: list[str]) -> dict:
    fallback = _heuristic_match(lead, niche, requirements)
    prompt = QUALIFICATION_PROMPT.format(
        niche=niche,
        location=location,
        requirements="\n".join(f"- {item}" for item in requirements) or "- None",
        lead=lead,
    )
    result = invoke_json(prompt, fallback)
    return {
        **lead,
        "relevant": bool(result.get("relevant")),
        "qualification_reason": result.get("reason", fallback["reason"]),
        "qualification_confidence": int(result.get("confidence", fallback["confidence"])),
    }


def qualify_leads(leads: list[dict], niche: str, location: str, requirements: list[str]) -> list[dict]:
    return [qualify_lead(lead, niche, location, requirements) for lead in leads]


def summarize_prospect(lead: dict, offer: str) -> str:
    fallback = (
        f"{lead.get('company', 'This business')} has visible contact signals and may be a fit for "
        f"{offer.lower()}."
    )
    result = invoke_json(SUMMARY_PROMPT.format(lead=lead, offer=offer), {"summary": fallback})
    return str(result.get("summary", fallback))
