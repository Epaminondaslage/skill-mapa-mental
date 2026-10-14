# Skill Mapas Mentais v2 — Codex

Geração de mapas didáticos e coloridos com SVG editável, JSON canônico e PNG opcional.

## Instalação
```bash
git clone https://github.com/Epaminondaslage/skill-mapa-mental.git ~/.agents/skills/mapas-mentais
```
Reinicie a sessão do Codex.

## Execução
```bash
python3 scripts/render.py examples/exemplo.json --out saida
python3 -m unittest discover -s tests -v
```
PNG: instale `cairosvg` em ambiente virtual. A geração de SVG/JSON usa somente Python padrão.

## Observações
O renderizador produz layouts básicos. Confira a legibilidade e a fidelidade semântica antes de usar mapas complexos. Divida conteúdos extensos em mapas complementares.

## Idiomas
A skill oferece português brasileiro (`pt-BR`, padrão) e italiano (`it-IT`). Exemplo: “Use a skill mapas-mentais para criar um mapa conceitual **em italiano** sobre este PDF”. A escolha deve valer para títulos, ramos, conectores e revisão ativa.


## Seleção de idioma
Antes de gerar, o Codex deve perguntar **“Você deseja o mapa em português ou italiano?”** quando o pedido não especificar idioma. São suportados `pt-BR` e `it-IT`. Também é possível pedir os dois idiomas, com arquivos separados e estrutura equivalente.
