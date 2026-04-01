# Key Performance Indicators (KPIs)

*partial automatic generator for structural example, please do not take as good proposal, make you own or even comment identified errors, once TP performed, remove this sentence.*

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

## KPI Mapping to Lifecycle Phases
| KPI Name | Construction | Training | Evaluation | Operation |
|----------|:---:|:---:|:---:|:---:|
| Robustness to Flash | | | X | X |
| Detection Confidence| | | X | X |
| Data Diversity | X | | | |
| Inference Latency | | | X | X |

## KPI Interface (Python)
The following code defines how KPIs are calculated and tracked.
