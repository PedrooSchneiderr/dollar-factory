#!/usr/bin/env python3
"""
3_baixar_clipes.py
Prepara os clipes visuais verticais (1080x1920) do produto:
  1. Se houver vídeos reais em `assets/clipes_brutos/produto_<id>/*.mp4` (baixados da Amazon/TikTok/AliExpress),
     aplica remix anti-copyright (cortes rápidos, crop 6%, leve ajuste de saturação/contraste).
  2. Caso ainda não haja `.mp4` bruto local, baixa as fotos reais de alta resolução do produto/galeria
     e gera 4 cenas dinâmicas em 1080x1920 com efeito Ken Burns (zoom/pan suave) + cards visuais.
"""
import argparse
import json
import subprocess
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PRODUTOS = BASE_DIR / "config" / "produtos.json"
RAW_CLIPS_DIR = BASE_DIR / "assets" / "clipes_brutos"
WORK_DIR = BASE_DIR / "output" / "work"


def download_image(url: str, dest: Path) -> bool:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            dest.write_bytes(resp.read())
        return dest.exists() and dest.stat().st_size > 1000
    except Exception as exc:
        print(f"[WARN] Não foi possível baixar imagem {url}: {exc}")
        return False


def prepare_clips(product_id: str, version: str = "v1") -> list[Path]:
    products = json.loads(CONFIG_PRODUTOS.read_text(encoding="utf-8"))
    product = next(p for p in products if p["id"] == product_id)

    work_dir = WORK_DIR / f"produto_{product_id}_{version}"
    clips_dir = work_dir / "clips"
    clips_dir.mkdir(parents=True, exist_ok=True)

    raw_product_dir = RAW_CLIPS_DIR / f"produto_{product_id}"
    raw_mp4s = list(raw_product_dir.glob("*.mp4")) if raw_product_dir.exists() else []

    if raw_mp4s:
        print(f"[3/5 Clipes] Encontrados {len(raw_mp4s)} clipes reais em {raw_product_dir} — aplicando remix anti-copyright...")
        out_clips: list[Path] = []
        for idx, src_mp4 in enumerate(raw_mp4s[:4], start=1):
            out_clip = clips_dir / f"scene_{idx:02d}.mp4"
            vf = (
                "scale=1150:2040:force_original_aspect_ratio=increase,"
                "crop=1080:1920,"
                "eq=contrast=1.05:saturation=1.08,"
                "fps=30,format=yuv420p"
            )
            cmd = [
                "ffmpeg", "-y", "-i", str(src_mp4),
                "-t", "5", "-an", "-vf", vf,
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
                str(out_clip),
            ]
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            out_clips.append(out_clip)
        return out_clips

    print(f"[3/5 Clipes] Baixando imagens do produto #{product_id} e gerando 4 cenas dinâmicas 1080x1920...")
    urls = list(dict.fromkeys([product["image_url"]] + product.get("gallery_urls", [])))
    while len(urls) < 4:
        urls.append(urls[len(urls) % len(urls)])

    out_clips = []
    for idx, url in enumerate(urls[:4], start=1):
        img_path = clips_dir / f"img_{idx:02d}.jpg"
        ok = download_image(url, img_path)
        out_clip = clips_dir / f"scene_{idx:02d}.mp4"

        if ok:
            zoom_expr = "min(zoom+0.0018,1.22)" if idx % 2 == 1 else "if(eq(on,1),1.22,max(1.0,zoom-0.0018))"
            vf = (
                "scale=1400:2488:force_original_aspect_ratio=increase,"
                "crop=1400:2488,"
                f"zoompan=z='{zoom_expr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=150:s=1080x1920:fps=30,"
                "eq=contrast=1.06:saturation=1.10:brightness=-0.03,"
                "format=yuv420p"
            )
            cmd = [
                "ffmpeg", "-y", "-loop", "1", "-i", str(img_path),
                "-t", "5", "-an", "-vf", vf,
                "-c:v", "libx264", "-preset", "ultrafast", "-crf", "23",
                str(out_clip),
            ]
        else:
            cmd = [
                "ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=#111827:s=1080x1920:r=30:d=5",
                "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
                str(out_clip),
            ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        out_clips.append(out_clip)

    print(f"[3/5 Clipes] {len(out_clips)} cenas verticais geradas em: {clips_dir}")
    return out_clips


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", default="01")
    parser.add_argument("--version", default="v1")
    args = parser.parse_args()
    prepare_clips(args.id, args.version)


if __name__ == "__main__":
    main()
