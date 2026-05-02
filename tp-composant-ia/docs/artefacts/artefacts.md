# Artefacts and Validation

This document describes how KPIs are aggregated and presented to stakeholders for decision-making across the AI component lifecycle.

## 1. Stakeholders and Artefacts

### 1.1 Operator (Production Line - OP 120)

- **Artefact**: Real-time dashboard displayed on the OP 120 screen for each weld image.
- **Content**:
  - Original image + preprocessed image
  - Final classification (OK / NOK / Unknown) with color-coded indicator (green / red / orange)
  - Confidence score (probability of predicted class)
  - Decision rationale when Unknown (high uncertainty / OOD detected / unusable image)
  - Batch summary: OK/NOK/Unknown counts over the last N welds, trend indicator
- **KPIs used**: confidence scores, OOD score, Unknown rate (batch)
- **Aggregation method**: per-image display (no aggregation), batch summary uses simple counts and moving averages
- **Phase**: Operation

### 1.2 Product Owner

- **Artefact**: Trust synthesis report for deployment go/no-go decision.
- **Content**:
  - Radar chart of the 6 trust attributes (performance, uncertainty, robustness, OOD, generalization, data drift) — immediate visual overview
  - Pass/fail status per attribute against defined thresholds
  - Weighted global trust score for cross-version comparison
  - Go/no-go recommendation
- **KPIs used**: all 8 KPIs aggregated into 6 trust attributes
- **Aggregation method**: two-level approach — (1) pass/fail gate: each attribute must meet its minimum threshold, (2) weighted score: normalized KPIs combined with criticality-based weights (Performance ×3, OOD ×2, Robustness ×2, Uncertainty ×1, Generalization ×1, Drift ×1)
- **Phase**: Evaluation

### 1.3 Quality & Safety Officer

- **Artefact**: Compliance and reliability report.
- **Content**:
  - Confusion matrix per seam type (C20/C33/C102) — detailed error analysis
  - Operational cost matrix — false negative impact weighted by weld criticality
  - Robustness report: ΔF1-score per perturbation type with ODD compliance assessment
  - OOD detection reliability: AUROC OOD, false negative OOD rate
  - Data drift behavior: performance stability curve under increasing degradation
- **KPIs used**: Performance, Robustness, OOD Monitoring, Data Drift
- **Aggregation method**: per seam type breakdown, per perturbation type breakdown, criticality weighting for cost matrix
- **Phase**: Evaluation, Operation

### 1.4 Technical Team (Data Scientists / ML Engineers)

- **Artefact**: Detailed technical report for model improvement and production monitoring.
- **Content**:
  - **During development**: training loss curves, F1-score evolution per epoch, train/val gap (overfitting detection), data quality metrics (class distribution, annotation consistency, ODD coverage)
  - **During evaluation**: detailed confusion matrices, ECE and Brier score analysis, per-class and per-seam performance breakdown, robustness curves per perturbation type and intensity level, generalization performance on unseen seams (C19/C34/C101)
  - **During operation**: real-time monitoring dashboard — confidence score distribution, Unknown rate trends, OOD detection frequency, drift indicators, latency tracking, operator feedback log
- **KPIs used**: all 8 KPIs at full granularity
- **Aggregation method**: no aggregation for development/evaluation (raw metrics), moving averages and trend detection for operation monitoring
- **Phase**: Training, Evaluation, Operation

## 2. Artefact Mapping to Lifecycle Phases

| Artefact | Construction | Training | Evaluation | Operation |
|----------|:---:|:---:|:---:|:---:|
| Operator Dashboard | | | | X |
| Trust Synthesis (Product Owner) | | | X | |
| Compliance Report (Quality/Safety) | | | X | X |
| Technical Report (Data/ML Team) | X | X | X | X |

## 3. Visual Representation

```mermaid
graph TD
    subgraph "KPIs"
        DQ[Data Quality]
        TC[Training Convergence]
        PERF[Performance]
        UNC[Uncertainty]
        ROB[Robustness]
        OOD[OOD Monitoring]
        GEN[Generalization]
        DRIFT[Data Drift]
    end

    subgraph "Artefacts"
        OP_DASH[🖥️ Operator Dashboard\nreal-time per-image display]
        PO_REPORT[📊 Trust Synthesis\nradar chart + go/no-go]
        QA_REPORT[📋 Compliance Report\ncost matrix + robustness]
        TECH_REPORT[🔧 Technical Report\nfull metrics + monitoring]
    end

    PERF --> OP_DASH
    UNC --> OP_DASH
    OOD --> OP_DASH

    DQ --> PO_REPORT
    TC --> PO_REPORT
    PERF --> PO_REPORT
    UNC --> PO_REPORT
    ROB --> PO_REPORT
    OOD --> PO_REPORT
    GEN --> PO_REPORT
    DRIFT --> PO_REPORT

    PERF --> QA_REPORT
    ROB --> QA_REPORT
    OOD --> QA_REPORT
    DRIFT --> QA_REPORT

    DQ --> TECH_REPORT
    TC --> TECH_REPORT
    PERF --> TECH_REPORT
    UNC --> TECH_REPORT
    ROB --> TECH_REPORT
    OOD --> TECH_REPORT
    GEN --> TECH_REPORT
    DRIFT --> TECH_REPORT

    style DQ fill:#4A90D9,stroke:#2C5F8A,color:#fff
    style TC fill:#4A90D9,stroke:#2C5F8A,color:#fff
    style PERF fill:#4A90D9,stroke:#2C5F8A,color:#fff
    style UNC fill:#4A90D9,stroke:#2C5F8A,color:#fff
    style ROB fill:#4A90D9,stroke:#2C5F8A,color:#fff
    style OOD fill:#4A90D9,stroke:#2C5F8A,color:#fff
    style GEN fill:#4A90D9,stroke:#2C5F8A,color:#fff
    style DRIFT fill:#4A90D9,stroke:#2C5F8A,color:#fff
    style OP_DASH fill:#8E44AD,stroke:#6C3483,color:#fff
    style PO_REPORT fill:#F39C12,stroke:#D68910,color:#fff
    style QA_REPORT fill:#E74C3C,stroke:#C0392B,color:#fff
    style TECH_REPORT fill:#2ECC71,stroke:#27AE60,color:#fff
```

## 4. Phase Usage Summary

- **Construction**: data quality reports (class distribution, annotation consistency, ODD coverage)
- **Training**: loss curves, F1 evolution, overfitting detection (train/val gap)
- **Evaluation**: trust synthesis (radar chart), compliance report (confusion matrices, cost matrix, robustness curves), go/no-go decision
- **Operation**: real-time operator dashboard, continuous monitoring (confidence trends, Unknown rate, OOD frequency, drift detection), operator feedback integration
