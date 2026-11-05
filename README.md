# Gerador de Descrição de Polígonos – PyQGIS

**Ferramenta independente em desenvolvimento para análise e descrição técnica de geometrias poligonais no QGIS.**

> **Estado:** versão inicial 1.0.0 do plugin (pasta `gerador_descricao_poligonos/`), ainda sem testes automatizados executados em QGIS. Use apenas para avaliação técnica; o relatório gerado é auxiliar e não substitui memorial descritivo nem validação registral.

## Português

### Objetivo

O projeto pretende apoiar a inspeção, validação e descrição técnica de polígonos e multipolígonos no QGIS, com aplicação prevista em trabalhos de cadastro e unificação imobiliária. Os resultados devem preservar a rastreabilidade da feição de origem, do CRS e dos parâmetros de processamento.

### Escopo planejado

O fluxo em avaliação contempla seleção de camadas vetoriais, identificação de Polygon/MultiPolygon e de anéis externos/internos, verificação de CRS, transformação de coordenadas, extração de vértices, medições e exportação de descrição. O primeiro escopo sugerido é uma versão instalável com validações essenciais e exportação TXT/CSV.

Dissolução, distâncias e azimutes por segmento, confrontantes, validação topológica abrangente, interface gráfica completa e exportações DOCX/PDF permanecem etapas futuras. Nenhuma dessas funções deve ser entendida como implementada nesta versão do repositório.

### Referenciais previstos

O planejamento considera SIRGAS 2000 geográfico (EPSG:4674), SIRGAS 2000 / UTM 24S (EPSG:31984) e SIRGAS 2000 / UTM 25S (EPSG:31985). A seleção do CRS de saída deverá ser explícita e adequada ao trabalho. As transformações devem respeitar o CRS de origem de cada camada e o contexto de transformação do projeto QGIS. Para medições geodésicas compatíveis com a finalidade, o projeto prevê o elipsoide GRS80.

Casas decimais indicam resolução de representação, não precisão ou acurácia posicional do levantamento.

### Estado do repositório

O pacote `gerador_descricao_poligonos/` contém `metadata.txt` (versão 1.0.0, QGIS mínimo 3.16), `__init__.py`, `plugin.py` e ícone. Implementado: seleção de camada poligonal, feições selecionadas ou todas, saída em EPSG:4674 ou EPSG:31985, área e perímetro com GRS80, identificação de partes e anéis e exportação TXT. Ainda não há suíte de testes automatizados nem pacote publicado no repositório oficial de plugins do QGIS. Instruções de instalação: [`INSTALACAO.md`](INSTALACAO.md).

### Documentação

- [Instalação do plugin](INSTALACAO.md)

- [Auditoria técnica](docs/AUDITORIA_TECNICA.md)

- [Plano de modernização](docs/PLANO_MODERNIZACAO.md)

- [Revisão técnica do código fornecido](docs/REVISAO_TECNICA_CODIGO_FORNECIDO.md)

- [Especificação PyQGIS](docs/ESPECIFICACAO_PYQGIS.md)

O `PROJECT_GUIDE.md` será escrito depois que o código e os fluxos reais existirem. O RepoDocs poderá gerar uma wiki técnica complementar com referências a arquivos e linhas; nenhum guia deve descrever como existente uma funcionalidade que não esteja comprovada no código.

### Licença e responsabilidade

Licença escolhida: **GNU GPL-2.0-or-later**. Consulte o arquivo `LICENSE` e o [texto oficial da GPL versão 2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt).

Este é um projeto independente. Não é um produto oficial, homologado ou endossado pelo ONR e não utiliza marca oficial do ONR.

## English

### Purpose

This project is an independent QGIS/PyQGIS tool under development for inspecting, validating, and describing polygon and multipolygon geometries, with a planned application in land-cadastre and property-unification workflows. Outputs are intended to preserve traceability to the source feature, CRS, and processing parameters.

### Planned scope

The proposed workflow covers vector-layer selection, Polygon/MultiPolygon and ring identification, CRS checks and transformations, vertex extraction, measurements, and description export. The suggested first release is an installable plugin with essential validation and TXT/CSV export.

Dissolve operations, segment distances and azimuths, adjoining-property identification, comprehensive topology checks, a complete graphical interface, and DOCX/PDF export remain future work. They are not implemented or verified in the repository at this stage.

### Planned reference systems

The design considers SIRGAS 2000 geographic (EPSG:4674), SIRGAS 2000 / UTM zone 24S (EPSG:31984), and SIRGAS 2000 / UTM zone 25S (EPSG:31985). Output CRS selection must be explicit and suitable for the task. Transformations must respect each layer's source CRS and the QGIS project's transform context. GRS80 is the planned ellipsoid for geodetic measurements where appropriate.

Decimal places describe numeric representation; they do not establish survey accuracy or positional precision.

### Repository status

The `gerador_descricao_poligonos/` package contains `metadata.txt` (version 1.0.0, minimum QGIS 3.16), `__init__.py`, `plugin.py`, and an icon. Implemented: polygon-layer selection, selected or all features, output in EPSG:4674 or EPSG:31985, GRS80 area and perimeter, part/ring identification, and TXT export. There is no automated test suite yet and no release on the official QGIS plugin repository. Installation instructions (Portuguese): see [`INSTALACAO.md`](INSTALACAO.md).

### Documentation

- [Plugin installation (PT-BR)](INSTALACAO.md)

- [Technical audit](docs/AUDITORIA_TECNICA.md)

- [Modernization plan](docs/PLANO_MODERNIZACAO.md)

- [Technical review of supplied code](docs/REVISAO_TECNICA_CODIGO_FORNECIDO.md)

- [PyQGIS specification](docs/ESPECIFICACAO_PYQGIS.md)

A `PROJECT_GUIDE.md` will be written once real code and execution flows exist. RepoDocs may be used to generate a complementary source-cited wiki. Documentation must not present unverified capabilities as implemented.

### License and disclaimer

Selected license: **GNU GPL-2.0-or-later**. See `LICENSE` and the [official GPL version 2 text](https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt).

This is an independent project. It is not an official product, nor is it endorsed by ONR. No official ONR branding is used.
