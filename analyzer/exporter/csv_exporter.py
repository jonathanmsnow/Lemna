import string
from typing import List
from analyzer.exporter.export_strategy import ExportStrategy
import csv

class CSVExporter(ExportStrategy):
    def export(self, data: List, file_path: string):
        
        return super().export(data)