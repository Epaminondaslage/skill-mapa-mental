#!/usr/bin/env python3
"""Exporta infográficos em SVG, PNG, PDF multipágina e HTML offline interativo."""
import argparse
import html
import json
from pathlib import Path

from render_infografico import render_svg

def export(data, output, paper="a4", orientation="landscape", dpi=160):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    pages = render_svg(data, paper, orientation)
    (output / "mapa.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    try:
        import cairosvg
    except (ImportError, OSError):
        cairosvg = None
    try:
        from pypdf import PdfReader, PdfWriter
    except ImportError:
        PdfReader = PdfWriter = None
    pdfs = []
    for i, svg in enumerate(pages, 1):
        name = f"mapa-{i:02d}"
        (output / (name + ".svg")).write_text(svg, encoding="utf-8")
        if cairosvg:
            cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=str(output / (name + ".png")), output_width=None, dpi=dpi)
            pdf_file = output / (name + ".pdf")
            cairosvg.svg2pdf(bytestring=svg.encode("utf-8"), write_to=str(pdf_file))
            pdfs.append(pdf_file)
    if pdfs and PdfWriter:
        writer = PdfWriter()
        for file in pdfs:
            writer.append(str(file))
        with (output / "mapa-completo.pdf").open("wb") as fp:
            writer.write(fp)
    viewer = build_html(data["title"], pages)
    (output / "mapa-interativo.html").write_text(viewer, encoding="utf-8")
    return {"pages": len(pages), "png_pdf": bool(cairosvg), "merged_pdf": bool(pdfs and PdfWriter)}

def build_html(title, pages):
    safe_title = html.escape(title, quote=True)
    # SVG is generated exclusively by render_svg, which XML-escapes all user labels.
    bodies = "\n".join(
        f'<section class="page" data-page="{i}" aria-label="Página {i}">{svg}</section>'
        for i, svg in enumerate(pages, 1)
    )
    return """<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>""" + safe_title + """</title>
<style>
:root{font-family:system-ui,sans-serif;color:#172554;background:#e8edf5}
*{box-sizing:border-box}body{margin:0}
header{position:sticky;top:0;z-index:2;background:#0b1730;color:white;padding:12px 20px;display:flex;gap:10px;align-items:center;flex-wrap:wrap}
header strong{margin-right:auto}button,input{font:inherit;padding:8px;border:1px solid #94a3b8;border-radius:6px}
button{cursor:pointer;background:white;color:#0b1730}button:focus-visible,input:focus-visible{outline:3px solid #f59e0b}
#counter{min-width:90px;text-align:center}main{padding:22px;overflow:auto;text-align:center}
.page{display:none;transform-origin:top center;box-shadow:0 6px 20px #33415533;background:white;margin:auto;width:max-content}
.page.active{display:block}.page svg{display:block;max-width:none}
mark{fill:#fde68a} .match{filter:drop-shadow(0 0 5px #f59e0b)}
@media print{header{display:none}main{padding:0;overflow:visible}.page,.page.active{display:block;box-shadow:none;break-after:page;transform:none!important;margin:0}.page svg{width:100%;height:auto}}
</style></head><body><header><strong>""" + safe_title + """</strong>
<label for="search">Buscar</label><input id="search" type="search" placeholder="Conceito ou termo">
<button id="prev" aria-label="Página anterior">Anterior</button><span id="counter"></span>
<button id="next" aria-label="Próxima página">Próxima</button>
<button id="minus" aria-label="Reduzir zoom">−</button><span id="zoom"></span>
<button id="plus" aria-label="Aumentar zoom">+</button>
<button id="print">Imprimir</button></header><main>""" + bodies + """</main>
<script>
(()=>{'use strict';
const pages=[...document.querySelectorAll('.page')], search=document.getElementById('search');
let index=0,zoom=1;
function show(){pages.forEach((p,i)=>{p.classList.toggle('active',i===index);p.style.transform='scale('+zoom+')';p.style.marginBottom=i===index?((zoom-1)*p.offsetHeight)+'px':'0'});document.getElementById('counter').textContent=(index+1)+' / '+pages.length;document.getElementById('zoom').textContent=Math.round(zoom*100)+'%'}
document.getElementById('prev').onclick=()=>{index=Math.max(0,index-1);show()};
document.getElementById('next').onclick=()=>{index=Math.min(pages.length-1,index+1);show()};
document.getElementById('plus').onclick=()=>{zoom=Math.min(2,zoom+.1);show()};
document.getElementById('minus').onclick=()=>{zoom=Math.max(.5,zoom-.1);show()};
document.getElementById('print').onclick=()=>window.print();
search.addEventListener('input',()=>{const term=search.value.trim().toLocaleLowerCase();pages.forEach(p=>p.querySelectorAll('svg text').forEach(t=>t.classList.toggle('match',!!term&&t.textContent.toLocaleLowerCase().includes(term))));if(term){const found=pages.findIndex(p=>p.querySelector('.match'));if(found>=0)index=found}show()});
show();
})();
</script></body></html>"""

def main():
    p = argparse.ArgumentParser()
    p.add_argument("input")
    p.add_argument("--out", default="saida")
    p.add_argument("--paper", choices=("a4", "a3"), default="a4")
    p.add_argument("--orientation", choices=("landscape", "portrait"), default="landscape")
    p.add_argument("--dpi", type=int, default=160)
    args = p.parse_args()
    if not 72 <= args.dpi <= 600:
        p.error("dpi deve estar entre 72 e 600")
    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    status = export(data, args.out, args.paper, args.orientation, args.dpi)
    print(json.dumps(status, ensure_ascii=False))
    if not status["merged_pdf"]:
        print("Para PDF único: python3 -m pip install cairosvg pypdf")

if __name__ == "__main__":
    main()
