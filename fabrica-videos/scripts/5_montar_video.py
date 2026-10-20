#!/usr/bin/env python3
"""
5_montar_video.py
Monta o vídeo final vertical 1080x1920 (.mp4) combinando:
  - Cenas verticais concatenadas em loop até cobrir a narração
  - Queima das legendas dinâmicas `.ass` (CapCut style + Top Badge + Bottom CTA)
  - Áudio da narração neural em inglês + batida sutil de fundo
  - Copia automaticamente o `.mp4` gerado para `vitrine/public/videos/produto_<id>.mp4`
"""
import argparse
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
WORK_DIR = BASE_DIR / "output" / "work"
OUTPUT_DIR = BASE_DIR / "output"
VITRINE_VIDEOS_DIR = BASE_DIR.parent / "vitrine" / "public" / "videos"


def get_duration(media_path: Path) -> float:
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(media_path)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())


def assemble_video(product_id: str, version: str = "v1") -> Path:
    work_dir = WORK_DIR / f"produto_{product_id}_{version}"
    clips_dir = work_dir / "clips"
    mp3_path = work_dir / "narracao.mp3"
    ass_path = work_dir / "legendas.ass"

    audio_dur = get_duration(mp3_path) + 0.35
    scene_files = sorted(clips_dir.glob("scene_*.mp4"))
    if not scene_files:
        raise FileNotFoundError(f"Nenhuma cena encontrada em {clips_dir}")

    concat_list_path = work_dir / "concat_list.txt"
    lines = []
    for _ in range(3):
        for sf in scene_files:
            lines.append(f"file '{sf.as_posix()}'")
    concat_list_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    raw_concat_mp4 = work_dir / "concat_raw.mp4"
    subprocess.run(
        [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", str(concat_list_path),
            "-t", f"{audio_dur:.2f}",
            "-c", "copy", str(raw_concat_mp4),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    date_str = datetime.now().strftime("%Y-%m-%d")
    final_mp4 = OUTPUT_DIR / f"{date_str}_produto_{product_id}_{version}.mp4"

    ass_escaped = ass_path.as_posix().replace(":", r"\:")
    cmd = [
        "ffmpeg", "-y",
        "-i", str(raw_concat_mp4),
        "-i", str(mp3_path),
        "-vf", f"ass='{ass_escaped}'",
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "22", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "128k",
        "-shortest",
        str(final_mp4),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"[5/5 Vídeo Pronto] Exportado com sucesso: {final_mp4} ({final_mp4.stat().st_size // 1024} KB)")

    VITRINE_VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
    vitrine_copy = VITRINE_VIDEOS_DIR / f"produto_{product_id}.mp4"
    shutil.copy2(final_mp4, vitrine_copy)
    print(f"      -> Copiado para a Vitrine Next.js: {vitrine_copy}")
    return final_mp4


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", default="01")
    parser.add_argument("--version", default="v1")
    args = parser.parse_args()
    assemble_video(args.id, args.version)


if __name__ == "__main__":
    main()
