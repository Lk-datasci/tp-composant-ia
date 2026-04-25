# Key Performance Indicators (KPIs)

This document defines the KPIs used to measure the performance and robustness of the AI component.

## 1. Robustness to Camera Flash
- **Description**: Measure the model's ability to maintain detection accuracy despite simulated or real camera flash overexposure.
- **Metadata**: `flash_intensity`, `flash_location`, `weld_type`.
- **Objective**: Ensure a drop in F1-score of less than 5% when flash is present.
- **Phase**: Evaluation, Operation.

## 2. Detection Confidence Score
- **Description**: Reliability of the model's prediction.
- **Metadata**: `probability_map`, `threshold`.
- **Objective**: Minimum confidence of 0.85 for reporting a defect.
- **Phase**: Operation.

## 3. Data Diversity KPI
- **Description**: Distribution of material types and defect types in the dataset.
- **Metadata**: `material_count`, `defect_distribution`.
- **Objective**: Ensure at least 20% of samples for each defect type.
- **Phase**: Construction dataset.

## 4. Inference Latency
- **Description**: Average wall-clock time between image arrival and the production of a prediction by the AI component, on the target deployment hardware.
- **Metadata**: `latency_ms`, `hardware_target`, `batch_size`.
- **Objective**: Median latency below 200 ms per image, with 95th percentile below 350 ms, on the operational target hardware.
- **Phase**: Evaluation, Operation.

## 5. Uncertainty Calibration
- **Description**: Alignment between the predicted confidence scores and the empirical accuracy. A well-calibrated model that predicts 0.8 for a class should be correct ~80% of the time.
- **Metadata**: `expected_calibration_error`, `reliability_diagram`, `n_bins`.
- **Objective**: Expected Calibration Error (ECE) below 0.05 on the standard evaluation set.
- **Phase**: Evaluation, Operation.

## 6. Out-of-Distribution Monitoring
- **Description**: Capacity of the component to flag inputs that lie outside the operational design domain (ODD) — both synthetic OOD perturbations and real OOD samples (unseen weld geometries, lighting regimes, sensor noise).
- **Metadata**: `ood_score`, `evaluation_set` (`synthetic` | `real`), `auroc`.
- **Objective**: AUROC ≥ 0.90 for OOD detection on both synthetic (`OOD_Syn`) and real (`OOD_Real`) evaluation sets.
- **Phase**: Evaluation, Operation.

## 7. Generalization
- **Description**: Stability of operational and ML performance metrics across designed evaluation sets that vary one or more nuisance factors (e.g., weld type, illumination, viewpoint) while staying within the ODD.
- **Metadata**: `op_g`, `ml_g`, `scenario_id`, `nuisance_factor`.
- **Objective**: Operational performance (`OP_g`) and ML performance (`ML_g`) degradation below 10% relative to the reference evaluation set.
- **Phase**: Evaluation.

## 8. Data-Drift
- **Description**: Detection of distributional drift between the training data distribution and the live operational data, in order to trigger re-evaluation or retraining of the component.
- **Metadata**: `drift_score`, `op_d`, `ood_d`, `time_window`.
- **Objective**: AUROC ≥ 0.85 for drift detection over a rolling 7-day operational window.
- **Phase**: Operation.

## KPI Mapping to Lifecycle Phases
| KPI Name | Construction | Training | Evaluation | Operation |
|----------|:---:|:---:|:---:|:---:|
| Robustness to Flash | | | X | X |
| Detection Confidence | | | X | X |
| Data Diversity | X | | | |
| Inference Latency | | | X | X |
| Uncertainty Calibration | | | X | X |
| OOD Monitoring | | | X | X |
| Generalization | | | X | |
| Data-Drift | | | | X |

## KPI Interface (Python)

The following code defines how KPIs are calculated and tracked. Each KPI is implemented as a concrete subclass of `KPIInterface`, exposing a `calculate_metric()` method that returns one or more numeric scores and a `get_kpi_metadata()` method that documents the KPI's parameters and units.

```python
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
```

### Usage example

```python
from tp_welding.interfaces.kpi import RobustnessKPI

kpi = RobustnessKPI()

# Toy inputs — replace with real evaluation data and model predictions
data = ["sample_1", "sample_2"]
predictions = ["pred_1", "pred_2"]

score = kpi.calculate_metric(data, predictions)
metadata = kpi.get_kpi_metadata()

print(f"Score: {score}")
print(f"Metadata: {metadata}")
# Score:    {'robustness_score': 0.94}
# Metadata: {'parameter': 'flash_intensity', 'dimension': 'percentage'}
```
