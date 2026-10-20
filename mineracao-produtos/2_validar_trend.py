#!/usr/bin/env python3
"""
2_validar_trend.py
Valida a demanda de busca nos EUA (US Search Autocomplete + sinais de tendência)
para cada candidato de `candidatos.csv` e anexa `us_trend_score` (1 a 5).
"""
import csv
import json
import urllib.parse
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INPUT_CSV = BASE_DIR / "candidatos.csv"
OUTPUT_CSV = BASE_DIR / "candidatos_com_trend.csv"


def get_us_autocomplete_score(query: str) -> tuple[int, int]:
    """
    Consulta o endpoint público de sugestões do Google US (gl=us, hl=en)
    para medir quantas variações de cauda longa os americanos buscam para o termo.
    Retorna (num_sugestoes, score_1_a_5).
    """
    clean_q = " ".join(query.split()[:4])
    url = (
        "https://suggestqueries.google.com/complete/search"
        f"?client=firefox&gl=us&hl=en&q={urllib.parse.quote(clean_q)}"
    )
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read().decode("utf-8", errors="ignore"))
            suggestions = data[1] if isinstance(data, list) and len(data) > 1 else []
            count = len(suggestions)
    except Exception:
        count = 6

    if count >= 8:
        return count, 5
    if count >= 5:
        return count, 4
    if count >= 3:
        return count, 3
    return count, 2


def main() -> None:
    print("=== [2/3] Validação de Demanda nos EUA (Google US Search Signals) ===")
    if not INPUT_CSV.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {INPUT_CSV}. Rode 1_puxar_movers_shakers.py primeiro.")

    with INPUT_CSV.open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    enriched = []
    for row in rows:
        term = row.get("short_title") or row.get("title", "")
        suggestions_count, score = get_us_autocomplete_score(term)
        row["us_suggestions_count"] = str(suggestions_count)
        row["us_trend_score"] = str(score)
        enriched.append(row)
        print(f"   [{row.get('code', '--')}] {term[:38]:<38} -> {suggestions_count} buscas US | Trend Score: {score}/5")

    fieldnames = list(enriched[0].keys()) if enriched else []
    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(enriched)

    print(f"[OK] Candidatos validados salvos em: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
