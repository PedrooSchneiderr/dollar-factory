#!/usr/bin/env python3
"""
5_montar_video.py
Monta o vídeo final vertical 1080x1920 (.mp4) de alta conversão combinando:
  - Cenas de 1.8s com fundo desfocado e produto centralizado
  - Queima das legendas palavra por palavra com faster-whisper (.ass)
  - Personagem autoral com boca reativa ao áudio (lipsync por envelope de amplitude)
  - Sound design: narração tratada + ding no preço + whoosh de transição + música de fundo baixa (10%)
  - Cópia automática para a Vitrine Next.js (vitrine/public/videos/produto_<id>.mp4)
"""
import argparse
import json
import math
import shutil
import struct
import subprocess
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
WORK_DIR = BASE_DIR / "output" / "work"
OUTPUT_DIR = BASE_DIR / "output"
VITRINE_VIDEOS_DIR = BASE_DIR.parent / "vitrine" / "public" / "videos"

SCIENTIST_DIR = BASE_DIR / "assets" / "scientist"
SFX_DIR = BASE_DIR / "assets" / "sfx"
MUSICA_DIR = BASE_DIR / "assets" / "musica"


def get_duration(media_path: Path) -> float:
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(media_path)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())


def build_reactive_avatar(mp3_path: Path, work_dir: Path, audio_dur: float) -> Path | None:
    """Gera um clipe de vídeo transparente do avatar com boca reativa à amplitude do áudio."""
    closed_img = SCIENTIST_DIR / "scientist_closed.png"
    open_img = SCIENTIST_DIR / "scientist_open.png"
    if not (closed_img.exists() and open_img.exists()):
        return None

    # Extrai PCM mono 16kHz
    raw_pcm = work_dir / "temp_pcm.raw"
    try:
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(mp3_path), "-ac", "1", "-ar", "16000", "-f", "s16le", str(raw_pcm)],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        data = raw_pcm.read_bytes()
    finally:
        if raw_pcm.exists():
            raw_pcm.unlink()

    samples = struct.unpack(f"<{len(data)//2}h", data)
    fps = 30
    spf = 16000 // fps
    total_frames = len(samples) // spf

    states = []
    for f in range(total_frames):
        chunk = samples[f * spf:(f + 1) * spf]
        rms = math.sqrt(sum(s * s for s in chunk) / len(chunk)) / 32768.0
        # Alterna boca aberta quando há fala ativa a cada ~3 frames para efeito orgânico de fala
        is_speaking = (rms > 0.022) and ((f // 3) % 2 == 0)
        states.append("open" if is_speaking else "closed")

    chunks = []
    cur_state = states[0] if states else "closed"
    cur_count = 0
    for s in states:
        if s == cur_state:
            cur_count += 1
        else:
            chunks.append((cur_state, cur_count / fps))
            cur_state = s
            cur_count = 1
    chunks.append((cur_state, cur_count / fps))

    concat_file = work_dir / "avatar_concat.txt"
    with open(concat_file, "w", encoding="utf-8") as f:
        for state, dur in chunks:
            img = open_img if state == "open" else closed_img
            f.write(f"file '{img.resolve().as_posix()}'\n")
            f.write(f"duration {dur:.3f}\n")
        f.write(f"file '{closed_img.resolve().as_posix()}'\n")

    out_mov = work_dir / "avatar_reactive.mov"
    cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_file),
        "-c:v", "png", "-pix_fmt", "rgba", "-r", "30", str(out_mov)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return out_mov


def assemble_video(product_id: str, version: str = "v1") -> Path:
    work_dir = WORK_DIR / f"produto_{product_id}_{version}"
    clips_dir = work_dir / "clips"
    mp3_path = work_dir / "narracao.mp3"
    ass_path = work_dir / "legendas.ass"
    roteiro_path = work_dir / "roteiro.json"

    roteiro = json.loads(roteiro_path.read_text(encoding="utf-8")) if roteiro_path.exists() else {}
    audio_dur = get_duration(mp3_path) + 0.35

    scene_files = sorted(clips_dir.glob("scene_*.mp4"))
    if not scene_files:
        raise FileNotFoundError(f"Nenhuma cena encontrada em {clips_dir}")

    # Concatena as cenas de 1.8s em loop suficiente para cobrir a narração
    concat_list_path = work_dir / "concat_list.txt"
    lines = []
    loops = max(2, int(audio_dur / (len(scene_files) * 1.8)) + 1)
    for _ in range(loops):
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
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )

    date_str = datetime.now().strftime("%Y-%m-%d")
    final_mp4 = OUTPUT_DIR / f"{date_str}_produto_{product_id}_{version}.mp4"
    ass_escaped = ass_path.as_posix().replace(":", r"\:")

    # 1. Monta clipe do avatar reativo
    avatar_mov = build_reactive_avatar(mp3_path, work_dir, audio_dur)

    # 2. Prepara assets de sound design
    musica_file = next(MUSICA_DIR.glob("*.mp3"), None) if MUSICA_DIR.exists() else None
    ding_file = SFX_DIR / "ding_preco.mp3"
    whoosh_file = SFX_DIR / "whoosh_transicao.mp3"

    inputs = ["-i", str(raw_concat_mp4), "-i", str(mp3_path)]
    filter_video_parts = []
    filter_audio_parts = ["[1:a]volume=1.0[a_voice]"]
    amix_inputs = ["[a_voice]"]

    # Montagem dos inputs e filtros
    inputs = ["-i", str(raw_concat_mp4), "-i", str(mp3_path)]
    filter_video_parts = []
    filter_audio_parts = ["[1:a]volume=1.0[a_voice]"]
    amix_inputs = ["[a_voice]"]
    current_input_idx = 2

    # Adiciona avatar se disponível
    if avatar_mov and avatar_mov.exists():
        inputs.extend(["-i", str(avatar_mov)])
        filter_video_parts.append(
            f"[0:v]ass='{ass_escaped}'[v_sub];"
            f"[{current_input_idx}:v]scale=260:-1[avatar_scaled];"
            f"[v_sub][avatar_scaled]overlay=x=W-w-35:y='H-h-240+8*sin(2*PI*t/2.2)':shortest=1[v_out]"
        )
        current_input_idx += 1
    else:
        filter_video_parts.append(f"[0:v]ass='{ass_escaped}'[v_out]")

    # Adiciona Música de fundo baixa (10% de volume)
    if musica_file and musica_file.exists():
        inputs.extend(["-stream_loop", "-1", "-i", str(musica_file)])
        filter_audio_parts.append(f"[{current_input_idx}:a]volume=0.10[a_bgm]")
        amix_inputs.append("[a_bgm]")
        current_input_idx += 1

    # Adiciona SFX Ding no preço (~4.2s)
    if ding_file and ding_file.exists():
        inputs.extend(["-i", str(ding_file)])
        filter_audio_parts.append(f"[{current_input_idx}:a]adelay=4200|4200,volume=0.35[a_ding]")
        amix_inputs.append("[a_ding]")
        current_input_idx += 1

    # Adiciona SFX Whoosh de transição inicial (~1.8s)
    if whoosh_file and whoosh_file.exists():
        inputs.extend(["-i", str(whoosh_file)])
        filter_audio_parts.append(f"[{current_input_idx}:a]adelay=1800|1800,volume=0.25[a_whoosh]")
        amix_inputs.append("[a_whoosh]")
        current_input_idx += 1

    # Combina áudios com amix
    filter_audio_parts.append(
        f"{''.join(amix_inputs)}amix=inputs={len(amix_inputs)}:duration=first:dropout_transition=2[a_out]"
    )

    filter_complex = ";".join(filter_video_parts + filter_audio_parts)

    cmd = ["ffmpeg", "-y"] + inputs + [
        "-filter_complex", filter_complex,
        "-map", "[v_out]",
        "-map", "[a_out]",
        "-t", f"{audio_dur:.2f}",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "22", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "160k",
        "-shortest",
        str(final_mp4),
    ]

    print("[5/5 Montagem] Renderizando vídeo completo com avatar reativo e sound design...")
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
