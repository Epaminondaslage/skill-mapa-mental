#!/usr/bin/env python3
"""Renderizador de infográficos técnicos, preservando o JSON e SVG como formatos abertos."""
import argparse
import html
import json
import math
import textwrap
from pathlib import Path

PALETTES = {
    "tecnico": ("#0b1730", "#2563eb", "#eff6ff", "#172554"),
    "diagnostico": ("#13251e", "#0f766e", "#ecfdf5", "#134e4a"),
    "referencia": ("#292524", "#c2410c", "#fff7ed", "#7c2d12"),
    "conceitual": ("#17152f", "#7c3aed", "#f5f3ff", "#4c1d95"),
}

def esc(value):
    return html.escape(str(value), quote=True)

def validate(data):
    if not isinstance(data, dict) or not str(data.get("title", "")).strip():
        raise ValueError("title obrigatório")
    if data.get("language", "pt-BR") not in ("pt-BR", "it-IT"):
        raise ValueError("idioma inválido")
    if data.get("style", "tecnico") not in PALETTES:
        raise ValueError("estilo inválido")
    sections = data.get("sections")
    if not isinstance(sections, list) or not sections:
        raise ValueError("sections deve ser lista não vazia")
    for section in sections:
        if not isinstance(section, dict) or not str(section.get("title", "")).strip():
            raise ValueError("seção sem título")
        if not isinstance(section.get("items", []), list):
            raise ValueError("items deve ser lista")
        for item in section["items"]:
            if not isinstance(item, str):
                raise ValueError("cada item deve ser texto")
    return sections

def wrapped(value, max_chars):
    lines = []
    for paragraph in str(value).splitlines() or [""]:
        lines.extend(textwrap.wrap(paragraph, width=max_chars, break_long_words=True,
                                   break_on_hyphens=False) or [""])
    return lines

def render_svg(data, paper="a4", orientation="landscape"):
    sections = validate(data)
    dimensions = {"a4": (1123, 794), "a3": (1587, 1123)}
    if paper not in dimensions or orientation not in ("landscape", "portrait"):
        raise ValueError("papel ou orientação inválidos")
    width, height = dimensions[paper]
    if orientation == "portrait":
        width, height = height, width
    dark, accent, pale, ink = PALETTES[data.get("style", "tecnico")]
    margin, gap, header = 44, 20, 142
    available = width - 2 * margin
    columns = 2 if orientation == "landscape" else 1
    card_width = (available - (columns - 1) * gap) / columns
    card_heights = []
    for section in sections:
        lines = wrapped(section["title"], max(15, int((card_width - 48) / 12)))
        items = [wrapped(i, max(18, int((card_width - 70) / 9))) for i in section.get("items", [])]
        card_heights.append(70 + len(lines) * 21 + sum(max(1, len(x)) * 20 + 10 for x in items))
    # Page-by-page packing: never shrink type to force content onto one sheet.
    pages = []
    current, heights = [], [header] * columns
    for index, section in enumerate(sections):
        card_height = card_heights[index]
        if card_height > height - margin - header:
            raise ValueError("seção extensa demais para uma página; divida em seções menores: " + section["title"])
        col = min(range(columns), key=lambda c: heights[c])
        if heights[col] + card_height + gap > height - margin:
            pages.append(current)
            current, heights = [], [header] * columns
            col = 0
        y = heights[col]
        current.append((index, col, y, card_height))
        heights[col] += card_height + gap
    if current:
        pages.append(current)
    svg_pages = []
    for page_no, page in enumerate(pages, 1):
        out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
               f'<rect width="{width}" height="{height}" fill="#f8fafc"/>',
               f'<rect width="{width}" height="116" fill="{dark}"/>',
               f'<title>{esc(data["title"])} — {page_no}</title>']
        title_lines = wrapped(data["title"], max(24, int((width - 100) / 23)))[:2]
        for n, line in enumerate(title_lines):
            out.append(f'<text x="{margin}" y="{49+n*35}" font-family="Arial,sans-serif" font-size="30" font-weight="bold" fill="white">{esc(line)}</text>')
        for index, col, y, card_height in page:
            section = sections[index]
            x = margin + col * (card_width + gap)
            out.append(f'<rect x="{x}" y="{y}" width="{card_width}" height="{card_height}" rx="16" fill="white" stroke="#cbd5e1"/>')
            out.append(f'<rect x="{x}" y="{y}" width="9" height="{card_height}" rx="4" fill="{accent}"/>')
            out.append(f'<circle cx="{x+34}" cy="{y+35}" r="18" fill="{accent}"/>')
            out.append(f'<text x="{x+34}" y="{y+41}" text-anchor="middle" font-family="Arial,sans-serif" font-size="16" font-weight="bold" fill="white">{index+1}</text>')
            cursor = y + 33
            for line in wrapped(section["title"], max(15, int((card_width-85)/12))):
                out.append(f'<text x="{x+62}" y="{cursor+5}" font-family="Arial,sans-serif" font-size="19" font-weight="bold" fill="{ink}">{esc(line)}</text>')
                cursor += 21
            cursor += 24
            for item in section.get("items", []):
                lines = wrapped(item, max(18, int((card_width-80)/9)))
                out.append(f'<circle cx="{x+36}" cy="{cursor-5}" r="4" fill="{accent}"/>')
                for line in lines:
                    out.append(f'<text x="{x+51}" y="{cursor}" font-family="Arial,sans-serif" font-size="16" fill="#334155">{esc(line)}</text>')
                    cursor += 20
                cursor += 10
        out.append(f'<text x="{width-margin}" y="{height-17}" text-anchor="end" font-family="Arial,sans-serif" font-size="12" fill="#64748b">{page_no}/{len(pages)}</text>')
        out.append("</svg>")
        svg_pages.append("\n".join(out))
    return svg_pages

def main():
    p = argparse.ArgumentParser()
    p.add_argument("input")
    p.add_argument("--out", default="saida")
    p.add_argument("--paper", choices=("a4", "a3"), default="a4")
    p.add_argument("--orientation", choices=("landscape", "portrait"), default="landscape")
    args = p.parse_args()
    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    pages = render_svg(data, args.paper, args.orientation)
    dest = Path(args.out)
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "mapa.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    try:
        import cairosvg
    except ImportError:
        cairosvg = None
    for i, svg in enumerate(pages, 1):
        name = f"mapa-{i:02d}"
        (dest / f"{name}.svg").write_text(svg, encoding="utf-8")
        if cairosvg:
            cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=str(dest / f"{name}.png"))
            cairosvg.svg2pdf(bytestring=svg.encode("utf-8"), write_to=str(dest / f"{name}.pdf"))
    print(f"{len(pages)} página(s) gerada(s); PNG/PDF: {'sim' if cairosvg else 'não (instale cairosvg)'}")

if __name__ == "__main__":
    main()
