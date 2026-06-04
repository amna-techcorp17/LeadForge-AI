QUALIFICATION_PROMPT = """
You are an expert B2B lead qualification analyst.

Determine if this business matches the user's target criteria.

Niche: {niche}
Location: {location}
Requirements:
{requirements}

Business Data:
{lead}

Return JSON only with these keys:
- relevant: true or false
- reason: short explanation
- confidence: integer from 0 to 100
"""

OUTREACH_PROMPT = """
Write highly personalized B2B sales outreach.

Business Data (JSON):
{lead}

Offer:
{offer}

Tone:
{tone}

Sender Name (use only in the email signature):
{sender_name}

Lead Summary:
{lead_summary}

IMPORTANT RULES:

1. Use the actual company/business name, address, and any industry details from the lead.
2. Do NOT address the email to the sender. The greeting must address the prospect or company.
3. Use sender_name only in the closing/signature line, not in the opening greeting.
4. Never use placeholders such as:
   [Recipient Name]
   [Practice Name]
   [Company Name]
5. Cold email MUST be a single plain text string.
6. Do NOT return greeting/body/signature as separate objects.
7. Do NOT return nested JSON.
8. Make the email specific to the business niche, location, and current online presence.
9. Keep the email under 130 words.

Return ONLY valid JSON:

{{
  "subject": "...",
  "cold_email": "...",
  "linkedin_message": "...",
  "follow_up": "..."
}}
"""

SUMMARY_PROMPT = """
Create a concise prospect summary for this qualified lead.

Lead:
{lead}

Mention why the prospect is valuable and what pain point the offer can solve.
Keep it under 55 words.
"""
