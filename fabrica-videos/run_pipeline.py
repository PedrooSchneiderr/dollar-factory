#!/usr/bin/env python3
"""
run_pipeline.py
Orquestrador completo da Fábrica de Vídeos Pro 2.0 (Etapas 1 a 5).
Uso:
  # Gera vídeo com persona Rick Sanchez (padrão Pro 2.0):
  uv run --with edge-tts python run_pipeline.py --id 01 --version v1

  # Gera com versão específica ou persona standard:
  uv run --with edge-tts python run_pipeline.py --id 02 --version v1 --persona rick
  uv run --with edge-tts python run_pipeline.py --id 01 --version v2 --persona standard
"""
import argparse
import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent / "scripts"


def run_step(script_name: str, product_id: str, version: str, persona: str = "rick") -> None:
    script_path = SCRIPTS_DIR / script_name
    cmd = [sys.executable, str(script_path), "--id", product_id, "--version", version]
    if script_name == "1_gerar_roteiro.py":
        cmd.extend(["--persona", persona])
    subprocess.run(cmd, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Fábrica de Vídeos Dollar Factory Pro 2.0")
    parser.add_argument("--id", default="01", help="ID do produto (01 a 10)")
    parser.add_argument("--version", default="v1", choices=["v1", "v2", "v3"], help="Versão do roteiro")
    parser.add_argument("--persona", default="scientist", choices=["scientist", "rick", "standard"], help="Persona do vídeo")
    args = parser.parse_args()

    print(f"\n========================================================")
    print(f" INICIANDO FÁBRICA DE VÍDEOS PRO 2.0")
    print(f" PRODUTO #{args.id} | VERSÃO: {args.version} | PERSONA: {args.persona.upper()}")
    print(f"========================================================")
    for step in [
        "1_gerar_roteiro.py",
        "2_gerar_narracao.py",
        "3_baixar_clipes.py",
        "4_transcrever_whisper.py",
        "5_montar_video.py",
    ]:
        run_step(step, args.id, args.version, args.persona)
    print(f"========================================================")
    print(f" PIPELINE PRO 2.0 CONCLUÍDO COM SUCESSO PARA PRODUTO #{args.id}!")
    print(f"========================================================\n")


if __name__ == "__main__":
    main()
