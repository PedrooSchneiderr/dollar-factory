#!/usr/bin/env python3
"""
4_transcrever_whisper.py
Transcreve o áudio real com `faster-whisper` extraindo timestamps exatos
palavra por palavra (word-level timestamps).
Gera legendas dinâmicas estilo CapCut/TikTok (.ass) com sincronização precisa.
Suporta personas:
  - scientist: Neon Cyber Green (&H0039FF14&) com estética científica e tecnológica.
  - standard: Neon Cyber Cyan (&H0000E5FF&), visual de e-commerce americano moderno.
"""
import argparse
import json
import re
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
WORK_DIR = BASE_DIR / "output" / "work"


def get_audio_duration(mp3_path: Path) -> float:
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(mp3_path)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())


def format_ass_time(seconds: float) -> str:
    seconds = max(0.0, float(seconds))
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def transcribe_words_whisper(mp3_path: Path) -> list[dict]:
    """Transcreve o áudio usando faster-whisper com timestamps de cada palavra."""
    try:
        from faster_whisper import WhisperModel
        # Usa modelo base.en rápido com computação int8
        model = WhisperModel("base.en", device="cpu", compute_type="int8")
        segments, _ = model.transcribe(str(mp3_path), word_timestamps=True)
        word_list = []
        for segment in segments:
            for w in segment.words:
                clean_w = w.word.strip().upper()
                if clean_w:
                    word_list.append({
                        "word": clean_w,
                        "start": float(w.start),
                        "end": float(w.end),
                    })
        if word_list:
            return word_list
    except Exception as exc:
        print(f"[WARN] faster-whisper falhou ({exc}), usando alinhamento de áudio.")

    # Fallback caso whisper não carregue
    return []


def generate_ass_subtitles(product_id: str, version: str = "v1") -> Path:
    work_dir = WORK_DIR / f"produto_{product_id}_{version}"
    roteiro = json.loads((work_dir / "roteiro.json").read_text(encoding="utf-8"))
    mp3_path = work_dir / "narracao.mp3"
    duration = get_audio_duration(mp3_path)

    persona = roteiro.get("persona", "scientist")
    is_scientist = persona in ("scientist", "rick")
    capcut_primary = "&H0039FF14" if is_scientist else "&H0000E5FF"
    top_badge_text = roteiro.get("top_banner") or (f"LAB FIND {roteiro['code']} ⚡" if is_scientist else f"AMAZON US FIND {roteiro['code']}")

    ass_header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: TopBadge,Arial Black,50,&H00FFFFFF,&H000000FF,&H00111827,&HCC111827,-1,0,0,0,100,100,1,0,3,18,0,8,40,40,140,1
Style: PricePill,Arial Black,46,{capcut_primary},&H000000FF,&H00000000,&HAA000000,-1,0,0,0,100,100,1,0,1,4,2,8,40,40,235,1
Style: WordPop,Arial Black,78,{capcut_primary},&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,100,100,1,0,1,7,4,2,70,70,480,1
Style: BottomCTA,Arial Black,48,&H00FFFFFF,&H000000FF,&H00004400,&HCC003300,-1,0,0,0,100,100,1,0,3,16,0,2,50,50,220,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    end_str = format_ass_time(duration + 0.3)
    code = roteiro["code"]
    short_title = roteiro["short_title"].upper()
    price = float(roteiro["price"])

    events = [
        f"Dialogue: 2,0:00:00.00,{end_str},TopBadge,,0,0,0,,{top_badge_text}",
        f"Dialogue: 2,0:00:00.00,{end_str},PricePill,,0,0,0,,{short_title} - ${price:.2f} PRIME",
        f"Dialogue: 2,0:00:00.00,{end_str},BottomCTA,,0,0,0,,LINK IN BIO -> SEARCH CODE {code}",
    ]

    words = transcribe_words_whisper(mp3_path)

    if words:
        # Agrupa em blocos de 2 a 3 palavras com timestamps precisos de início e fim
        chunk_size = 2
        for i in range(0, len(words), chunk_size):
            chunk_words = words[i:i + chunk_size]
            start_t = format_ass_time(chunk_words[0]["start"])
            end_t = format_ass_time(chunk_words[-1]["end"] + 0.05)
            text_str = " ".join(w["word"] for w in chunk_words)
            # Destaca a primeira palavra com amarelo e o resto no verde neon
            if len(chunk_words) > 1:
                highlighted = r"{\c&H0000FFFF&}" + chunk_words[0]["word"] + r"{\r} " + " ".join(w["word"] for w in chunk_words[1:])
            else:
                highlighted = r"{\c&H0000FFFF&}" + text_str

            events.append(f"Dialogue: 1,{start_t},{end_t},WordPop,,0,0,0,,{highlighted}")
        print(f"[4/5 Legendas] faster-whisper: {len(words)} palavras sincronizadas com precisão milimétrica.")
    else:
        # Fallback de contagem
        words_raw = re.findall(r"\S+", roteiro["full_narration"])
        chunk_size = 2
        dt = duration / max(1, (len(words_raw) / chunk_size))
        for i in range(0, len(words_raw), chunk_size):
            chunk = words_raw[i:i + chunk_size]
            start_t = format_ass_time((i // chunk_size) * dt)
            end_t = format_ass_time(((i // chunk_size) + 1) * dt)
            events.append(f"Dialogue: 1,{start_t},{end_t},WordPop,,0,0,0,,{' '.join(chunk).upper()}")
        print(f"[4/5 Legendas] Fallback: Legendas geradas.")

    out_file = work_dir / "legendas.ass"
    out_file.write_text(ass_header + "\n".join(events) + "\n", encoding="utf-8")
    return out_file


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", default="01")
    parser.add_argument("--version", default="v1")
    args = parser.parse_args()
    generate_ass_subtitles(args.id, args.version)


if __name__ == "__main__":
    main()
