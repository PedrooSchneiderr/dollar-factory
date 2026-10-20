#!/usr/bin/env python3
"""
gerar_lote_completo.py
Gera o lote completo de vídeos (produtos #01 ao #10) com a Fábrica Pro 3.0:
  - Persona Cientista Autoral (sem violação de IP)
  - Roteiros dinâmicos (20-25s) com gancho de dor nos primeiros 3s
  - Cenas de 1.8s com fundo desfocado e produto centralizado
  - Legendas palavra por palavra com faster-whisper
  - Avatar reativo com lipsync automático
  - Sound design completo com FFmpeg
"""
import subprocess
import sys
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = BASE_DIR / "scripts"
OUTPUT_DIR = BASE_DIR / "output"
VITRINE_VIDEOS = BASE_DIR.parent / "vitrine" / "public" / "videos"

PRODUCT_IDS = ["01", "03", "04", "05", "06", "07", "08", "09", "10"]


def run_pipeline_for_product(pid: str) -> bool:
    print(f"\n==========================================================")
    print(f" >>> PROCESSANDO PRODUTO #{pid} (SCIENTIST / PRO 3.0) <<<")
    print(f"==========================================================")
    start_t = time.time()

    steps = [
        ("1_gerar_roteiro.py", ["--persona", "scientist"]),
        ("2_gerar_narracao.py", []),
        ("3_baixar_clipes.py", []),
        ("4_transcrever_whisper.py", []),
        ("5_montar_video.py", []),
    ]

    for script, extra_args in steps:
        cmd = [sys.executable, str(SCRIPTS_DIR / script), "--id", pid, "--version", "v1"] + extra_args
        res = subprocess.run(cmd)
        if res.returncode != 0:
            print(f"[ERRO] Falha na etapa {script} para produto #{pid}")
            return False

    elapsed = time.time() - start_t
    print(f"[OK] Produto #{pid} concluído em {elapsed:.1f} segundos!")
    return True


def main() -> None:
    print("Iniciando geração em lote para os 9 produtos restantes...")
    success = []
    failed = []

    for pid in PRODUCT_IDS:
        ok = run_pipeline_for_product(pid)
        if ok:
            success.append(pid)
        else:
            failed.append(pid)

    print("\n==========================================================")
    print(f" RELATÓRIO DO LOTE PRO 3.0")
    print(f" Concluídos com sucesso ({len(success)}): {', '.join(success)}")
    if failed:
        print(f" Falhas ({len(failed)}): {', '.join(failed)}")
    print("==========================================================\n")


if __name__ == "__main__":
    main()
