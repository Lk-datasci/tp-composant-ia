from abc import ABC, abstractmethod
from typing import Any, List, Dict
import random

class DatasetInterface(ABC):
    """
    Interface for dataset generation and selection.
    """

    @abstractmethod
    def generate_sample(self, params: Dict[str, Any]) -> Any:
        """
        Generate or alter a single data sample based on parameters.
        """
        pass

    @abstractmethod
    def select_samples(self, criteria: Dict[str, Any]) -> List[Any]:
        """
        Filter samples based on metadata criteria.
        """
        pass

class WeldingDataset(DatasetInterface):
    """
    Implementation for the Welding Challenge dataset.
    """

    def generate_sample(self, params: Dict[str, Any]) -> Any:
        # Simulate flash effect if requested
        flash = params.get("flash_effect", False)
        return {
            "image_data": "...",
            "metadata": {
                "flash_applied": flash,
                "defect": random.choice(["POROSITY", "NONE"])
            }
        }

    def select_samples(self, criteria: Dict[str, Any]) -> List[Any]:
        # Simulate filtering by material or defect
        return [{"sample_id": i} for i in range(5)]
