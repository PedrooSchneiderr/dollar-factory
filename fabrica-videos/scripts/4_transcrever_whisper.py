#!/usr/bin/env python3
"""
4_transcrever_whisper.py
Gera o arquivo de legendas dinâmicas estilo CapCut/TikTok (`.ass` Advanced SubStation Alpha)
com sincronização precisa de tempo baseada na duração real de `narracao.mp3`,
além do banner fixo superior com o código do produto (`AMAZON FIND #01`) e preço.
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
    seconds = max(0.0, seconds)
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def split_into_chunks(text: str, words_per_chunk: int = 3) -> list[str]:
    words = re.findall(r"\S+", text)
    chunks = []
    for i in range(0, len(words), words_per_chunk):
        chunk = " ".join(words[i:i + words_per_chunk])
        chunks.append(chunk.upper())
    return chunks


def generate_ass_subtitles(product_id: str, version: str = "v1") -> Path:
    work_dir = WORK_DIR / f"produto_{product_id}_{version}"
    roteiro = json.loads((work_dir / "roteiro.json").read_text(encoding="utf-8"))
    mp3_path = work_dir / "narracao.mp3"
    duration = get_audio_duration(mp3_path)

    full_text = roteiro["full_narration"]
    chunks = split_into_chunks(full_text, words_per_chunk=3)
    total_words = sum(len(c.split()) for c in chunks)

    ass_header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: TopBadge,Arial Black,52,&H00FFFFFF,&H000000FF,&H00111827,&HCC111827,-1,0,0,0,100,100,1,0,3,18,0,8,40,40,140,1
Style: PricePill,Arial Black,46,&H0000FF99,&H000000FF,&H00000000,&HAA000000,-1,0,0,0,100,100,1,0,1,4,2,8,40,40,235,1
Style: CapCutPop,Arial Black,78,&H0000E5FF,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,1,0,1,7,4,2,70,70,480,1
Style: BottomCTA,Arial Black,48,&H00FFFFFF,&H000000FF,&H000055FF,&HCC0055FF,-1,0,0,0,100,100,1,0,3,16,0,2,50,50,220,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    end_str = format_ass_time(duration + 0.4)
    code = roteiro["code"]
    short_title = roteiro["short_title"].upper()
    price = roteiro["price"]

    events = [
        f"Dialogue: 2,0:00:00.00,{end_str},TopBadge,,0,0,0,,AMAZON US FIND {code}",
        f"Dialogue: 2,0:00:00.00,{end_str},PricePill,,0,0,0,,{short_title} - ${price:.2f} PRIME",
        f"Dialogue: 2,0:00:00.00,{end_str},BottomCTA,,0,0,0,,LINK IN BIO -> SEARCH CODE {code}",
    ]

    cur_time = 0.0
    usable_duration = max(1.0, duration - 0.15)
    for idx, chunk in enumerate(chunks):
        w_count = len(chunk.split())
        chunk_dur = usable_duration * (w_count / max(1, total_words))
        start_t = format_ass_time(cur_time)
        end_t = format_ass_time(cur_time + chunk_dur)
        cur_time += chunk_dur

        words = chunk.split()
        if len(words) >= 2:
            words[-1] = r"{\c&H00FFFFFF&}" + words[-1] + r"{\c&H0000E5FF&}"
        styled_chunk = r"{\fscx110\fscy110\t(0,90,\fscx100\fscy100)}" + " ".join(words)
        events.append(f"Dialogue: 3,{start_t},{end_t},CapCutPop,,0,0,0,,{styled_chunk}")

    ass_path = work_dir / "legendas.ass"
    ass_path.write_text(ass_header + "\n".join(events) + "\n", encoding="utf-8")
    print(f"[4/5 Legendas] Arquivo ASS estilo CapCut salvo em: {ass_path} ({len(chunks)} blocos)")
    return ass_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", default="01")
    parser.add_argument("--version", default="v1")
    args = parser.parse_args()
    generate_ass_subtitles(args.id, args.version)


if __name__ == "__main__":
    main()
