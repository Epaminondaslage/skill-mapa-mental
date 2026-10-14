---
name: mapas-mentais
description: Gera mapas mentais didáticos e coloridos, com diagramas editáveis e revisão ativa, a partir de material fornecido.
---

# Skill Mapas Mentais v2

Leia o material integralmente. Identifique tema central, subtópicos, conceitos, exemplos e relações. Não invente fatos. Escolha mapa radial, árvore, conceitual ou sequencial conforme o conteúdo. Organize um modelo JSON canônico e gere SVG editável, PNG e PDF vetorial quando CairoSVG estiver disponível. Use cores por ramo, textos legíveis e conexões explícitas. Valide cobertura, fidelidade, legibilidade e correspondência entre formatos. Para estudo, produza cinco perguntas, cinco flashcards e três pontos essenciais. Responda em português brasileiro, salvo solicitação contrária.

## Idioma de saída (português ou italiano)
- Padrão: português brasileiro (`pt-BR`). O usuário pode pedir `italiano` (`it-IT`) em qualquer execução.
- Antes de gerar o mapa, identificar o idioma solicitado. Se não estiver explícito, manter `pt-BR`; não presumir italiano apenas porque a fonte está em italiano.
- Aplicar o idioma selecionado a título, nós, conectores, legendas, perguntas, respostas, flashcards e checklist.
- Preservar nomes próprios, citações e termos técnicos na forma original quando necessário.
- Para `it-IT`, usar italiano natural, com acentuação correta; não misturar português nos textos do mapa.
- Registrar `language: "it-IT"` ou `"pt-BR"` no JSON. Conferir consistência linguística na validação.


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
