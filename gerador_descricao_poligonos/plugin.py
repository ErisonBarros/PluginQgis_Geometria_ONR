# -*- coding: utf-8 -*-
"""
Gerador de Descrição de Polígonos - Plugin QGIS
Compatibilidade pretendida: QGIS 3.16 ou superior.
"""

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import (
    QAction, QCheckBox, QComboBox, QDialog, QDialogButtonBox,
    QFileDialog, QFormLayout, QHBoxLayout, QLabel, QMessageBox,
    QVBoxLayout
)
from qgis.core import (
    QgsProject,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsDistanceArea,
    QgsGeometry,
    QgsWkbTypes
)
import os


class GeradorDialog(QDialog):
    """Janela principal do plugin."""

    def __init__(self, iface, parent=None):
        super().__init__(parent)
        self.iface = iface
        self.setWindowTitle("Gerador de Descrição de Polígonos")
        self.setMinimumWidth(460)

        layout = QVBoxLayout(self)

        intro = QLabel(
            "Selecione uma camada poligonal e gere um arquivo TXT "
            "com área, perímetro e coordenadas dos vértices."
        )
        intro.setWordWrap(True)
        layout.addWidget(intro)

        form = QFormLayout()
        self.layer_combo = QComboBox()
        self.populate_layers()
        form.addRow("Camada poligonal:", self.layer_combo)

        self.crs_combo = QComboBox()
        self.crs_combo.addItem("SIRGAS 2000 geográfico (EPSG:4674)", "EPSG:4674")
        self.crs_combo.addItem("SIRGAS 2000 / UTM 25S (EPSG:31985)", "EPSG:31985")
        form.addRow("Sistema de saída:", self.crs_combo)

        layout.addLayout(form)

        self.selected_only = QCheckBox("Processar somente feições selecionadas")
        self.selected_only.setChecked(True)
        layout.addWidget(self.selected_only)

        note = QLabel(
            "A camada original não será alterada. Se nenhuma feição estiver "
            "selecionada, o plugin processará todas as feições."
        )
        note.setWordWrap(True)
        note.setStyleSheet("color: #666;")
        layout.addWidget(note)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.button(QDialogButtonBox.Ok).setText("Gerar TXT")
        buttons.button(QDialogButtonBox.Cancel).setText("Cancelar")
        buttons.accepted.connect(self.run_export)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def populate_layers(self):
        self.layer_combo.clear()
        self.layers = []
        for layer in QgsProject.instance().mapLayers().values():
            if layer.isValid() and layer.type() == layer.VectorLayer:
                if layer.geometryType() == QgsWkbTypes.PolygonGeometry:
                    self.layers.append(layer)
                    self.layer_combo.addItem(layer.name(), layer.id())

        if not self.layers:
            self.layer_combo.addItem("Nenhuma camada poligonal disponível", None)

    def run_export(self):
        layer_id = self.layer_combo.currentData()
        layer = QgsProject.instance().mapLayer(layer_id) if layer_id else None

        if layer is None or not layer.isValid():
            QMessageBox.warning(self, "Camada não encontrada",
                                "Adicione uma camada poligonal válida ao projeto.")
            return

        if not layer.crs().isValid():
            QMessageBox.warning(self, "CRS inválido",
                                "A camada não possui sistema de referência válido.")
            return

        use_selection = self.selected_only.isChecked()
        selected = layer.selectedFeatures() if use_selection else []
        features = list(selected) if selected else list(layer.getFeatures())

        if not features:
            QMessageBox.information(self, "Sem feições",
                                    "Não há polígonos para processar.")
            return

        output_authid = self.crs_combo.currentData()
        output_crs = QgsCoordinateReferenceSystem(output_authid)
        if not output_crs.isValid():
            QMessageBox.critical(self, "CRS inválido",
                                 "Não foi possível carregar o CRS de saída.")
            return

        default_name = "descricao_poligonos.txt"
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Salvar descrição dos polígonos",
            os.path.join(os.path.expanduser("~"), default_name),
            "Arquivo de texto (*.txt)"
        )
        if not path:
            return
        if not path.lower().endswith(".txt"):
            path += ".txt"

        try:
            report = self.build_report(layer, features, output_crs)
            with open(path, "w", encoding="utf-8") as output:
                output.write(report)

            QMessageBox.information(
                self,
                "Processamento concluído",
                "Arquivo gerado com sucesso:\n{}".format(path)
            )
            self.accept()

        except Exception as exc:
            QMessageBox.critical(
                self,
                "Erro no processamento",
                "Não foi possível gerar o arquivo.\n\n{}".format(exc)
            )

    def build_report(self, layer, features, output_crs):
        project = QgsProject.instance()
        transform = QgsCoordinateTransform(
            layer.crs(), output_crs, project.transformContext()
        )

        measure = QgsDistanceArea()
        measure.setSourceCrs(output_crs, project.transformContext())
        # GRS80 é o elipsoide associado ao SIRGAS 2000.
        measure.setEllipsoid("GRS80")

        lines = [
            "DESCRIÇÃO GEOMÉTRICA DE POLÍGONOS",
            "Gerador de Descrição de Polígonos - PyQGIS",
            "=" * 72,
            "Camada: {}".format(layer.name()),
            "CRS de origem: {}".format(layer.crs().authid()),
            "CRS de saída: {}".format(output_crs.authid()),
            "Elipsoide de cálculo: GRS80",
            "Quantidade de feições processadas: {}".format(len(features)),
            "",
            "OBSERVAÇÃO: documento auxiliar de extração geométrica. "
            "Não substitui levantamento, planta, memorial técnico ou "
            "qualificação registral.",
            ""
        ]

        for number, feature in enumerate(features, start=1):
            geom = feature.geometry()

            lines.extend([
                "-" * 72,
                "POLÍGONO {}".format(number),
                "ID da feição: {}".format(feature.id())
            ])

            if geom is None or geom.isNull() or geom.isEmpty():
                lines.append("ERRO: geometria vazia.")
                lines.append("")
                continue

            if not geom.isGeosValid():
                lines.append(
                    "ALERTA: geometria inválida segundo a verificação GEOS."
                )

            # QgsGeometry(geom) cria uma cópia; QgsGeometry não usa .clone().
            geom_out = QgsGeometry(geom)
            result = geom_out.transform(transform)

            # Em diferentes versões do QGIS o retorno é um código de resultado.
            # Falhas de transformação também podem ser lançadas como exceção.
            if result != 0:
                lines.append(
                    "ERRO: transformação de coordenadas retornou código {}."
                    .format(result)
                )
                lines.append("")
                continue

            area_m2 = measure.measureArea(geom_out)
            perimeter_m = measure.measurePerimeter(geom_out)

            lines.extend([
                "Área: {:.3f} m²".format(area_m2),
                "Perímetro: {:.3f} m".format(perimeter_m)
            ])

            polygons = (
                geom_out.asMultiPolygon()
                if geom_out.isMultipart()
                else [geom_out.asPolygon()]
            )

            for part_index, polygon in enumerate(polygons, start=1):
                for ring_index, ring in enumerate(polygon):
                    ring_name = (
                        "CONTORNO EXTERNO"
                        if ring_index == 0
                        else "ANEL INTERNO {}".format(ring_index)
                    )
                    lines.append("")
                    lines.append("{} - PARTE {}".format(ring_name, part_index))

                    for vertex_index, point in enumerate(ring, start=1):
                        # Em CRS geográfico: X = longitude; Y = latitude.
                        if output_crs.isGeographic():
                            x_label, y_label = "Longitude", "Latitude"
                        else:
                            x_label, y_label = "Easting", "Northing"

                        lines.append(
                            "V{}: {} = {:.10f}; {} = {:.10f}".format(
                                vertex_index, x_label, point.x(),
                                y_label, point.y()
                            )
                        )

            lines.append("")

        return "\n".join(lines)


