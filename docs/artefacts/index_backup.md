# Artefacts and Validation

This document describes how KPIs are aggregated and presented for final validation by stakeholders.

## 1. Aggregated KPIs for Confidence Demonstration

Artefacts are filtered and aggregated representations of the component's performance.

### Example: Robustness by Weld Type

- **Artefact**: A bar graph showing the F1-score for different welding scenarios (e.g., T-joint vs Butt-joint) in both "Normal" and "Flash" conditions.
- **Aggregation Method**: Grouping test samples by `weld_type` and calculating the mean F1-score.
- **Audience**: Quality Assurance (QA) and Industrial Supervisors.

### Example: Confidence Distribution Map

- **Artefact**: A heatmap showing where the model typically has lower confidence in its predictions.
- **Aggregation Method**: Spatial aggregation of `probability_map` across a test set.
- **Audience**: AI Developers for model refinement.

## 2. Intended Usage and Stakeholders
| Artefact | Stakeholder | Objective |
|----------|-------------|-----------|
| Robustness Report | Safety Officer | Validate component reliability under lighting changes. |
| Defect Heatmap | Maintenance Team | Optimize robot movement to avoid poor-visibility areas. |
| KPI Evolution | Project Manager| Track performance improvement across training iterations. |

## 3. Visual Representation (Mock)

```mermaid
graph TD
    subgraph "KPI Aggregation"
        K1[Robustness]
        K2[Confidence]
        K3[Latency]
    end

    subgraph "Artefacts (Validation)"
        A1[Safety Dashboard]
        A2[Developer Report]
        A3[Management Summary]
    end

    K1 --> A1
    K2 --> A1
    K2 --> A2
    K3 --> A3
```

## 4. Phase Usage

- **Construction Dataset**: Data diversity reports.
- **Training**: Training loss and validation accuracy curves.
- **Evaluation**: Final F1-score report, confusion matrix.
- **Operation**: Real-time confidence monitoring and drift detection.
