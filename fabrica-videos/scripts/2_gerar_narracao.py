#!/usr/bin/env python3
"""
2_gerar_narracao.py
Converte o roteiro em narração neural nativa dos EUA usando `edge-tts`
e já extrai os timestamps de fala em `.vtt` / `.json` para sincronizar legendas.
"""
import argparse
import asyncio
import json
from pathlib import Path
import edge_tts

BASE_DIR = Path(__file__).resolve().parent.parent
VOZES_CONFIG = BASE_DIR / "config" / "vozes.json"
WORK_DIR = BASE_DIR / "output" / "work"


async def synthesize(roteiro_path: Path) -> tuple[Path, Path]:
    roteiro = json.loads(roteiro_path.read_text(encoding="utf-8"))
    vozes = json.loads(VOZES_CONFIG.read_text(encoding="utf-8"))

    niche = roteiro.get("niche", "")
    voice = vozes.get("niches", {}).get(niche) or vozes.get("default", "en-US-AvaMultilingualNeural")
    rate = vozes.get("rate", "+8%")
    pitch = vozes.get("pitch", "+0Hz")
    text = roteiro["full_narration"]

    out_dir = roteiro_path.parent
    mp3_path = out_dir / "narracao.mp3"
    vtt_path = out_dir / "narracao.vtt"

    communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate, pitch=pitch)
    submaker = edge_tts.SubMaker()

    with mp3_path.open("wb") as audio_file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_file.write(chunk["data"])
            elif chunk["type"] in ("WordBoundary", "SentenceBoundary"):
                submaker.feed(chunk)

    vtt_content = submaker.get_srt() if hasattr(submaker, "get_srt") else str(submaker)
    vtt_path.write_text(vtt_content, encoding="utf-8")
    print(f"[2/5 Narração] Voz '{voice}' gerada em: {mp3_path}")
    return mp3_path, vtt_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", default="01")
    parser.add_argument("--version", default="v1")
    args = parser.parse_args()

    roteiro_path = WORK_DIR / f"produto_{args.id}_{args.version}" / "roteiro.json"
    asyncio.run(synthesize(roteiro_path))


if __name__ == "__main__":
    main()
