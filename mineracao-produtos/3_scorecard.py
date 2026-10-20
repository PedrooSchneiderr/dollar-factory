#!/usr/bin/env python3
"""
3_scorecard.py
Aplica o Scorecard de 4 critérios do plan.md (máximo 20 pontos, mínimo 12/20 para aprovar):
  1. Preço de compra por impulso US$ 15–50 (1-5 pts)
  2. Dor clara e visual nos primeiros 3 segundos (1-5 pts)
  3. Efeito 'WOW' / demonstração mecânica (1-5 pts)
  4. Demanda US + disponibilidade Prime/Reviews (1-5 pts)
Gera: produtos_aprovados.csv
"""
import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INPUT_CSV = BASE_DIR / "candidatos_com_trend.csv"
OUTPUT_CSV = BASE_DIR / "produtos_aprovados.csv"


def score_price(price: float) -> int:
    if 15.0 <= price <= 40.0:
        return 5
    if 12.0 <= price <= 55.0:
        return 4
    if 10.0 <= price <= 70.0:
        return 3
    return 2


def score_visual_pain(row: dict) -> int:
    pain = (row.get("pain_point") or "").lower()
    hook = (row.get("visual_hook") or "").lower()
    if len(pain) > 20 and len(hook) > 20:
        return 5
    if len(pain) > 10 or len(hook) > 10:
        return 4
    return 3


def score_wow_factor(row: dict) -> int:
    title = (row.get("title") or "").lower()
    wow_keywords = [
        "spin", "electric", "roller", "chopper", "sprayer", "gel",
        "putty", "rotary", "motion", "shaver", "cleaner", "magnetic", "pull-out"
    ]
    hits = sum(1 for kw in wow_keywords if kw in title)
    if hits >= 2:
        return 5
    if hits == 1:
        return 4
    return 3


def main() -> None:
    print("=== [3/3] Scorecard de Aprovação de Produtos (Corte >= 12/20) ===")
    if not INPUT_CSV.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {INPUT_CSV}. Rode 2_validar_trend.py primeiro.")

    with INPUT_CSV.open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    approved = []
    for row in rows:
        try:
            price = float(row.get("price") or 0)
        except ValueError:
            price = 24.99

        s_price = score_price(price)
        s_pain = score_visual_pain(row)
        s_wow = score_wow_factor(row)
        s_trend = int(row.get("us_trend_score") or 4)
        total = s_price + s_pain + s_wow + s_trend

        row["score_preco"] = str(s_price)
        row["score_dor_3s"] = str(s_pain)
        row["score_wow"] = str(s_wow)
        row["score_total_20"] = str(total)
        row["status"] = "APPROVED" if total >= 12 else "REJECTED"

        if total >= 12:
            approved.append(row)
            print(
                f"   [APROVADO {total:02d}/20] {row.get('code', '--')} "
                f"{(row.get('short_title') or row.get('title', ''))[:32]:<32} "
                f"(${price:.2f} | Preço:{s_price} Dor:{s_pain} Wow:{s_wow} Trend:{s_trend})"
            )

    approved.sort(key=lambda r: int(r["score_total_20"]), reverse=True)
    fieldnames = list(approved[0].keys()) if approved else []
    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(approved)

    print(f"[OK] {len(approved)} produtos aprovados salvos em: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
