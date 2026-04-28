# Key Performance Indicators (KPIs)

This document defines the KPIs used to measure the performance and trustworthiness of the AI component for the Welding Quality Detection Challenge. KPIs are organized around the 6 trust attributes defined in the Confiance.ai evaluation framework.

## 1. Data Quality KPI

- **Description**: Evaluate the quality and representativeness of the dataset before training begins, ensuring sufficient coverage of the operational design domain.
- **Metrics**:
  - **Class distribution**: ratio OK/KO per seam type (C20/C33/C102). Detect severe imbalance or missing defect samples for a specific seam.
  - **Annotation consistency**: agreement rate between operator and quality controller annotations. Low agreement signals labeling noise that could harm training.
  - **ODD coverage**: diversity of capture conditions represented in the dataset (lighting variations, blur levels, rotation angles). Gaps in coverage indicate blind spots.
- **Objective**: All seam types represented with both OK and KO samples, annotation consistency > threshold (TBD), ODD conditions sufficiently covered.
- **Phase**: Construction.

## 2. Training Convergence KPI

- **Description**: Monitor the progression and stability of model training to detect issues early (divergence, overfitting, instability).
- **Metrics**:
  - **Loss evolution**: training loss should decrease smoothly without oscillation.
  - **F1-score on validation set per epoch**: tracks model improvement over time.
  - **Train/val gap**: difference between training F1 and validation F1. A growing gap signals overfitting (model memorizes training data instead of learning generalizable features).
- **Objective**: Smooth convergence, F1 val plateau triggers early stopping, train/val gap < threshold (TBD).
- **Phase**: Training.

## 3. Performance KPI

- **Description**: Evaluate the component's ability to correctly classify welds, prioritizing defect detection (minimizing false negatives is the top priority — a defective weld classified as OK is a safety risk).
- **Metrics**:
  - **Recall NOK**: proportion of actual defects correctly detected. Recall = TP / (TP + FN). A recall of 0.95 means the model misses 5% of defects.
  - **Precision NOK**: when the model predicts NOK, is it correct? Precision = TP / (TP + FP). Low precision means too many false alarms.
  - **F1-score**: harmonic mean of precision and recall (global + per class + per seam type). A single indicator balancing both.
  - **Confusion matrix**: cross-tabulation of predictions vs true classes (OK/NOK/Unknown), broken down by seam type (C20/C33/C102) to identify seam-specific weaknesses.
  - **Operational cost matrix**: asymmetric cost weighting — a false negative (NOK classified as OK) costs significantly more than a false positive (OK classified as NOK), especially on critical welds.
  - **Inference latency**: time from image input to prediction output. Must remain under 1/12s (~83ms).
- **Objective**: Recall NOK > threshold (TBD), F1 NOK > threshold (TBD), inference latency < 1/12s.
- **Phase**: Evaluation, Operation.

## 4. Uncertainty KPI

- **Description**: Evaluate the relevance and calibration of the component's confidence estimates, ensuring alignment between expressed uncertainty and actual error risk. A model that displays 90% confidence should be correct ~90% of the time.
- **Metrics**:
  - **ECE (Expected Calibration Error)**: measures the gap between expressed confidence and actual accuracy, grouped by confidence bins. An ECE of 0.05 means confidence is off by 5% on average.
  - **Brier Score**: global measure of predicted probability quality, combining calibration and discrimination. Ranges from 0 (perfect) to 1 (worst).
  - **Unknown rate**: percentage of predictions routed to Unknown. Must be within a target range — too high means the model is useless, too low means it may miss doubtful cases.
- **Objective**: ECE < threshold (TBD), Unknown rate within target range (e.g. 2-10%).
- **Phase**: Evaluation, Operation.

## 5. Robustness KPI

