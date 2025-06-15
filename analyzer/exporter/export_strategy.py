
from abc import ABC, abstractmethod


class ExportStrategy(ABC):
    """
    The ExportStrategy provides a common interface for all export strategies used to export data
    """
    @abstractmethod
    def export(self, data):
        pass