# Infográficos técnicos — primeira implementação

O formato de referência é o mapa visual técnico da coleção MikroTik, interpretado como **composição de páginas** e não como mapa radial. Esta é uma implementação inicial, sem reprodução literal de arte de terceiros.

## Modelo JSON

O layout modular usa `title` e `sections`. Cada seção contém `title` e `items` (lista de textos). Campos opcionais: `language` (`pt-BR` ou `it-IT`) e `style` (`tecnico`, `diagnostico`, `referencia`, `conceitual`).

### Layout de mapa de decisão

Use `layout: "decision"` quando o leitor precisar responder perguntas e chegar a recomendações. Esse modo gera uma página com pergunta inicial, de dois a quatro caminhos, opções internas e uma síntese final.

Campos:

- `prompt`: pergunta inicial;
- `branches`: de dois a quatro caminhos, cada um com `title` e de uma a três `options`;
- cada opção exige `question` e `result`, com `detail` opcional;
- `subtitle` e `takeaway` são opcionais.

Veja `examples/mapa-decisao.json`. Prefira orientação retrato para quatro caminhos e paisagem para dois ou três. O objetivo é revelar critérios de escolha, não transformar qualquer conteúdo em árvore de decisão.

## Renderização

```bash
python3 scripts/render_infografico.py examples/infografico-tecnico.json --out saida-infografico --paper a4 --orientation landscape

python3 scripts/export_visual.py examples/mapa-decisao.json --out saida-decisao --paper a4 --orientation portrait
```

Também aceita `--paper a3` e `--orientation portrait`. O script gera um SVG por página, JSON e, quando CairoSVG está instalado, PNG/PDF por página. Se uma seção exceder a área imprimível, a execução falha com erro explícito em vez de cortar texto.

## Limites desta versão

- Não há composição de imagens externas, capturas de tela ou biblioteca de ícones.
- O PDF consolidado depende de CairoSVG, da biblioteca nativa Cairo e de pypdf.
- Não há editor HTML interativo.
- O mapa de decisão é uma composição de uma página; árvores com ramificação recursiva continuam fora deste renderizador.
- A quebra de linha é aproximada por caracteres; verificar visualmente antes de imprimir.
- O renderizador tradicional `scripts/render.py` continua disponível e inalterado.
