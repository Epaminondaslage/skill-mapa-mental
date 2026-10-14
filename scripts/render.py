#!/usr/bin/env python3
"""Renderizador SVG/PNG e JSON de mapas mentais (biblioteca padrão; PNG opcional)."""
import argparse
import html
import json
import math
from pathlib import Path

COLORS = ("#2563eb", "#16a34a", "#9333ea", "#ea580c", "#0891b2", "#be123c")
def escape(value):
    return html.escape(str(value), quote=True)

def validate(data):
    if not isinstance(data, dict) or not isinstance(data.get("title"), str) or not data["title"].strip():
        raise ValueError("title obrigatório")
    if data.get("language") not in ("pt-BR", "it-IT"):
        raise ValueError("language deve ser pt-BR ou it-IT")
    if data.get("layout") not in ("radial", "arvore", "conceitual", "sequencial"):
        raise ValueError("layout inválido")
    nodes = data.get("nodes")
    if not isinstance(nodes, list) or not nodes:
        raise ValueError("nodes deve ser uma lista não vazia")
    ids = []
    for node in nodes:
        if not isinstance(node, dict) or not isinstance(node.get("id"), str) or not node["id"]:
            raise ValueError("id inválido")
        if not isinstance(node.get("label"), str) or not node["label"].strip():
            raise ValueError("label inválido")
        ids.append(node["id"])
    if len(ids) != len(set(ids)):
        raise ValueError("IDs duplicados")
    lookup = {n["id"]: n for n in nodes}
    for node in nodes:
        parent = node.get("parent")
        if parent is not None and parent not in lookup:
            raise ValueError("parent inexistente")
        seen = {node["id"]}
        while parent is not None:
            if parent in seen:
                raise ValueError("ciclo na hierarquia")
            seen.add(parent)
            parent = lookup[parent].get("parent")
    for edge in data.get("edges", []):
        if edge.get("from") not in lookup or edge.get("to") not in lookup:
            raise ValueError("aresta inválida")
    return nodes

def render_svg(data):
    nodes = validate(data)
    layout = data["layout"]
    root = next((n for n in nodes if n.get("parent") is None), nodes[0])
    positions = {}
    if layout == "radial":
        width, height = 1400, 1000
        positions[root["id"]] = (700, 500)
        others = [n for n in nodes if n["id"] != root["id"]]
        for i, node in enumerate(others):
            angle = 2 * math.pi * i / max(len(others), 1) - math.pi / 2
            positions[node["id"]] = (700 + 360 * math.cos(angle), 500 + 360 * math.sin(angle))
    elif layout == "sequencial":
        width, height = max(1100, 270 * len(nodes) + 200), 480
        for i, node in enumerate(nodes):
            positions[node["id"]] = (180 + i * 270, 240)
    else:
        depths = {root["id"]: 0}
        remaining = [n for n in nodes if n["id"] != root["id"]]
        while remaining:
            progress = False
            for node in remaining[:]:
                parent = node.get("parent")
                if parent in depths:
                    depths[node["id"]] = depths[parent] + 1
                    remaining.remove(node)
                    progress = True
            if not progress:
                for node in remaining:
                    depths[node["id"]] = 1
                break
        counts = {d: list(depths.values()).count(d) for d in set(depths.values())}
        width = max(1100, 310 * (max(depths.values()) + 1))
        height = max(600, 160 * max(counts.values()) + 160)
        placed = {}
        for node in nodes:
            depth = depths[node["id"]]
            i = placed.get(depth, 0)
            placed[depth] = i + 1
            positions[node["id"]] = (170 + 290 * depth, (i + 1) * height / (counts[depth] + 1))
    output = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
              '<rect width="100%" height="100%" fill="#f8fafc"/>',
              f'<title>{escape(data["title"])}</title>']
    edges = data.get("edges")
    if edges is None:
        edges = [{"from": n["parent"], "to": n["id"]} for n in nodes if n.get("parent") is not None]
    for edge in edges:
        x1, y1 = positions[edge["from"]]
        x2, y2 = positions[edge["to"]]
        output.append(f'<path d="M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}" fill="none" stroke="#94a3b8" stroke-width="3"/>')
        if edge.get("label"):
            output.append(f'<text x="{(x1+x2)/2:.1f}" y="{(y1+y2)/2-10:.1f}" text-anchor="middle" font-size="15" fill="#334155">{escape(edge["label"])}</text>')
    for i, node in enumerate(nodes):
        x, y = positions[node["id"]]
        color = "#0f172a" if node["id"] == root["id"] else COLORS[(i - 1) % len(COLORS)]
        words = node["label"].split()
        lines, current = [], ""
        for word in words:
            if len(current + " " + word) > 23 and current:
                lines.append(current)
                current = word
            else:
                current = (current + " " + word).strip()
        if current:
            lines.append(current)
        if len(lines) > 3 or any(len(line) > 26 for line in lines):
            raise ValueError("Rótulo muito longo: " + node["label"])
        output.append(f'<g id="{escape(node["id"])}"><rect x="{x-120:.1f}" y="{y-42:.1f}" width="240" height="84" rx="18" fill="{color}"/>')
        for j, line in enumerate(lines):
            ty = y + (j - (len(lines)-1)/2)*21 + 6
            output.append(f'<text x="{x:.1f}" y="{ty:.1f}" font-family="Arial,sans-serif" font-size="17" font-weight="600" text-anchor="middle" fill="white">{escape(line)}</text>')
        output.append('</g>')
    output.append('</svg>')
    return "\n".join(output)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--out", default="saida")
    args = parser.parse_args()
    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    svg = render_svg(data)
    dest = Path(args.out)
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "mapa.svg").write_text(svg, encoding="utf-8")
    (dest / "mapa.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    try:
        import cairosvg
    except ImportError:
        print("SVG e JSON gerados. PNG opcional: instale cairosvg.")
    else:
        cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=str(dest / "mapa.png"))
        print("SVG, JSON e PNG gerados.")
if __name__ == "__main__":
    main()
