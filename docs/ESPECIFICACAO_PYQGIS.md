# **Gerador de Descrição de Polígonos – PyQGIS**

## **1\. Identificação do projeto**

| Campo | Descrição |
| ----- | ----- |
| Projeto | Gerador de Descrição de Polígonos |
| Linguagem | Python |
| API | PyQGIS |
| Software | QGIS |
| Datum | SIRGAS 2000 |
| EPSG geográfico | 4674 |
| EPSG projetado | 31985 |
| Aplicação | Unificação de imóveis urbanos |

## **2\. Fluxograma do processamento**

```
flowchart TD
    A[Início] --> B[Selecionar camada]
    B --> C{Geometria poligonal?}
    C -->|Não| D[Mensagem de erro]
    C -->|Sim| E[Identificar CRS]
    E --> F[Transformar coordenadas]
    F --> G[Extrair vértices]
    G --> H[Calcular área e perímetro]
    H --> I[Organizar descrição]
    I --> J[Exportar TXT]
    J --> K[Fim]
```

## **3\. Desenvolvimento do código**

### **3.1. Importação das bibliotecas**

**Objetivo:** importar as bibliotecas necessárias para o processamento geoespacial.

```
from qgis.core import (
    QgsProject,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsDistanceArea,
    QgsWkbTypes
)

from qgis.PyQt.QtWidgets import (
    QFileDialog,
    QMessageBox
)
```

### **3.2. Identificação da camada ativa**

**Objetivo:** identificar a camada selecionada no QGIS e verificar seu tipo geométrico.

```
layer = iface.activeLayer()

if layer is None:
    raise Exception("Selecione uma camada vetorial.")

if layer.geometryType() != QgsWkbTypes.PolygonGeometry:
    raise Exception("A camada não é poligonal.")
```

### **3.3. Definição do sistema de referência**

**Objetivo:** estabelecer o sistema de referência geográfico SIRGAS 2000\.

```
crs_saida = QgsCoordinateReferenceSystem("EPSG:4674")
```

### **3.4. Transformação das coordenadas**

**Objetivo:** transformar as coordenadas da camada original para o sistema de saída.

```
transform = QgsCoordinateTransform(
    layer.crs(),
    crs_saida,
    QgsProject.instance()
)
```

Aplicação da transformação:

```
geom_saida = geom.clone()
geom_saida.transform(transform)
```

### **3.5. Configuração geodésica**

**Objetivo:** configurar os cálculos de área e perímetro utilizando o elipsoide GRS80.

```
distance = QgsDistanceArea()

distance.setSourceCrs(
    crs_saida,
    QgsProject.instance().transformContext()
)

distance.setEllipsoid("GRS80")
```

### **3.6. Identificação dos anéis geométricos**

**Objetivo:** identificar os anéis externos e internos dos polígonos.

```
def obter_aneis(geom):

    if geom.isMultipart():
        return geom.asMultiPolygon()

    return [geom.asPolygon()]
```

### **3.7. Formatação das coordenadas**

**Objetivo:** padronizar a apresentação das coordenadas geográficas.

```
def formatar_coord(valor):
    return f"{valor:.10f}"
```

### **3.8. Seleção das feições**

**Objetivo:** processar as feições selecionadas ou toda a camada.

```
features = (
    layer.selectedFeatures()
    if layer.selectedFeatureCount() > 0
    else layer.getFeatures()
)

features = list(features)

if not features:
    raise Exception("Nenhum polígono encontrado.")
```

### **3.9. Cálculo de área e perímetro**

**Objetivo:** calcular as dimensões geométricas dos polígonos.

```
area = distance.measureArea(geom_saida)

perimetro = distance.measurePerimeter(geom_saida)
```

### **3.10. Extração dos vértices**

**Objetivo:** percorrer os anéis e extrair as coordenadas de cada vértice.

```
for vertice_idx, ponto in enumerate(anel):

    longitude = formatar_coord(ponto.x())
    latitude = formatar_coord(ponto.y())

    print(
        f"V{vertice_idx + 1}: "
        f"Longitude = {longitude}; "
        f"Latitude = {latitude}"
    )
```

### **3.11. Organização das informações**

**Objetivo:** organizar os resultados em uma lista de textos.

```
linhas = []

linhas.append("DESCRIÇÃO TÉCNICA DOS POLÍGONOS")
linhas.append("UNIFICAÇÃO DE IMÓVEIS URBANOS")
linhas.append("=" * 65)

linhas.append("Sistema de Referência: SIRGAS 2000")
linhas.append("Código EPSG: 4674")
linhas.append("Coordenadas: Longitude e Latitude")
```

