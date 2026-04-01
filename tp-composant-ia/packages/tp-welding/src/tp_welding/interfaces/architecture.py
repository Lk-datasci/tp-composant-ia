from abc import ABC, abstractmethod
from typing import Any, Dict
import random

class AIComponentInterface(ABC):
    """
    Main interface for the AI Component.
    """

    @abstractmethod
    def preprocess(self, raw_data: Any) -> Any:
        """
        Pre-process raw data (images, sensors).
        """
        pass

    @abstractmethod
    def predict(self, processed_data: Any) -> Dict[str, Any]:
        """
        Run inference on processed data.
        """
        pass

    @abstractmethod
    def postprocess(self, inference_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Post-process inference results.
        """
        pass

class WeldingQualityComponent(AIComponentInterface):
    """
    Black-box implementation of the Welding Quality Detection Component.
    """

    def preprocess(self, raw_data: Any) -> Any:
        # Simulate normalization
        return {"processed": True}

    def predict(self, processed_data: Any) -> Dict[str, Any]:
        # Black-box that returns random result
        return {
            "defect_type": random.choice(["NONE", "POROSITY", "SPLASH"]),
            "confidence": random.uniform(0.5, 1.0)
        }

    def postprocess(self, inference_result: Dict[str, Any]) -> Dict[str, Any]:
        # Filter and format
        return {
            "status": "OK" if inference_result["defect_type"] == "NONE" else "DEFECT_DETECTED",
            "details": inference_result
        }
