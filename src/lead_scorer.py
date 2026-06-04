from __future__ import annotations


def analyze_website_quality(lead: dict) -> dict:
    website = bool(lead.get("website"))
    email = bool(lead.get("email"))
    phone = bool(lead.get("phone"))
    quality_score = 0
    quality_score += 45 if website else 0
    quality_score += 25 if email else 0
    quality_score += 15 if phone else 0
    quality_score += 15 if lead.get("address") else 0

    if quality_score >= 80:
        label = "Professional"
    elif quality_score >= 50:
        label = "Basic"
    else:
        label = "Needs Review"
    return {"website_quality": label, "website_quality_score": quality_score}


def score_lead(lead: dict) -> dict:
    score = 0
    score += 20 if lead.get("website") else 0
    score += 20 if lead.get("email") else 0
    score += 15 if lead.get("phone") else 0
    score += 30 if lead.get("relevant") else 0
    quality = analyze_website_quality(lead)
    score += round(quality["website_quality_score"] * 0.15)
    score = min(100, int(score))

    if score >= 80:
        status = "Hot Lead"
    elif score >= 55:
        status = "Warm Lead"
    else:
        status = "Cold Lead"

    return {**lead, **quality, "score": score, "status": status}


def score_leads(leads: list[dict]) -> list[dict]:
    return [score_lead(lead) for lead in leads]
