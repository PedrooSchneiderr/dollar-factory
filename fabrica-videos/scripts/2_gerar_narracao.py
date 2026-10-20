#!/usr/bin/env python3
"""
2_gerar_narracao.py
Converte o roteiro em narração neural nativa dos EUA usando `edge-tts`.
Suporta personas personalizadas (ex: Rick Sanchez com pitch/rate acelerados)
e aplica silenceremove para eliminar pausas mortas de áudio.
"""
import argparse
import asyncio
import json
import subprocess
from pathlib import Path
import edge_tts

BASE_DIR = Path(__file__).resolve().parent.parent
VOZES_CONFIG = BASE_DIR / "config" / "vozes.json"
WORK_DIR = BASE_DIR / "output" / "work"


def apply_silence_remove(raw_mp3: Path, final_mp3: Path) -> None:
    """Aplica o filtro silenceremove do FFmpeg para deixar a fala no ritmo acelerado de TikTok."""
    cmd = [
        "ffmpeg", "-y", "-i", str(raw_mp3),
        "-af", "silenceremove=start_periods=1:start_duration=0.02:start_threshold=-45dB:stop_periods=-1:stop_duration=0.18:stop_threshold=-45dB",
        "-c:a", "libmp3lame", "-b:a", "192k",
        str(final_mp3),
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as exc:
        print(f"[WARN] Silenceremove falhou ({exc}), mantendo áudio original.")
        if raw_mp3 != final_mp3:
            import shutil
            shutil.copy2(raw_mp3, final_mp3)


async def synthesize(roteiro_path: Path) -> tuple[Path, Path]:
    roteiro = json.loads(roteiro_path.read_text(encoding="utf-8"))
    vozes = json.loads(VOZES_CONFIG.read_text(encoding="utf-8"))

    persona = roteiro.get("persona", "rick")
    personas_cfg = vozes.get("personas", {})

    if persona in personas_cfg:
        cfg = personas_cfg[persona]
        voice = cfg.get("voice", "en-US-GuyNeural")
        rate = cfg.get("rate", "+14%")
        pitch = cfg.get("pitch", "-2Hz")
    else:
        niche = roteiro.get("niche", "")
        voice = vozes.get("niches", {}).get(niche) or vozes.get("default", "en-US-AvaMultilingualNeural")
        rate = vozes.get("rate", "+8%")
        pitch = vozes.get("pitch", "+0Hz")

    text = roteiro["full_narration"]

    out_dir = roteiro_path.parent
    raw_mp3 = out_dir / "narracao_raw.mp3"
    mp3_path = out_dir / "narracao.mp3"
    vtt_path = out_dir / "narracao.vtt"

    communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate, pitch=pitch)
    submaker = edge_tts.SubMaker()

    with raw_mp3.open("wb") as audio_file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_file.write(chunk["data"])
            elif chunk["type"] in ("WordBoundary", "SentenceBoundary"):
                submaker.feed(chunk)

    vtt_content = submaker.get_srt() if hasattr(submaker, "get_srt") else str(submaker)
    vtt_path.write_text(vtt_content, encoding="utf-8")

    # Aplica corte de silêncio para manter o ritmo hipnótico/rápido de TikTok
    apply_silence_remove(raw_mp3, mp3_path)

    print(f"[2/5 Narração] Persona [{persona.upper()}]: Voz '{voice}' (rate {rate}, pitch {pitch}) -> {mp3_path}")
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
