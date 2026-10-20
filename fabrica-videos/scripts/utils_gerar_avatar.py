#!/usr/bin/env python3
"""
utils_gerar_avatar.py
Gera o avatar autoral do Cientista Maluco ("Dr. Volt") em alta resolução com canal alfa transparente (512x512):
  1. scientist_closed.png (Boca fechada / neutra cínica)
  2. scientist_open.png (Boca aberta falando)
"""
from pathlib import Path
from PIL import Image, ImageDraw

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets" / "scientist"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)


def draw_mad_scientist(mouth_open: bool = False) -> Image.Image:
    size = (512, 512)
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # 1. Cabelo Maluco Eletrizado (Picos espetados no topo e laterais)
    hair_color = (235, 240, 250, 255)
    hair_outline = (160, 175, 195, 255)
    spikes = [
        # Esquerda
        [(150, 220), (90, 160), (160, 170)],
        [(140, 170), (70, 90), (165, 120)],
        [(160, 120), (110, 40), (200, 80)],
        # Topo
        [(200, 80), (210, 15), (256, 70)],
        [(256, 70), (300, 15), (312, 80)],
        # Direita
        [(312, 80), (402, 40), (352, 120)],
        [(352, 120), (442, 90), (372, 170)],
        [(372, 170), (422, 160), (362, 220)],
    ]
    for spike in spikes:
        d.polygon(spike, fill=hair_color, outline=hair_outline, width=3)

    # 2. Cabeça / Rosto (Forma levemente oval / angular)
    skin_color = (248, 224, 196, 255)
    skin_outline = (50, 50, 60, 255)
    d.ellipse([(160, 120), (352, 330)], fill=skin_color, outline=skin_outline, width=4)

    # 3. Jaleco de Cientista e Gravata Borboleta
    coat_color = (245, 248, 255, 255)
    coat_outline = (40, 40, 50, 255)
    d.polygon([(130, 480), (170, 310), (342, 310), (382, 480)], fill=coat_color, outline=coat_outline, width=4)
    # Gola do jaleco
    d.polygon([(170, 310), (230, 380), (210, 310)], fill=(225, 235, 245, 255), outline=coat_outline, width=3)
    d.polygon([(342, 310), (282, 380), (302, 310)], fill=(225, 235, 245, 255), outline=coat_outline, width=3)
    # Gravata borboleta vermelha
    d.polygon([(236, 316), (220, 305), (220, 335)], fill=(220, 38, 38, 255), outline=coat_outline, width=2)
    d.polygon([(276, 316), (292, 305), (292, 335)], fill=(220, 38, 38, 255), outline=coat_outline, width=2)
    d.ellipse([(246, 310), (266, 330)], fill=(185, 28, 28, 255), outline=coat_outline, width=2)

    # 4. Óculos Tecnológicos / Lente Neon Científica
    frame_color = (30, 41, 59, 255)
    lens_color = (57, 255, 20, 210)  # Neon Green transparente
    # Ponte dos óculos
    d.rectangle([(244, 192), (268, 204)], fill=frame_color)
    # Lente Esquerda
    d.ellipse([(174, 168), (248, 230)], fill=lens_color, outline=frame_color, width=5)
    d.ellipse([(202, 190), (218, 208)], fill=(15, 23, 42, 255))  # Pupila
    d.ellipse([(210, 193), (216, 199)], fill=(255, 255, 255, 255))  # Brilho
    # Lente Direita
    d.ellipse([(264, 168), (338, 230)], fill=lens_color, outline=frame_color, width=5)
    d.ellipse([(294, 190), (310, 208)], fill=(15, 23, 42, 255))  # Pupila
    d.ellipse([(302, 193), (308, 199)], fill=(255, 255, 255, 255))  # Brilho

    # Sobrancelhas levantadas expressivas
    d.line([(180, 155), (240, 165)], fill=hair_color, width=7)
    d.line([(272, 165), (332, 150)], fill=hair_color, width=7)

    # 5. Nariz
    d.line([(256, 210), (248, 238), (260, 240)], fill=(180, 120, 90, 255), width=3)

    # 6. Boca
    if mouth_open:
        # Boca aberta em formato de sorriso largo falante
        d.chord([(215, 250), (297, 305)], start=0, end=180, fill=(153, 27, 27, 255), outline=skin_outline, width=3)
        # Dentes superiores
        d.rectangle([(230, 253), (282, 268)], fill=(255, 255, 255, 255))
        # Língua
        d.ellipse([(238, 280), (274, 304)], fill=(244, 114, 182, 255))
    else:
        # Sorriso cínico e fechado
        d.arc([(220, 255), (292, 285)], start=20, end=160, fill=skin_outline, width=4)
        d.line([(288, 265), (296, 258)], fill=skin_outline, width=3)

    return img


if __name__ == "__main__":
    closed = draw_mad_scientist(mouth_open=False)
    closed.save(ASSETS_DIR / "scientist_closed.png")
    print(f"Salvo: {ASSETS_DIR / 'scientist_closed.png'}")

    open_m = draw_mad_scientist(mouth_open=True)
    open_m.save(ASSETS_DIR / "scientist_open.png")
    print(f"Salvo: {ASSETS_DIR / 'scientist_open.png'}")
