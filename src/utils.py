from __future__ import annotations

import re
from hashlib import sha1
from typing import Iterable

import pandas as pd


EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE_RE = re.compile(r"(?:\+?\d[\d\s().-]{7,}\d)")


def clean_text(value: object) -> str:
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value)).strip()


def extract_email(text: str) -> str:
    match = EMAIL_RE.search(text or "")
    return match.group(0) if match else ""


def extract_phone(text: str) -> str:
    match = PHONE_RE.search(text or "")
    return clean_text(match.group(0)) if match else ""


def normalize_website(url: str) -> str:
    url = clean_text(url)
    if not url:
        return ""
    if url.startswith(("http://", "https://")):
        return url
    return f"https://{url}"


def lead_id(lead: dict) -> str:
    key = "|".join(
        clean_text(lead.get(field, "")).lower()
        for field in ("company", "website", "email", "phone", "address")
    )
    return sha1(key.encode("utf-8")).hexdigest()[:12]


def deduplicate_leads(leads: Iterable[dict]) -> list[dict]:
    seen: set[str] = set()
    unique: list[dict] = []
    for lead in leads:
        identity = lead_id(lead)
        if identity in seen:
            continue
        seen.add(identity)
        unique.append({**lead, "lead_id": identity})
    return unique


def to_dataframe(leads: list[dict]) -> pd.DataFrame:
    columns = [
        "lead_id",
        "company",
        "website",
        "email",
        "phone",
        "address",
        "source",
        "relevant",
        "qualification_reason",
        "score",
        "status",
        "website_quality",
        "prospect_summary",
        "cold_email",
        "linkedin_message",
        "follow_up",
    ]
    frame = pd.DataFrame(leads)
    for column in columns:
        if column not in frame:
            frame[column] = ""
    return frame[columns]
