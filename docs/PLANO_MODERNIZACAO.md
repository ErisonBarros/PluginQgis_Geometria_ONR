# Plano de modernização — Gerador de Descrição de Polígonos

Este plano adapta boas práticas de um template QGIS ao repositório existente `PluginQgis_Geometria_ONR`. O objetivo é modernizar o plugin específico; não criar um repositório genérico independente.

## Decisões e pendências

| Tema | Situação |
|---|---|
| Nome | Gerador de Descrição de Polígonos – PyQGIS |
| Licença | GNU GPL-2.0-or-later escolhida; consultar o [texto oficial da GPLv2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt); incorporar `LICENSE` e identificadores nos metadados |
| Aplicação prevista | Inspeção e descrição técnica de polígonos, com foco em cadastro e unificação imobiliária |
| Versão mínima de QGIS | Pendente; declarar antes de definir compatibilidade e chamadas PyQGIS |
| CRS de referência | SIRGAS 2000 / EPSG:4674, EPSG:31984 e EPSG:31985; o CRS de cada camada deve ser identificado |
| Elipsoide para cálculos geodésicos | GRS80, quando adequado à operação |
| Versão instalável no repositório | Ainda não disponível no commit-base auditado |

## Fases de implementação

### Fase 1 — Base instalável

Criar `metadata.txt`, ponto de entrada, inicialização, ícone próprio, estrutura de módulos e diálogo inicial. Declarar versão mínima de QGIS e Python compatível. Preservar o histórico e as alterações existentes na branch do repositório.

**Aceite:** o plugin é reconhecido pelo QGIS, instala sem alterar dados do usuário e informa claramente sua versão e dependências.

### Fase 2 — Camadas e geometria

Permitir seleção explícita da camada vetorial e das feições selecionadas ou de toda a camada. Validar tipo Polygon/MultiPolygon, feições vazias e existência/validade do CRS. Processar geometrias copiadas, preservar os dados originais e identificar partes, anéis externos e anéis internos.

**Aceite:** testes sintéticos cobrem Polygon, MultiPolygon, furos, geometrias vazias e seleção de feições; inconsistências são exibidas e registradas.

### Fase 3 — CRS e geodésia

Identificar o CRS de origem de cada camada e realizar transformações com `QgsCoordinateTransform` e o contexto do projeto QGIS. Oferecer escolha explícita do CRS de saída. Configurar `QgsDistanceArea` com CRS e elipsoide coerentes, incluindo GRS80 quando aplicável.

**Aceite:** valores de área, perímetro, distâncias e azimutes, quando implementados, têm método, unidade, CRS e testes de referência documentados. Casas decimais não são apresentadas como medida de precisão posicional.

### Fase 4 — Qualidade e operações geométricas

Implementar verificações geométricas e topológicas progressivamente. Geometrias inválidas não devem ser apresentadas como aprovadas apenas por gerar um aviso. Se uma reparação for solicitada, operar em cópia e registrar a operação. Dissolução/unificação deve ser não destrutiva e comparada com os insumos.

**Aceite:** relatório identifica validade, erros e advertências; geometrias originais permanecem preservadas.

### Fase 5 — Descrição e exportação

Definir convenções de ordenação e orientação dos vértices, vértice inicial, fechamento de anéis, unidades, arredondamento e texto técnico. Implementar primeiro TXT e CSV. Avaliar DOCX e PDF após decidir layout e dependências opcionais.

**Aceite:** pré-visualização e arquivo exportado derivam do mesmo resultado validado; o relatório registra origem, CRS e parâmetros relevantes.

### Fase 6 — Interface, documentação e publicação

Manter README como apresentação e início rápido; criar documentação de arquitetura, instalação, uso e desenvolvimento. O `PROJECT_GUIDE.md` deve ser escrito com base no código real, distinguindo fatos, inferências e incógnitas. Separar testes unitários dos testes de integração dependentes do QGIS. Criar pacote/release somente depois da validação de instalação e exportação.

**Aceite:** comandos e instruções reproduzíveis; CI informa apenas verificações executadas; pacote não inclui arquivos de desenvolvimento desnecessários.

## Guardrails para o script de referência

O material de referência descreve seleção de camada, transformação, medições, extração de anéis/vértices e exportação TXT. Esses itens são requisitos propostos, não funcionalidades verificadas no repositório. Antes de reutilizar o exemplo:

- não usar `geom.clone()`; copiar com uma construção apropriada, como `QgsGeometry(geom)`;
- não medir/exportar como validada uma geometria após apenas emitir aviso de invalidez;
- verificar o CRS da geometria efetivamente medida, o contexto da transformação e o elipsoide;
- definir como apresentar o ponto repetido de fechamento dos anéis;
- tratar a formatação decimal como resolução numérica, não como precisão ou acurácia;
- substituir o uso de `iface.activeLayer()` e `print()` por interação nativa do plugin na versão distribuível.

## Testes e colaboração

Usar dados sintéticos, sem dados pessoais ou matrículas reais. Criar testes para Polygon/MultiPolygon, anéis internos, validade, transformação e exportação. Executar testes de integração no ambiente QGIS mínimo declarado; testes não executados devem permanecer marcados como não verificados.

Usar o Project Explainer como método para o guia de onboarding e o RepoDocs, após existir código substancial, para uma wiki complementar com referências a arquivos/linhas. Essas ferramentas documentais não são dependências de execução do plugin. Revisar toda saída gerada antes de publicá-la.

## Referências

- [Repositório do plugin](https://github.com/ErisonBarros/PluginQgis_Geometria_ONR)
- [Requisitos de publicação de plugins no QGIS](https://plugins.qgis.org/docs/publish)
- [Licença oficial do QGIS](https://qgis.org/license/)
- [Project Explainer Skill](https://github.com/Abdelouahedb/project-explainer-skill)
- [RepoDocs](https://github.com/aryrabelo/repodocs)
