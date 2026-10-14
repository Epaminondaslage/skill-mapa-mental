# Infográficos técnicos — primeira implementação

O formato de referência é o mapa visual técnico da coleção MikroTik, interpretado como **composição de páginas** e não como mapa radial. Esta é uma implementação inicial, sem reprodução literal de arte de terceiros.

## Modelo JSON

Campos obrigatórios: `title` e `sections`. Cada seção contém `title` e `items` (lista de textos). Campos opcionais: `language` (`pt-BR` ou `it-IT`) e `style` (`tecnico`, `diagnostico`, `referencia`, `conceitual`).

## Renderização

```bash
python3 scripts/render_infografico.py examples/infografico-tecnico.json --out saida-infografico --paper a4 --orientation landscape
```

Também aceita `--paper a3` e `--orientation portrait`. O script gera um SVG por página, JSON e, quando CairoSVG está instalado, PNG/PDF por página. Se uma seção exceder a área imprimível, a execução falha com erro explícito em vez de cortar texto.

## Limites desta versão

- Não há composição de imagens externas, capturas de tela ou ícones.
- Não há PDF multipágina consolidado.
- Não há editor HTML interativo.
- A quebra de linha é aproximada por caracteres; verificar visualmente antes de imprimir.
- O renderizador tradicional `scripts/render.py` continua disponível e inalterado.
