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
- Renderizar preferencialmente com `python3 scripts/export_visual.py <entrada.json> --out <diretorio> --paper a4 --orientation landscape` (requer CairoSVG e pypdf para PDF consolidado).
- Estilos disponíveis: `tecnico`, `diagnostico`, `referencia`, `conceitual`. Preservar o renderizador clássico `scripts/render.py` para mapas de nós e conexões.
- Para conteúdo longo, dividir em seções curtas; revisar visualmente a legibilidade de cada página.
- O exportador gera PDFs por página com CairoSVG, PDF consolidado quando pypdf também está instalado, e HTML offline com zoom e busca. Não prometer edição visual interativa de nós.

## Publicação longa: aproximadamente 150 páginas
- Quando o usuário solicitar um guia completo, planejar primeiro um índice editorial por capítulos e seções, com meta configurável de cerca de 150 páginas (não uma obrigação de completar exatamente 150).
- Priorizar uma unidade visual didática por página; dividir conteúdos extensos em várias páginas e não inventar tópicos para atingir a meta.
- Registrar para cada página título, objetivo, conteúdo de origem, seção/capítulo e ordem. Conferir cobertura do material fornecido.
- Gerar o conteúdo em lotes verificáveis (por exemplo, capítulos de 10 a 20 páginas), mantendo numeração e identidade visual consistentes.
- Consolidar as páginas em um único PDF; validar a contagem efetiva de páginas, ausência de páginas em branco e legibilidade antes da entrega.
- O renderizador atual não garante 150 páginas a partir de qualquer entrada: a quantidade depende do planejamento editorial e da densidade do conteúdo. Não declarar guia de 150 páginas pronto sem verificar o PDF resultante.

## Especificação editorial: livro de mapas visuais de um tema central
- A entrada é um **tema central específico**, acompanhado de fontes ou escopo autorizado. O resultado esperado é um livro PDF de aproximadamente 150 páginas, não 150 assuntos independentes.
- Cada página representa uma unidade pedagógica sobre **um subtema do tema central**, contendo preferencialmente 3 a 6 blocos relacionados por hierarquia, comparação, sequência, causa e efeito ou exemplo. Evitar páginas compostas somente por parágrafos extensos.
- Planejar primeiro um sumário hierárquico (tema → capítulos → subtemas → páginas), com progressão de conceitos introdutórios a aplicações, síntese e revisão. Distribuir as páginas de acordo com densidade e importância, sem cotas fixas por capítulo.
- Usar componentes visuais relevantes: mapas conceituais, fluxogramas, diagramas, tabelas sintéticas, exemplos, ícones e ilustrações quando os recursos de produção estiverem disponíveis. Não alegar que um recurso gráfico foi produzido se o renderizador ainda não o implementa.
- Manter unidade gráfica, legibilidade, fontes de informação e numeração de páginas. Reservar páginas para capa, sumário e encerramento conforme o projeto editorial, incluindo-as na contagem total.
- A meta de aproximadamente 150 páginas é uma preferência editorial, subordinada à fidelidade às fontes e à suficiência do conteúdo. Não repetir informação ou inventar fatos para alcançar a contagem.
- Distinguir o **planejamento do livro** da **geração e verificação do PDF**: somente considerar entregue quando o PDF único existir, tiver sido inspecionado e sua contagem de páginas confirmada.