- **Description**: Evaluate the component's ability to produce stable predictions under ODD-compliant perturbations (blur, lighting, rotation ±10°, translation ~20px).
- **Metrics**:
  - **ΔF1-score under perturbation**: difference in F1-score between clean images and perturbed images, per perturbation type. Smaller delta = more robust.
  - **AUC of precision per perturbation level**: F1-score curve as perturbation intensity increases. Area under this curve gives a global robustness score. A robust model maintains a flat curve.
  - **Unknown switch rate under perturbation**: does the Unknown rate increase reasonably under perturbation? If it explodes → model too sensitive. If it doesn't move → model may not detect it's struggling.
- **Objective**: ΔF1 < acceptable threshold (e.g. < 5% degradation), stable behavior within ODD limits.
- **Phase**: Evaluation.

## 6. OOD Monitoring KPI

- **Description**: Evaluate the component's ability to detect out-of-distribution inputs (dirty camera, saturated image, unknown object, extreme blur) and flag them as Unknown rather than producing unreliable predictions.
- **Metrics**:
  - **AUROC OOD**: global ability to separate in-distribution from OOD images. Ranges from 0.5 (random) to 1.0 (perfect separation).
  - **OOD false negative rate**: OOD image not detected → passes through the model with potentially meaningless prediction. Most dangerous case, to be minimized.
  - **OOD false positive rate**: normal image flagged as OOD → unnecessary Unknown, overloads operator with manual checks.
- **Objective**: AUROC OOD > threshold (e.g. > 0.95), OOD false negative rate minimized.
- **Phase**: Evaluation, Operation.

## 7. Generalization KPI

- **Description**: Evaluate the component's ability to classify unseen weld seam types (C19, C34, C101) that share visual features with training data, without retraining.
- **Metrics**:
  - **F1-score on unseen seams**: same metric as performance KPI, computed on unseen seam types.
  - **ΔF1 seen vs unseen**: performance gap between training seam types and unseen ones. Small delta = good generalization.
  - **Confusion matrix on unseen seams**: to check whether error patterns on unseen seams differ from seen seams.
  - **Unknown rate on unseen seams**: is the model appropriately less confident on new seam types? A slightly higher Unknown rate would indicate healthy caution.
- **Objective**: Acceptable performance on unseen seam types without retraining, ΔF1 < threshold.
- **Phase**: Evaluation.

## 8. Data Drift KPI

- **Description**: Evaluate the component's ability to handle progressive hardware degradation: maintain performance under mild drift, and trigger OOD detection under severe drift.
- **Metrics**:
  - **F1-score per degradation level**: performance at each intensity level (mild → moderate → severe Gaussian noise, dead pixels). Shows at which point the model breaks down.
  - **OOD trigger point**: at which degradation level does the OOD detector start firing? Too early → too sensitive. Too late → model predicts poorly without signaling it.
  - **AUROC OOD under severe drift**: does OOD detection work specifically on hardware-degraded images?
  - **False negative rate under drift**: degraded image neither detected as OOD nor correctly classified — model says OK on an unusable image. Most dangerous case.
- **Objective**: Stable performance under mild drift, reliable OOD detection under severe drift.
- **Phase**: Evaluation, Operation.

## KPI Mapping to Lifecycle Phases

| KPI | Construction | Training | Evaluation | Operation |
|-----|:---:|:---:|:---:|:---:|
| Data Quality | X | | | |
| Training Convergence | | X | | |
| Performance | | | X | X |
| Uncertainty | | | X | X |
| Robustness | | | X | |
| OOD Monitoring | | | X | X |
| Generalization | | | X | |
| Data Drift | | | X | X |

## Aggregation Method

KPIs are aggregated using a two-level approach:
1. **Pass/fail gate**: each KPI must meet its minimum threshold — any failure blocks deployment
2. **Weighted score**: KPIs are normalized (0-1) and combined with criticality-based weights (e.g. Performance weight 3, OOD weight 2, Robustness weight 2, Uncertainty weight 1, Generalization weight 1, Drift weight 1) for cross-version comparison and progress tracking

Visual synthesis: radar chart of the 6 trust attributes for immediate overview.