### **3.12. Exportação do arquivo TXT**

**Objetivo:** permitir que o usuário escolha onde salvar o arquivo.

```
caminho, _ = QFileDialog.getSaveFileName(
    None,
    "Salvar descrição dos polígonos",
    "descricao_poligonos_unificacao.txt",
    "Arquivo TXT (*.txt)"
)

if caminho:

    with open(caminho, "w", encoding="utf-8") as arquivo:

        arquivo.write("\n".join(linhas))

    QMessageBox.information(
        None,
        "Processamento concluído",
        "Arquivo exportado com sucesso!"
    )
```

---

## **4\. Código completo consolidado**

O bloco abaixo reúne as principais operações em um único script executável no Console Python do QGIS.

```
# ============================================================
# GERADOR DE DESCRIÇÃO DE POLÍGONOS
# UNIFICAÇÃO DE IMÓVEIS URBANOS
# PYQGIS
# ============================================================

from qgis.core import (
    QgsProject,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsDistanceArea,
    QgsWkbTypes
)

from qgis.PyQt.QtWidgets import (
    QFileDialog,
    QMessageBox
)

# ============================================================
# 1. IDENTIFICAÇÃO DA CAMADA
# ============================================================

layer = iface.activeLayer()

if layer is None:
    raise Exception("Selecione uma camada vetorial.")

if layer.geometryType() != QgsWkbTypes.PolygonGeometry:
    raise Exception("A camada selecionada não é poligonal.")

# ============================================================
# 2. SISTEMA DE REFERÊNCIA
# ============================================================

crs_saida = QgsCoordinateReferenceSystem("EPSG:4674")

if not layer.crs().isValid():
    raise Exception("CRS de origem inválido.")

transform = QgsCoordinateTransform(
    layer.crs(),
    crs_saida,
    QgsProject.instance()
)

# ============================================================
# 3. CONFIGURAÇÃO GEODÉSICA
# ============================================================

distance = QgsDistanceArea()

distance.setSourceCrs(
    crs_saida,
    QgsProject.instance().transformContext()
)

distance.setEllipsoid("GRS80")

# ============================================================
# 4. FUNÇÕES AUXILIARES
# ============================================================

def formatar_coord(valor):
    return f"{valor:.10f}"


def obter_aneis(geom):

    if geom.isMultipart():
        return geom.asMultiPolygon()

    return [geom.asPolygon()]


# ============================================================
# 5. SELEÇÃO DAS FEIÇÕES
# ============================================================

features = (
    layer.selectedFeatures()
    if layer.selectedFeatureCount() > 0
    else layer.getFeatures()
)

features = list(features)

if not features:
    raise Exception("Nenhum polígono encontrado.")

# ============================================================
# 6. INICIALIZAÇÃO DO RELATÓRIO
# ============================================================

linhas = []

linhas.append("DESCRIÇÃO TÉCNICA DOS POLÍGONOS")
linhas.append("UNIFICAÇÃO DE IMÓVEIS URBANOS")
linhas.append("=" * 65)

linhas.append("Sistema de Referência: SIRGAS 2000")
linhas.append("Código EPSG: 4674")
linhas.append("Coordenadas: Longitude e Latitude")
linhas.append("Unidade: Graus decimais")

# ============================================================
# 7. PROCESSAMENTO DOS POLÍGONOS
# ============================================================

for indice, feature in enumerate(features, start=1):

    geom = feature.geometry()

    if geom.isNull() or geom.isEmpty():
        continue

    linhas.append("")
    linhas.append("=" * 65)
    linhas.append(f"POLÍGONO {indice}")
    linhas.append(f"ID DA FEIÇÃO: {feature.id()}")

    if not geom.isGeosValid():
        linhas.append(
            "AVISO: Geometria inválida. "
            "Requer correção antes do uso técnico."
        )

    # Criar cópia da geometria
    geom_saida = geom.clone()

    # Transformar coordenadas
    geom_saida.transform(transform)

    # Calcular área e perímetro
    area = distance.measureArea(geom_saida)
    perimetro = distance.measurePerimeter(geom_saida)

    linhas.append(f"ÁREA: {area:.3f} m²")
    linhas.append(f"PERÍMETRO: {perimetro:.3f} m")

    # Identificar partes e anéis
    partes = obter_aneis(geom_saida)

    for parte_idx, polygon in enumerate(partes, start=1):

        for anel_idx, anel in enumerate(polygon):

            if anel_idx == 0:
                tipo = "CONTORNO EXTERNO"
            else:
                tipo = f"ANEL INTERNO {anel_idx}"

            linhas.append("")
            linhas.append(
                f"{tipo} - PARTE {parte_idx}"
            )

            for vertice_idx, ponto in enumerate(anel):

                longitude = formatar_coord(ponto.x())
                latitude = formatar_coord(ponto.y())

                linhas.append(
                    f"V{vertice_idx + 1}: "
                    f"Longitude = {longitude}; "
                    f"Latitude = {latitude}"
                )

# ============================================================
# 8. EXPORTAÇÃO
# ============================================================

caminho, _ = QFileDialog.getSaveFileName(
    None,
    "Salvar descrição dos polígonos",
    "descricao_poligonos_unificacao.txt",
    "Arquivo TXT (*.txt)"
)

if caminho:

    with open(
        caminho,
        "w",
        encoding="utf-8"
    ) as arquivo:

        arquivo.write("\n".join(linhas))

    QMessageBox.information(
        None,
        "Processamento concluído",
        f"Arquivo gerado com sucesso:\n{caminho}"
    )

else:

    print("Exportação cancelada pelo usuário.")
```

