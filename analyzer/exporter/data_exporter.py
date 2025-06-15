import string
from typing import List
from analyzer.exporter.export_strategy import ExportStrategy


class DataExporter:
    def __init__(self, export_strategy: ExportStrategy):
        self.export_strategy = export_strategy

    def export(self, data: List, output_path: string):
        return self.export_strategy.export(data)

    def set_strategy(self, strategy:ExportStrategy):
        self.export_strategy = strategy