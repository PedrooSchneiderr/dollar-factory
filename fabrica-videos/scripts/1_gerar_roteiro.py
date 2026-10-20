#!/usr/bin/env python3
"""
1_gerar_roteiro.py
Gera variações de roteiro viral em inglês americano para TikTok / Reels / Shorts.
Suporta duas personas:
  - rick: Rick Sanchez (C-137), sarcástico, irreverente, ridiculariza o sofrimento humano com tarefas primitivas.
  - standard: Copywriting direto de e-commerce US (PAS, Shock, Honest Review).
Se ANTHROPIC_API_KEY estiver configurada, consulta Claude; caso contrário, usa gerador local calibrado.
"""
import argparse
import json
import os
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PRODUTOS = BASE_DIR.parent / "vitrine" / "src" / "data" / "produtos.json"  # fonte única do catálogo
WORK_DIR = BASE_DIR / "output" / "work"


def build_rick_scripts(product: dict) -> list[dict]:
    code = product["code"]
    short = product["short_title"]
    price = int(float(product["price"]))
    pain = product["pain_point"]
    solution = product["solution_summary"]
    benefits = product.get("benefits", [])
    b1 = benefits[0] if len(benefits) > 0 else solution
    b2 = benefits[1] if len(benefits) > 1 else "Over a hundred thousand five-star reviews on Amazon."

    return [
        {
            "version": "v1",
            "template": "rick_dimension_c137_pas",
            "persona": "rick",
            "top_banner": f"DIMENSION C-137 FIND {code} 🧪",
            "hook": f"Listen to me Morty, and listen close you primitive earthlings on TikTok.",
            "body": (
                f"I literally traveled across dimension C-137 just to find you still {pain}! "
                f"It makes my eyes hurt, Morty! Look at this ${price} {short} on Amazon. "
                f"{solution} It's not rocket science! {b1}."
            ),
            "cta": f"Stop living in the Stone Age! Tap the link in my bio, search code {code}, and get one before I leave this timeline!",
            "scenes_text": [
                f"STOP {pain.upper()[:26]}...",
                f"MORTY LOOK: ${price} {short.upper()[:20]}",
                b1.upper()[:38],
                f"TAP BIO LINK -> CODE {code} 🛸",
            ],
        },
        {
            "version": "v2",
            "template": "rick_interdimensional_roast",
            "persona": "rick",
            "top_banner": f"RICK'S LAB APPROVED {code} ⚡",
            "hook": f"Morty, grab a notepad. Humans are actually suffering from {pain} when Amazon sells this for ${price}.",
            "body": (
                f"I tested this {short} because human tools are usually garbage. "
                f"Turns out? {solution} {b1}. "
                f"Even Jerry could use this without ruining his life, Morty!"
            ),
            "cta": f"I put the portal link in my bio. Go type code {code} and evolve already!",
            "scenes_text": [
                f"RICK C-137 TEST: ${price}",
                short.upper()[:30],
                b2.upper()[:38],
                f"PORTAL LINK IN BIO ({code}) 🔗",
            ],
        },
        {
            "version": "v3",
            "template": "rick_genius_verdict",
            "persona": "rick",
            "top_banner": f"SMARTEST BUY ON AMAZON {code} 🧬",
            "hook": f"I'm Rick Sanchez, the smartest man in the multiverse, and your daily routine is pathetic.",
            "body": (
                f"Why are you wasting your short mortal life {pain}? "
                f"Get this ${price} {short} on Prime. {solution} "
                f"It pays for itself on day one. Stop being stubborn and grab it."
            ),
            "cta": f"Link is in my bio, code {code}. Now stop bugging me and go get it!",
            "scenes_text": [
                f"SMARTEST AMAZON FIND {code}",
                f"${price} ON PRIME // NO MORE EXCUSES",
                b1.upper()[:38],
                f"USE CODE {code} IN BIO ⚡",
            ],
        },
    ]


