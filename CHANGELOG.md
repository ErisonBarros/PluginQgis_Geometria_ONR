# Changelog

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [Não publicado]

### Documentação
- README: orientações para envio de polígonos ao Mapa do Registro de Imóveis (ONR), com base no Manual do Profissional Técnico v2.0: formato de coordenadas, shapefile, atributos, categorias, fluxo na plataforma e lista de verificação.
- Novo layout do site (GitHub Pages): cabeçalho com destaque e botão de download, cartões de recursos, sumário lateral automático, modo escuro, layout responsivo e botão de copiar nos blocos de código.
- Site no GitHub Pages gerado a partir do `README.md`, com atualização automática via GitHub Actions (`.github/workflows/pages.yml`, `_config.yml`).
- `INSTALACAO.md` com instruções de instalação, ativação, atualização, remoção e solução de problemas.

## [1.0.0] - 2026-11-04

### Adicionado
- Pacote do plugin `gerador_descricao_poligonos` (QGIS ≥ 3.16): seleção de camada poligonal, processamento de feições selecionadas ou de todas, saída em EPSG:4674 ou EPSG:31985, área e perímetro geodésicos (GRS80), identificação de partes e anéis, exportação TXT UTF-8.
- Licença GPL-2.0-or-later.
- Documentação técnica em `docs/` (auditoria, plano de modernização, revisão técnica, especificação).
