from qgis.core import (
    QgsProject,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsDistanceArea,
    QgsWkbTypes
)
from qgis.PyQt.QtWidgets import QFileDialog, QMessageBox
from qgis.PyQt.QtCore import QLocale

# =====================================================
# CONFIGURAÇÕES
# =====================================================

layer = iface.activeLayer()

if layer is None:
    raise Exception("Selecione uma camada vetorial.")

if layer.geometryType() != QgsWkbTypes.PolygonGeometry:
    raise Exception("A camada selecionada não é poligonal.")

# Sistema de referência geográfico
crs_saida = QgsCoordinateReferenceSystem("EPSG:4674")

# Transformação de coordenadas
transform = QgsCoordinateTransform(
    layer.crs(),
    crs_saida,
    QgsProject.instance()
)

# Cálculo geodésico
distance = QgsDistanceArea()
distance.setSourceCrs(
    crs_saida,
    QgsProject.instance().transformContext()
)
distance.setEllipsoid("GRS80")

# =====================================================
# FUNÇÕES
# =====================================================

def formatar_coord(valor):
    return f"{valor:.10f}"

def obter_aneis(geom):
    """Retorna os anéis externos e internos da geometria."""
    if geom.isMultipart():
        return geom.asMultiPolygon()
    return [geom.asPolygon()]

# =====================================================
# PROCESSAMENTO
# =====================================================

features = (
    layer.selectedFeatures()
    if layer.selectedFeatureCount() > 0
    else layer.getFeatures()
)

features = list(features)

if not features:
    raise Exception("Nenhum polígono encontrado.")

linhas = []

linhas.append("DESCRIÇÃO TÉCNICA DOS POLÍGONOS")
linhas.append("UNIFICAÇÃO DE IMÓVEIS URBANOS")
linhas.append("=" * 65)
linhas.append("Sistema de Referência: SIRGAS 2000")
linhas.append("Código EPSG: 4674")
linhas.append("Coordenadas: Longitude e Latitude")
linhas.append("Unidade angular: Graus decimais")
linhas.append("")

for indice, feature in enumerate(features, start=1):

    geom = feature.geometry()

    if geom.isNull() or geom.isEmpty():
        continue

    if not geom.isGeosValid():
        linhas.append(
            f"AVISO: Feição {feature.id()} possui geometria inválida."
        )

    geom_saida = QgsGeometry(geom)
    geom_saida.transform(transform)

    area = distance.measureArea(geom_saida)
    perimetro = distance.measurePerimeter(geom_saida)

    linhas.append("-" * 65)
    linhas.append(f"POLÍGONO {indice}")
    linhas.append(f"ID da feição: {feature.id()}")
    linhas.append(f"Área: {area:.3f} m²")
    linhas.append(f"Perímetro: {perimetro:.3f} m")

    # Identificação dos anéis
    partes = obter_aneis(geom_saida)

    for parte_idx, polygon in enumerate(partes, start=1):

        for anel_idx, anel in enumerate(polygon):

            if anel_idx == 0:
                tipo = "CONTORNO EXTERNO"
            else:
                tipo = f"ANEL INTERNO {anel_idx}"

            linhas.append("")
            linhas.append(f"{tipo} - PARTE {parte_idx}")

            for vertice_idx, ponto in enumerate(anel):

                longitude = formatar_coord(ponto.x())
                latitude = formatar_coord(ponto.y())

                linhas.append(
                    f"V{vertice_idx + 1}: "
                    f"Longitude = {longitude}; "
                    f"Latitude = {latitude}"
                )

    linhas.append("")

# =====================================================
# EXPORTAÇÃO TXT
# =====================================================

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
        f"Descrição gerada com sucesso!\n\n{caminho}"
    )
