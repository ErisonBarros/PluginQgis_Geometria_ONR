# Gerador de Descrição de Polígonos – PyQGIS

**Ferramenta independente em desenvolvimento para análise e descrição técnica de geometrias poligonais no QGIS, com orientações para preparar polígonos para o [Mapa do Registro de Imóveis (ONR)](#onr).**

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

<a id="onr"></a>

### Orientações para envio ao Mapa do Registro de Imóveis (ONR)

Esta seção resume os requisitos do *Mapa do Registro de Imóveis – Manual de Uso: Profissional Técnico* (ONR, versão 2.0) e mostra em que etapas o plugin ajuda. A plataforma fica em <https://mapa.onr.org.br/>. O ONR pode mudar seus requisitos, por isso confira sempre a versão vigente do manual antes de enviar.

> O plugin **não envia** dados ao ONR. Ele também **não cria** os campos de atributos exigidos e **não gera** o texto de coordenadas no formato da plataforma. Ele ajuda a validar a geometria, transformar as coordenadas para EPSG:4674 e conferir área e perímetro antes do envio.

#### Fluxo de trabalho

| Etapa | Onde | O que fazer | Papel do plugin |
|---|---|---|---|
| 1. Preparar a geometria | QGIS | Confirmar o SRC da camada, verificar a validade da geometria e o fechamento dos anéis | Indica geometria inválida (GEOS) no relatório |
| 2. Conferir medidas | QGIS | Comparar área e perímetro com a planta, o memorial e a matrícula | Calcula área e perímetro elipsoidais (GRS80) |
| 3. Obter as coordenadas em EPSG:4674 | QGIS | Transformar para SIRGAS 2000 geográfico, em graus decimais | Saída em EPSG:4674, com longitude e latitude por vértice |
| 4. Montar o arquivo de envio | QGIS / editor de texto | Shapefile com os atributos do ONR **ou** texto de coordenadas | Manual (veja abaixo) |
| 5. Enviar | Plataforma ONR | Módulo do Profissional Técnico, com certificado digital | Fora do escopo do plugin |
| 6. Acompanhar | Plataforma ONR | Conferir a situação do polígono ("Em análise" ou "Aprovado") | Fora do escopo do plugin |

#### Requisito geodésico

O manual exige coordenadas em **graus decimais**, no **datum SIRGAS 2000 (EPSG:4674)**. No plugin, escolha **SIRGAS 2000 geográfico (EPSG:4674)** como SRC de saída. Os resultados em UTM (EPSG:31985) servem para conferência métrica, mas não para o envio.

#### Opção 1 – Envio por coordenadas (longitude, latitude)

Regras de formatação do campo "Polígono", segundo o manual:

1. Cada par começa pela **longitude** e depois vem a **latitude**.
2. A longitude e a latitude de cada par ficam separadas por **vírgula** (`,`).
3. Os pares ficam separados por **ponto e vírgula** (`;`).
4. O último par **não leva** ponto e vírgula e deve ser **igual ao primeiro**, para fechar o polígono.
5. As quebras de linha e os espaços depois dos separadores são opcionais.

Exemplo de estrutura (coordenadas **fictícias**, só para mostrar o formato):

```text
-34.9512345678, -8.0551234567;
-34.9508765432, -8.0553456789;
-34.9510987654, -8.0557654321;
-34.9512345678, -8.0551234567
```

Como montar esse texto a partir do relatório do plugin:

- Gere o TXT com saída em **EPSG:4674**. Cada vértice aparece como `Vn: Longitude = …; Latitude = …`, já na ordem longitude e latitude que o ONR exige.
- O plugin lista todos os pontos do anel, inclusive o de fechamento. O último vértice repete o primeiro, como o ONR exige.
- Copie apenas os vértices do **CONTORNO EXTERNO**, monte cada par como `longitude, latitude` e separe os pares com `;`.
- Use **ponto** como separador decimal. Uma vírgula decimal se confundiria com o separador entre longitude e latitude.
- O formato por texto tem um único contorno. **Polígonos com anéis internos (furos) ou com várias partes** devem ser enviados por shapefile. Isso é uma interpretação técnica: o manual só descreve sequências simples de coordenadas.

> O plugin grava 10 casas decimais, o que equivale a cerca de 0,01 mm no terreno. Isso é **resolução numérica**, não acurácia. A qualidade posicional vem do levantamento e é declarada na categorização (campo `CLASSIFICA`).

#### Opção 2 – Envio por shapefile

- Envie os quatro arquivos do conjunto: **`.shp`, `.shx`, `.dbf` e `.prj`**, todos com o **mesmo nome-base**.
- Para enviar vários polígonos de uma vez, cada conjunto precisa ter um nome-base diferente (por exemplo, `poligono01.*` e `poligono02.*`).
- O manual recomenda nomes de camada e de arquivo **sem acentos, espaços ou caracteres especiais**.
- Para gravar o shapefile em EPSG:4674 no QGIS, use **Exportar → Salvar feições como…**, escolha o formato *ESRI Shapefile* e o SRC *EPSG:4674 – SIRGAS 2000*. O `.prj` é gerado automaticamente.

##### Atributos exigidos

O manual traz um script PyQGIS que cria a estrutura de campos abaixo. Os nomes têm no máximo 10 caracteres, por causa do limite do formato DBF.

| Campo | Conteúdo | Tipo criado pelo script |
|---|---|---|
| `TRANSCRI` | Número da transcrição do imóvel | Texto |
| `CNS` | Código Nacional da Serventia | Texto |
| `ENDERECO` | Endereço do imóvel | Texto |
| `NUMERO` | Número do imóvel | Texto |
| `CEP` | CEP do imóvel | Inteiro |
| `MUNICIPIO` | Município | Texto |
| `UF` | Unidade da Federação | Texto |
| `NOME_PROP` | Proprietário(s), separados por vírgula | Texto |
| `CPF_CNPJ` | CPF/CNPJ do(s) proprietário(s), separados por vírgula | Texto |
| `CONF_MAT` | Matrículas confrontantes | Texto |
| `CONF_NOM` | Nomes dos confrontantes | Texto |
| `NOME_IMO` | Nome do imóvel | Texto |
| `AREA_HA` | Área em hectares | Decimal (2 casas) |
| `AREA_M2` | Área em m² | Decimal (2 casas) |
| `PERIM_M` | Perímetro em metros | Decimal (2 casas) |
| `PERIM_KM` | Perímetro em quilômetros | Decimal (2 casas) |
| `CCIR_SNCR` | Número do CCIR | Texto |
| `SIGEF` | Código da parcela no SIGEF | Texto |
| `SNCI` | Número no SNCI | Texto |
| `CIB_NIRF` | CIB ou NIRF | Texto |
| `CAR` | Número do Cadastro Ambiental Rural | Texto |
| `CIF` | Cadastro Imobiliário Fiscal | Inteiro |
| `CLASSIFICA` | Categoria do polígono: `1` = A, `2` = B, `3` = C | Inteiro |

Categorias do campo `CLASSIFICA`, segundo o manual:

| Valor | Categoria | Descrição |
|---|---|---|
| `1` | A | Georreferenciados rurais com certificação, ou urbanos com ART |
| `2` | B | Georreferenciados sem certificação |
| `3` | C | Desenho sobre imagem de satélite ou Google Earth |

Campos que podem ser preenchidos com os resultados do plugin:

- `AREA_M2` = área (m²) do relatório
- `AREA_HA` = `AREA_M2` / 10 000
- `PERIM_M` = perímetro (m) do relatório
- `PERIM_KM` = `PERIM_M` / 1 000

Antes de preencher, confirme se a área a declarar é a elipsoidal (calculada pelo plugin), a plana em UTM ou a que consta no memorial e na matrícula. Use o mesmo critério em todos os documentos do processo.

##### Cuidados técnicos com o script de campos do manual

Estes pontos vêm da leitura do código publicado no manual. São uma **interpretação técnica** e convém confirmá-los com o ONR ou com a serventia:

| Ponto | Consequência | Recomendação |
|---|---|---|
| O script **apaga todos os atributos** da camada antes de criar os novos campos | Perda dos dados da tabela original | Rode o script numa **cópia** da camada (o próprio manual recomenda backup) |
| `CEP` e `CIF` são criados como **inteiro** | Zeros à esquerda se perdem (por exemplo, `01001000` vira `1001000`) | Confira o valor gravado e consulte o ONR se o CEP começar com zero |
| Campos decimais com **2 casas** | `AREA_HA` fica arredondada a 0,01 ha (100 m²), e o próprio manual mostra exemplo com 4 casas | Leve em conta esse arredondamento ao comparar com o memorial |
| O script usa `QVariant` para os tipos | Funciona no QGIS 3.x. No QGIS 4 (Qt6) pode precisar de ajuste | Rode no QGIS 3.x (LTR) |

> **Dados pessoais (LGPD):** `NOME_PROP`, `CPF_CNPJ` e `CONF_NOM` são dados pessoais. Não publique shapefiles preenchidos em repositórios públicos, inclusive neste. Guarde e compartilhe esses arquivos só pelos canais do processo registral.

#### Envio na plataforma (resumo)

1. Acesse <https://mapa.onr.org.br/> e clique no ícone do módulo do profissional técnico, na barra superior. Depois, clique em **"Acessar o módulo para envio de arquivos"**.
2. Entre com **certificado digital**, conectado ao computador, e escolha o acesso **"Profissional Técnico – CAU, CREA, CRT"**. No primeiro acesso, o sistema pede o cadastro e envia um e-mail de confirmação.
3. No menu lateral, vá em **Gerenciador de Imóveis → Carregar Polígonos**. No primeiro envio, é preciso aceitar os Termos de Uso.
4. Em **Tipo de Envio**, escolha *Arquivos Shapefile* ou *coordenadas*.
5. Preencha o formulário:
   - Estado, Comarca e Serventia (o código CNS é preenchido automaticamente);
   - número da prenotação do título;
   - finalidade do envio;
   - categorização (exatidão cartográfica);
   - tipo (urbano ou rural);
   - descrição do polígono.
6. Envie os arquivos (**Selecionar arquivos → Enviar Formulário**) ou cole as coordenadas (**Cadastrar polígono**).

**Acompanhamento.** Em **Lotes de Polígonos Enviados** e **Polígonos Enviados**, confira os detalhes e a **Situação** ("Em análise" ou "Aprovado"). Pelo manual:

- acompanhar o status é responsabilidade do profissional técnico;
- a serventia faz a análise, e não há prazo estimado;
- polígonos com erro precisam ser reenviados já corrigidos;
- depois da aprovação, o profissional não consegue mais editar os campos. Dados descritivos, como a prenotação, só a serventia altera.

#### Lista de verificação antes do envio

- [ ] A camada tem o SRC correto e a geometria é válida (sem autointerseções nem vértices duplicados).
- [ ] O relatório do plugin foi gerado em **EPSG:4674**, e a área e o perímetro conferem com a planta e o memorial.
- [ ] A ordem é **longitude, latitude**, o separador decimal é o ponto, e o primeiro e o último vértice são iguais.
- [ ] No shapefile: `.shp`, `.shx`, `.dbf` e `.prj` com o mesmo nome-base, sem acentos nem espaços.
- [ ] Os campos de atributos foram criados numa **cópia** da camada, e o `CLASSIFICA` corresponde à categoria do levantamento.
- [ ] A prenotação, a serventia e a finalidade conferem com o título protocolado.

#### Suporte da plataforma

Dúvidas sobre a plataforma do ONR devem ir ao suporte do ONR (no manual: `servicedesk@onr.org.br`, telefone (11) 3195-2290). Problemas do **plugin** devem ser relatados nas [*issues* deste repositório](https://github.com/ErisonBarros/PluginQgis_Geometria_ONR/issues).

#### Próximas etapas do plugin relacionadas ao ONR

Planejadas, **ainda não implementadas**:

- exportar o texto de coordenadas pronto para o campo "Polígono" do ONR;
- exportar um shapefile em EPSG:4674 com a estrutura de atributos do ONR, sem apagar os dados da camada original;
- verificar fechamento, vértices duplicados e número de partes e anéis antes da exportação.

### Documentação

- Site do projeto: <https://erisonbarros.github.io/PluginQgis_Geometria_ONR/>

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

### Use with the ONR Property Registry Map

The Portuguese section above summarizes the submission requirements of the ONR *Mapa do Registro de Imóveis – Professional Technician Manual* (version 2.0). Polygons are submitted at <https://mapa.onr.org.br/> by a technician logged in with a digital certificate. There are two ways to submit:

- a **shapefile set** (`.shp`, `.shx`, `.dbf`, `.prj`, same base name) with the ONR attribute schema (23 fields, including `CLASSIFICA` for accuracy category A/B/C);
- a **coordinate string**: `longitude, latitude` pairs separated by `;`, closed by repeating the first pair.

In both cases coordinates must be in **SIRGAS 2000 geographic (EPSG:4674), decimal degrees**. This plugin helps validate geometry, transform coordinates to EPSG:4674, and check GRS80 area and perimeter. It does not submit data, create the ONR attribute fields, or build the coordinate string yet; these are planned. Owner names and CPF/CNPJ are personal data: do not publish filled attribute tables in public repositories.

### Documentation

- Project site: <https://erisonbarros.github.io/PluginQgis_Geometria_ONR/>

- [Plugin installation (PT-BR)](INSTALACAO.md)

- [Technical audit](docs/AUDITORIA_TECNICA.md)

- [Modernization plan](docs/PLANO_MODERNIZACAO.md)

- [Technical review of supplied code](docs/REVISAO_TECNICA_CODIGO_FORNECIDO.md)

- [PyQGIS specification](docs/ESPECIFICACAO_PYQGIS.md)

A `PROJECT_GUIDE.md` will be written once real code and execution flows exist. RepoDocs may be used to generate a complementary source-cited wiki. Documentation must not present unverified capabilities as implemented.

### License and disclaimer

Selected license: **GNU GPL-2.0-or-later**. See `LICENSE` and the [official GPL version 2 text](https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt).

This is an independent project. It is not an official product, nor is it endorsed by ONR. No official ONR branding is used.
