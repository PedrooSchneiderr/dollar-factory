#!/usr/bin/env python3
"""
run_pipeline.py
Orquestrador completo da Fábrica de Vídeos (Etapas 1 a 5).
Uso:
  uv run --with edge-tts python run_pipeline.py --id 01 --version v1
"""
import argparse
import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent / "scripts"


def run_step(script_name: str, product_id: str, version: str) -> None:
    script_path = SCRIPTS_DIR / script_name
    cmd = [sys.executable, str(script_path), "--id", product_id, "--version", version]
    subprocess.run(cmd, check=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", default="01", help="ID do produto (01 a 10)")
    parser.add_argument("--version", default="v1", choices=["v1", "v2", "v3"])
    args = parser.parse_args()

    print(f"\n========================================================")
    print(f" INICIANDO FÁBRICA DE VÍDEOS — PRODUTO #{args.id} ({args.version})")
    print(f"========================================================")
    for step in [
        "1_gerar_roteiro.py",
        "2_gerar_narracao.py",
        "3_baixar_clipes.py",
        "4_transcrever_whisper.py",
        "5_montar_video.py",
    ]:
        run_step(step, args.id, args.version)
    print(f"========================================================")
    print(f" PIPELINE CONCLUÍDO COM SUCESSO PARA PRODUTO #{args.id}!")
    print(f"========================================================\n")


if __name__ == "__main__":
    main()
