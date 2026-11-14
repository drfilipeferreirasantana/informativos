"""Gera as imagens da Calculadora de rescisão (cartão 480x300 e capa 1200x630).

Uso (na pasta do repositório): python ferramentas/capa_calculadora.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gerar as g  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402


def capa(l, a, destino):
    img = Image.new("RGB", (l, a), g.PAPEL)
    d = ImageDraw.Draw(img)
    m = int(l * 0.07)
    d.line((m, m, l - m, m), fill=g.TINTA, width=max(2, l // 400))
    d.text((m, m + int(a * 0.04)), "Direito Trabalhista", font=g.serifa(int(a * 0.06), "Text Semibold"), fill=g.BORDO)
    f1 = g.serifa(int(a * 0.15), "Display Bold")
    y = g.escrever(d, m, int(a * 0.28), g.quebrar(d, "Calculadora de rescisão", f1, int(l * 0.62)), f1, g.TINTA, 1.05)
    d.rectangle((m, y + 18, m + int(l * 0.09), y + 18 + max(5, a // 90)), fill=g.BORDO)
    f2 = g.condensada(int(a * 0.065))
    g.escrever(d, m, y + 40, g.quebrar(d, "Aviso prévio, 13º, férias e multa do FGTS", f2, int(l * 0.6)), f2, (42, 42, 42), 1.25)
    x0, y0, w, h = int(l * 0.72), int(a * 0.24), int(l * 0.2), int(a * 0.56)
    d.rectangle((x0, y0, x0 + w, y0 + h), outline=g.TINTA, width=max(3, l // 300))
    d.rectangle((x0 + w * 0.1, y0 + h * 0.07, x0 + w * 0.9, y0 + h * 0.25), fill=g.TINTA)
    for r in range(4):
        for c in range(3):
            bx, by = x0 + w * (0.1 + c * 0.28), y0 + h * (0.33 + r * 0.16)
            d.rectangle((bx, by, bx + w * 0.22, by + h * 0.11), fill=g.BORDO if (r == 3 and c == 2) else (200, 193, 180))
    img.save(destino, "JPEG", quality=86, optimize=True)


if __name__ == "__main__":
    raiz = Path(__file__).resolve().parent.parent
    capa(1200, 630, raiz / "assets" / "calculadora-capa.jpg")
    capa(480, 300, raiz / "assets" / "calculadora-p.jpg")
    print("imagens da calculadora prontas")
