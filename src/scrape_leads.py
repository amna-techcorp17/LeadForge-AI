from __future__ import annotations

import re
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup

from .utils import clean_text, deduplicate_leads, extract_email, extract_phone, normalize_website

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager
    _SELENIUM_AVAILABLE = True
except Exception:
    _SELENIUM_AVAILABLE = False


COMPANY_PATTERNS = [
    "{niche} Solutions",
    "Prime {niche}",
    "{niche} Hub",
    "NorthStar {niche}",
    "Urban {niche} Co",
    "Elite {niche} Group",
    "{niche} Partners",
    "BrightPath {niche}",
    "NextWave {niche}",
    "Summit {niche}",
]

LOCATION_AREAS = [
    "New York",
    "Los Angeles",
    "Chicago",
    "Houston",
    "Phoenix",
    "Philadelphia",
    "San Antonio",
    "San Diego",
    "Dallas",
    "Austin",
]


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", clean_text(value).lower()).strip("-")
    return slug or "business"


def scrape_demo_leads(niche: str, location: str, limit: int) -> list[dict]:
    niche_name = clean_text(niche).title() or "Business"
    location_name = clean_text(location) or "USA"
    niche_slug = slugify(niche_name)
    leads = []
    for index in range(max(limit, 1)):
        company = COMPANY_PATTERNS[index % len(COMPANY_PATTERNS)].format(niche=niche_name)
        area = LOCATION_AREAS[index % len(LOCATION_AREAS)]
        domain = f"{slugify(company)}.example.com"
        leads.append(
            {
                "company": company,
                "website": f"https://{domain}" if index % 5 != 3 else "",
                "phone": f"+1 555 {100 + index:03d} {2000 + index:04d}" if index % 6 != 4 else "",
                "email": f"contact@{domain}" if index % 5 != 4 else "",
                "address": f"{area}, {location_name}",
                "source": f"{niche_name} Fallback Directory",
            }
        )
    return deduplicate_leads(leads[:limit])


def _create_chrome_driver() -> webdriver.Chrome:
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    )
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    try:
        driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined});"
            },
        )
    except Exception:
        pass
    return driver


def _fetch_yellowpages_html(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=20)
        if response.status_code == 200 and "Attention Required" not in response.text:
            return response.text
    except Exception:
        pass

    if not _SELENIUM_AVAILABLE:
        raise RuntimeError("Selenium is not available for Yellow Pages scraping")

    driver = _create_chrome_driver()
    try:
        driver.get(url)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".result"))
        )
        return driver.page_source
    finally:
        driver.quit()


def scrape_yellow_pages(niche: str, location: str, limit: int = 20) -> list[dict]:
    query = quote_plus(clean_text(niche))
    place = quote_plus(clean_text(location))
    url = f"https://www.yellowpages.com/search?search_terms={query}&geo_location_terms={place}"
    html = _fetch_yellowpages_html(url)
    soup = BeautifulSoup(html, "html.parser")

    leads: list[dict] = []
    for card in soup.select(".result")[:limit]:
        name = clean_text(card.select_one(".business-name").get_text(" ", strip=True) if card.select_one(".business-name") else "")
        website = ""
        website_node = card.select_one("a.track-visit-website")
        if website_node and website_node.get("href"):
            website = normalize_website(website_node["href"])
        phone = clean_text(card.select_one(".phones").get_text(" ", strip=True) if card.select_one(".phones") else "")
        address = clean_text(card.select_one(".street-address").get_text(" ", strip=True) if card.select_one(".street-address") else "")
        locality = clean_text(card.select_one(".locality").get_text(" ", strip=True) if card.select_one(".locality") else "")
        text = card.get_text(" ", strip=True)
        email = extract_email(text)

        if name:
            leads.append(
                {
                    "company": name,
                    "website": website,
                    "phone": phone or extract_phone(text),
                    "email": email,
                    "address": clean_text(f"{address} {locality}"),
                    "source": "Yellow Pages",
                }
            )
    return deduplicate_leads(leads)


def scrape_leads(niche: str, location: str, limit: int = 25, source: str = "Demo") -> list[dict]:
    if source == "Yellow Pages":
        try:
            leads = scrape_yellow_pages(niche, location, limit)
            if leads:
                return leads
        except Exception:
            pass
    return scrape_demo_leads(niche, location, limit)