---

## **5\. Testes de validação**

### **5.1. Verificação da camada**

```
print("Nome:", layer.name())
print("CRS:", layer.crs().authid())
print("Quantidade de feições:", layer.featureCount())
```

### **5.2. Verificação da transformação**

```
print("CRS de origem:", layer.crs().authid())
print("CRS de saída:", crs_saida.authid())
```

### **5.3. Verificação topológica**

```
for feature in layer.getFeatures():

    geom = feature.geometry()

    print(
        f"Feição {feature.id()}: "
        f"Geometria válida = {geom.isGeosValid()}"
    )
```

### **5.4. Verificação dos cálculos**

```
print("Área (m²):", area)
print("Perímetro (m):", perimetro)
```

---

## **6\. Estrutura de saída esperada**

```
DESCRIÇÃO TÉCNICA DOS POLÍGONOS
UNIFICAÇÃO DE IMÓVEIS URBANOS

Sistema de Referência: SIRGAS 2000
Código EPSG: 4674

POLÍGONO 1

ID DA FEIÇÃO: 1
ÁREA: 1250.000 m²
PERÍMETRO: 150.000 m

CONTORNO EXTERNO - PARTE 1

V1: Longitude = -34.9876543210; Latitude = -8.1234567890
V2: Longitude = -34.9876543215; Latitude = -8.1234567895
V3: Longitude = -34.9876543220; Latitude = -8.1234567900
```

*Os valores apresentados são ilustrativos.*

---

## **7\. Controle de qualidade e limitações**

| Funcionalidade | Situação |
| ----- | ----- |
| Leitura de polígonos | Implementada |
| Leitura de MultiPolygon | Implementada |
| Transformação de coordenadas | Implementada |
| Cálculo de área e perímetro | Implementado |
| Extração de vértices | Implementada |
| Identificação de anéis | Implementada |
| Dissolução de polígonos | Pendente |
| Cálculo de azimutes | Pendente |
| Distâncias por segmento | Pendente |
| Identificação de confrontantes | Pendente |
| Memorial DOCX | Pendente |
| Validação topológica completa | Pendente |

---

## **8\. Próximas etapas do desenvolvimento**

```
# FUNCIONALIDADES FUTURAS

# 1. DISSOLUÇÃO DOS POLÍGONOS
# 2. VALIDAÇÃO TOPOLÓGICA
# 3. ORDENAÇÃO DOS VÉRTICES
# 4. CÁLCULO DE AZIMUTES
# 5. CÁLCULO DE DISTÂNCIAS
# 6. IDENTIFICAÇÃO DOS CONFRONTANTES
# 7. GERAÇÃO DO MEMORIAL DESCRITIVO
# 8. EXPORTAÇÃO DOCX E PDF
# 9. CRIAÇÃO DE INTERFACE GRÁFICA
# 10. RELATÓRIO DE CONTROLE DE QUALIDADE
```

## **9\. Referências técnicas**

* Lei nº 6.015/1973 – Lei de Registros Públicos.  
* Lei nº 10.267/2001.  
* ABNT NBR 17047:2022.  
* Documentação oficial do QGIS e PyQGIS.  
* Documentação da biblioteca PROJ.  
* Especificações do sistema de referência SIRGAS 2000\.

## **10\. Considerações finais**

O Gerador de Descrição de Polígonos constitui uma ferramenta de apoio à Engenharia Cartográfica e Agrimensura, permitindo automatizar operações de extração de coordenadas, cálculos geométricos e organização de informações para processos de unificação imobiliária.

A utilização em procedimentos registrais depende da validação dos resultados e da compatibilidade com as peças técnicas e exigências da serventia competente.

