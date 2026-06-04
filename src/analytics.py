from __future__ import annotations

import pandas as pd


def build_metrics(leads: list[dict]) -> dict:
    total = len(leads)
    qualified = sum(1 for lead in leads if lead.get("relevant"))
    hot = sum(1 for lead in leads if lead.get("status") == "Hot Lead")
    warm = sum(1 for lead in leads if lead.get("status") == "Warm Lead")
    cold = sum(1 for lead in leads if lead.get("status") == "Cold Lead")
    avg_score = round(sum(int(lead.get("score", 0)) for lead in leads) / total, 1) if total else 0
    return {
        "Total Leads": total,
        "Qualified Leads": qualified,
        "Hot Leads": hot,
        "Warm Leads": warm,
        "Cold Leads": cold,
        "Average Score": avg_score,
    }


def status_dataframe(leads: list[dict]) -> pd.DataFrame:
    if not leads:
        return pd.DataFrame({"status": [], "count": []})
    frame = pd.DataFrame(leads)
    return frame.groupby("status").size().reset_index(name="count")


def location_dataframe(leads: list[dict]) -> pd.DataFrame:
    rows = []
    for lead in leads:
        address = str(lead.get("address", "Unknown"))
        location = address.split(",")[-2].strip() if "," in address else address or "Unknown"
        rows.append({"location": location, "score": int(lead.get("score", 0))})
    if not rows:
        return pd.DataFrame({"location": [], "average_score": []})
    return pd.DataFrame(rows).groupby("location", as_index=False)["score"].mean().rename(columns={"score": "average_score"})


def ai_recommendations(leads: list[dict]) -> list[str]:
    if not leads:
        return ["Run a search to generate recommendations."]
    hot = [lead for lead in leads if lead.get("status") == "Hot Lead"]
    with_websites = [lead for lead in leads if lead.get("website")]
    return [
        f"Focus on {len(hot)} Hot Leads first for the highest conversion probability.",
        f"{round(len(with_websites) / len(leads) * 100)}% of leads have active website data.",
        "Prioritize leads with both email and phone for multi-channel outreach.",
    ]
