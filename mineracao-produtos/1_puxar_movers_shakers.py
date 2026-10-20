#!/usr/bin/env python3
"""
1_puxar_movers_shakers.py
Coleta educada (1x/dia) de candidatos do Amazon US Movers & Shakers por categoria,
com fallback automático para lista semente validada caso a Amazon retorne bloqueio/CAPTCHA.
Gera: candidatos.csv
"""
import csv
import json
import re
import time
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_CSV = BASE_DIR / "candidatos.csv"
CATALOG_JSON = BASE_DIR.parent / "fabrica-videos" / "config" / "produtos.json"

CATEGORIES = {
    "Home & Cleaning": "https://www.amazon.com/gp/movers-and-shakers/home-garden",
    "Kitchen Hacks": "https://www.amazon.com/gp/movers-and-shakers/kitchen",
    "Pet Must-Haves": "https://www.amazon.com/gp/movers-and-shakers/pet-supplies",
    "Car & Everyday": "https://www.amazon.com/gp/movers-and-shakers/automotive",
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/128.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def try_fetch_category(niche: str, url: str) -> list[dict]:
    """Tenta extrair títulos e preços básicos da página pública do Movers & Shakers."""
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
    except Exception as exc:
        print(f"[WARN] Falha ao acessar {url}: {exc}")
        return []

    if "api-services-support@amazon.com" in html or "validateCaptcha" in html:
        print(f"[INFO] Amazon solicitou CAPTCHA para {niche} — usando catálogo validado.")
        return []

    titles = re.findall(r'class="[^"]*p13n-sc-truncate[^"]*"[^>]*>\s*([^<]+)\s*<', html)
    prices = re.findall(r'\$([0-9]+\.[0-9]{2})', html)
    items = []
    for idx, raw_title in enumerate(titles[:10], start=1):
        title = raw_title.strip()
        if len(title) < 8:
            continue
        price = float(prices[idx - 1]) if idx - 1 < len(prices) else 24.99
        items.append({
            "rank": idx,
            "niche": niche,
            "title": title,
            "price": price,
            "source": "amazon_movers_live",
        })
    return items


def load_fallback_candidates() -> list[dict]:
    """Carrega os 10 produtos campeões já mapeados no catálogo base."""
    if not CATALOG_JSON.exists():
        return []
    data = json.loads(CATALOG_JSON.read_text(encoding="utf-8"))
    rows = []
    for idx, p in enumerate(data, start=1):
        rows.append({
            "id": p["id"],
            "code": p["code"],
            "rank": idx,
            "niche": p["niche"],
            "title": p["title"],
            "short_title": p["short_title"],
            "price": p["price"],
            "rating": p.get("rating", 4.7),
            "reviews_count": p.get("reviews_count", 10000),
            "pain_point": p.get("pain_point", ""),
            "visual_hook": p.get("visual_hook", ""),
            "amazon_url": p.get("amazon_url", ""),
            "source": "curated_us_bestsellers",
        })
    return rows


def main() -> None:
    print("=== [1/3] Mineração Amazon US Movers & Shakers ===")
    collected: list[dict] = []
    for niche, url in CATEGORIES.items():
        print(f"-> Consultando categoria: {niche}...")
        live_items = try_fetch_category(niche, url)
        if live_items:
            print(f"   +{len(live_items)} itens extraídos ao vivo.")
            collected.extend(live_items)
        time.sleep(1.0)

    curated = load_fallback_candidates()
    if curated:
        print(f"-> Mesclando {len(curated)} produtos campeões curados (Amazon US Best Sellers)...")
        collected = curated + collected

    fieldnames = [
        "id", "code", "rank", "niche", "short_title", "title",
        "price", "rating", "reviews_count", "pain_point", "visual_hook",
        "amazon_url", "source"
    ]
    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in collected:
            writer.writerow(row)

    print(f"[OK] {len(collected)} candidatos salvos em: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
