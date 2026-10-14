# Modelo JSON

Campos: `title` (texto), `language` (`pt-BR` ou `it-IT`), `layout` (`radial`, `arvore`, `conceitual`, `sequencial`), `nodes` (lista de `{id,label,parent}`) e `edges` (opcional, `{from,to,label}`). IDs devem ser únicos; `parent` deve referir a um nó existente ou ser `null`. Sem idioma solicitado, perguntar ao usuário antes de produzir o JSON.