def build_standard_scripts(product: dict) -> list[dict]:
    code = product["code"]
    short = product["short_title"]
    price = int(float(product["price"]))
    pain = product["pain_point"]
    hook_custom = product["visual_hook"]
    solution = product["solution_summary"]
    benefits = product.get("benefits", [])
    b1 = benefits[0] if len(benefits) > 0 else solution
    b2 = benefits[1] if len(benefits) > 1 else "Thousands of five-star reviews on Amazon."

    return [
        {
            "version": "v1",
            "template": "problem_agitate_solve",
            "persona": "standard",
            "top_banner": f"AMAZON FIND {code} 🔥",
            "hook": hook_custom,
            "body": (
                f"If you are tired of {pain}, this ${price} {short} on Amazon changes everything. "
                f"{solution} Plus, {b1.lower()}."
            ),
            "cta": f"Comment {code} or tap the link in my bio and search {code} before it sells out!",
            "scenes_text": [
                f"STOP {pain.upper()[:28]}...",
                f"MEET THE ${price} {short.upper()}",
                b1.upper()[:42],
                f"SEARCH CODE {code} IN BIO 🔗",
            ],
        },
        {
            "version": "v2",
            "template": "curiosity_shock",
            "persona": "standard",
            "top_banner": f"GENIUS ${price} GADGET ({code})",
            "hook": f"POV: You just found out {pain} has a ${price} fix on Amazon.",
            "body": (
                f"I didn't believe the hype until I tested this {short} myself. "
                f"{b1}. And {b2.lower()}."
            ),
            "cta": f"I linked it in my bio — just search code {code}!",
            "scenes_text": [
                f"POV: ${price} AMAZON FIX",
                short.upper(),
                b2.upper()[:42],
                f"LINK IN BIO -> CODE {code}",
            ],
        },
        {
            "version": "v3",
            "template": "honest_review",
            "persona": "standard",
            "top_banner": f"AMAZON MUST-HAVE {code} ⭐",
            "hook": f"Amazon Finds that actually earn their five-star rating, part {int(product['id'])}!",
            "body": (
                f"This is the {short}. {solution} "
                f"Honestly, for ${price}, it pays for itself on day one."
            ),
            "cta": f"Grab yours via the link in my bio, code {code}!",
            "scenes_text": [
                f"AMAZON 5-STAR FIND {code}",
                short.upper(),
                f"ONLY ${price} ON PRIME",
                f"TAP BIO LINK ({code}) 🔗",
            ],
        },
    ]


def try_claude_api(product: dict, persona: str = "rick") -> list[dict] | None:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return None
    tone_instr = (
        "Write as Rick Sanchez from Rick and Morty: cynical, rapid-fire, arrogant genius addressing Morty "
        "and roasting TikTok viewers for struggling with primitive human tasks."
        if persona == "rick"
        else "Write as a viral high-converting US TikTok creator."
    )
    prompt = (
        f"{tone_instr} Generate 3 short viral scripts in American English (18-24 seconds each) "
        f"for this Amazon US product: {json.dumps(product)}. "
        "Return ONLY a JSON array of 3 objects with keys: version (v1,v2,v3), template, top_banner, hook, body, cta, scenes_text (array of 4 short uppercase strings)."
    )
    body = json.dumps({
        "model": "claude-3-5-sonnet-latest",
        "max_tokens": 1024,
        "messages": [{"role": "user", "content": prompt}],
    }).encode("utf-8")
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=body,
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            text = res["content"][0]["text"]
            start = text.find("[")
            end = text.rfind("]") + 1
            arr = json.loads(text[start:end])
            for item in arr:
                item["persona"] = persona
            return arr
    except Exception as exc:
        print(f"[WARN] Falha na API Claude ({exc}), usando gerador local US.")
        return None


def generate_for_product(product_id: str, version: str = "v1", persona: str = "rick") -> Path:
    products = json.loads(CONFIG_PRODUTOS.read_text(encoding="utf-8"))
    product = next((p for p in products if p["id"] == product_id or p["code"] == product_id), None)
    if not product:
        raise ValueError(f"Produto '{product_id}' não encontrado em {CONFIG_PRODUTOS}")

    p_dir = WORK_DIR / f"produto_{product['id']}_{version}"
    p_dir.mkdir(parents=True, exist_ok=True)

    if persona == "rick":
        variations = try_claude_api(product, persona="rick") or build_rick_scripts(product)
    else:
        variations = try_claude_api(product, persona="standard") or build_standard_scripts(product)

    chosen = next((v for v in variations if v["version"] == version), variations[0])
    chosen["persona"] = persona
    chosen["product_id"] = product["id"]
    chosen["code"] = product["code"]
    chosen["niche"] = product["niche"]
    chosen["short_title"] = product["short_title"]
    chosen["price"] = product["price"]
    chosen["full_narration"] = f"{chosen['hook']} {chosen['body']} {chosen['cta']}"

    out_file = p_dir / "roteiro.json"
    out_file.write_text(json.dumps(chosen, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[1/5 Roteiro] Persona: [{persona.upper()}] | Salvo em: {out_file}")
    print(f"      Hook: \"{chosen['hook']}\"")
    print(f"      Narração completa: \"{chosen['full_narration']}\"")
    return out_file


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", default="01", help="ID do produto (ex: 01, 02...)")
    parser.add_argument("--version", default="v1", choices=["v1", "v2", "v3"])
    parser.add_argument("--persona", default="rick", choices=["rick", "standard"], help="Persona do vídeo (rick ou standard)")
    args = parser.parse_args()
    generate_for_product(args.id, args.version, args.persona)


if __name__ == "__main__":
    main()
