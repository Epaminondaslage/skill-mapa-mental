---
name: mapas-mentais
description: Gera mapas mentais didáticos e coloridos, com diagramas editáveis e revisão ativa, a partir de material fornecido.
---

# Skill Mapas Mentais v2

Leia o material integralmente. Identifique tema central, subtópicos, conceitos, exemplos e relações. Não invente fatos. Escolha mapa radial, árvore, conceitual ou sequencial conforme o conteúdo. Organize um modelo JSON canônico e gere SVG editável, PNG e PDF vetorial quando CairoSVG estiver disponível. Use cores por ramo, textos legíveis e conexões explícitas. Valide cobertura, fidelidade, legibilidade e correspondência entre formatos. Para estudo, produza cinco perguntas, cinco flashcards e três pontos essenciais. Respeite o idioma explicitamente escolhido pelo usuário.

## Seleção obrigatória de idioma
- Idiomas suportados: português brasileiro (`pt-BR`) e italiano (`it-IT`).
- Se o usuário não indicar o idioma de saída, perguntar **“Você deseja o mapa em português ou italiano?”** antes de gerar qualquer arquivo.
- Se o usuário indicar um idioma, utilizá-lo sem perguntar novamente.
- Se solicitar ambos, gerar duas versões completas e equivalentes do mapa, mantendo IDs, relações e disposição visual correspondentes; usar nomes de arquivo distintos, como `mapa-pt-BR.svg` e `mapa-it-IT.svg`.
- Aplicar o idioma escolhido a títulos, rótulos, conectores, legendas, perguntas, respostas, flashcards e relatório de validação.
- O idioma do documento de entrada não determina automaticamente o idioma de saída.
- Preservar nomes próprios, citações e terminologia técnica quando necessário. Conferir ortografia e consistência de idioma antes da entrega.
- Registrar o idioma escolhido no campo `language` do JSON canônico.

## Exportação PDF
- Gerar `mapa.pdf` diretamente do SVG usando CairoSVG, preservando formas e textos vetoriais quando suportado.
- Instalar dependência opcional: `python3 -m pip install cairosvg`.
- Se CairoSVG não estiver instalado, entregar SVG/JSON e informar que PNG/PDF não foram gerados; nunca declarar PDF gerado sem verificar o arquivo.
- Para impressão em A4/A3, adequar layout e verificar margens e legibilidade antes de exportar.

## Infográficos técnicos (estilo prioritário)
- Para conteúdos procedimentais, diagnósticos, comandos ou mapas visuais de consulta, priorizar o estilo de infográfico técnico inspirado na organização didática dos exemplos MikroTik.
- Consultar `references/infografico-tecnico.md` e gerar o JSON com `title`, `language`, `style` e `sections`.
- Renderizar com `python3 scripts/render_infografico.py <entrada.json> --out <diretorio> --paper a4 --orientation landscape`.
- Estilos disponíveis: `tecnico`, `diagnostico`, `referencia`, `conceitual`. Preservar o renderizador clássico `scripts/render.py` para mapas de nós e conexões.
- Para conteúdo longo, dividir em seções curtas; revisar visualmente a legibilidade de cada página.
- Esta versão produz PDFs individuais por página quando CairoSVG está instalado; não prometer PDF multipágina ou editor interativo.
