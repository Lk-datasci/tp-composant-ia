from abc import ABC, abstractmethod
from typing import Any, Dict
import random

class KPIInterface(ABC):
    """
    Interface for KPI calculation.
    """

    @abstractmethod
    def calculate_metric(self, data: Any, predictions: Any) -> Dict[str, float]:
        """
        Calculate a specific metric (e.g., F1-score, robustness).
        """
        pass

    @abstractmethod
    def get_kpi_metadata(self) -> Dict[str, Any]:
        """
        Return metadata associated with the KPI.
        """
        pass

class RobustnessKPI(KPIInterface):
    """
    KPI implementation for robustness to flash.
    """

    def calculate_metric(self, data: Any, predictions: Any) -> Dict[str, float]:
        # Simulate calculation
        return {"robustness_score": random.uniform(0.9, 1.0)}

    def get_kpi_metadata(self) -> Dict[str, Any]:
        return {
            "parameter": "flash_intensity",
            "dimension": "percentage"
        }