class GeradorDescricaoPoligonos:
    """Classe principal carregada pelo gerenciador de plugins do QGIS."""

    def __init__(self, iface):
        self.iface = iface
        self.action = None
        self.toolbar = self.iface.addToolBar(
            "Gerador de Polígonos"
        )
        self.toolbar.setObjectName("GeradorDescricaoPoligonosToolbar")

    def initGui(self):
        icon_path = os.path.join(os.path.dirname(__file__), "icon.svg")
        self.action = QAction(
            QIcon(icon_path),
            "Gerador de Descrição de Polígonos",
            self.iface.mainWindow()
        )
        self.action.setWhatsThis(
            "Extrai vértices, área e perímetro de polígonos."
        )
        self.action.triggered.connect(self.show_dialog)
        self.iface.addPluginToMenu(
            "&Gerador de Polígonos", self.action
        )
        self.toolbar.addAction(self.action)

    def show_dialog(self):
        dialog = GeradorDialog(self.iface, self.iface.mainWindow())
        dialog.exec_()

    def unload(self):
        if self.action:
            self.iface.removePluginMenu(
                "&Gerador de Polígonos", self.action
            )
            self.iface.removeToolBarIcon(self.action)
            self.action = None

        if self.toolbar:
            self.iface.mainWindow().removeToolBar(self.toolbar)
            self.toolbar = None
