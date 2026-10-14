---
name: mapas-mentais
description: Gera mapas mentais didáticos e coloridos, com diagramas editáveis e revisão ativa, a partir de material fornecido.
---

# Skill Mapas Mentais v2

Leia o material integralmente. Identifique tema central, subtópicos, conceitos, exemplos e relações. Não invente fatos. Escolha mapa radial, árvore, conceitual ou sequencial conforme o conteúdo. Organize um modelo JSON canônico e gere SVG editável e PNG quando houver renderizador disponível. Use cores por ramo, textos legíveis e conexões explícitas. Valide cobertura, fidelidade, legibilidade e correspondência entre formatos. Para estudo, produza cinco perguntas, cinco flashcards e três pontos essenciais. Responda em português brasileiro, salvo solicitação contrária.

## Idioma de saída (português ou italiano)
- Padrão: português brasileiro (`pt-BR`). O usuário pode pedir `italiano` (`it-IT`) em qualquer execução.
- Antes de gerar o mapa, identificar o idioma solicitado. Se não estiver explícito, manter `pt-BR`; não presumir italiano apenas porque a fonte está em italiano.
- Aplicar o idioma selecionado a título, nós, conectores, legendas, perguntas, respostas, flashcards e checklist.
- Preservar nomes próprios, citações e termos técnicos na forma original quando necessário.
- Para `it-IT`, usar italiano natural, com acentuação correta; não misturar português nos textos do mapa.
- Registrar `language: "it-IT"` ou `"pt-BR"` no JSON. Conferir consistência linguística na validação.
