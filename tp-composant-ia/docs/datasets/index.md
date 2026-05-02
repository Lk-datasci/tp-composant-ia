# Datasets Definition

This document describes the datasets used for training, validating, calibrating, and evaluating the welding quality detection AI component. Each dataset is defined by its constitution method, volume, augmentation strategy, and intended usage within the component lifecycle.

## 1. Data Split Strategy

The full Renault welding dataset (22,753 images, 3 seam types: C20/C33/C102, 98% OK / 2% KO) is divided using **stratified splitting**, preserving the distribution of seam types (22% C20 / 39% C33 / 39% C102) and the OK/KO ratio within each subset.

Stratified splitting ensures that each subset contains a representative proportion of all classes and seam types. Without stratification, random sampling could produce subsets with missing or under-represented categories, compromising training or evaluation quality.

The split is performed on the combination (seam_type, label) to guarantee that each subset contains KO samples for every seam type.

| Subset | Volume | Purpose |
|--------|--------|---------|
| Training | ~60% (~13,650 images) | Model learning |
| Validation | ~10% (~2,275 images) | Hyperparameter tuning + early stopping |
| Calibration | ~10% (~2,275 images) | UQ/OOD threshold calibration |
| Evaluation | ~20% (~4,550 images) | Final assessment before deployment |

## 2. Core Datasets

### 2.1 Training Dataset

- **Method**: stratified split from the Renault dataset, preserving seam type and OK/KO distribution. KO class rebalancing through targeted data augmentation to compensate the 98/2 imbalance.
- **Volume**: ~60% of the data (~13,650 images before augmentation)
- **Data augmentation**: transformations applied randomly on-the-fly during training (each image may be presented clean or with one or more transformations drawn at random, with a probability of 0.3-0.5 per transformation type):
  - Geometric: rotation ±10°, translation ~20px (within ODD limits)
  - Colorimetric: brightness and contrast variations
  - Noise: light Gaussian blur, simulated sensor noise
- **KO rebalancing**: oversampling of KO images (duplicate + augmented variants) to reach a less extreme ratio (target to be defined experimentally, e.g. 80/20 or 70/30 rather than 50/50 to stay closer to operational reality)
- **Usage**: joint training of backbone CNNs (one per seam type) and predictor. Exposure to ODD-compliant variations for robustness.

### 2.2 Validation Dataset

- **Method**: stratified split, same distribution as training set, data fully disjoint from training.
- **Volume**: ~10% of the data (~2,275 images)
- **Augmentation**: none — evaluation on clean data for reliable progress tracking during training.
- **Usage**: early stopping (halt training when F1 NOK on validation set plateaus for N consecutive epochs), hyperparameter tuning, overfitting monitoring (train/val gap tracking).

### 2.3 Calibration Dataset

- **Method**: stratified split, data never seen during training, distribution close to operational reality (98/2 OK/KO ratio preserved — not rebalanced).
- **Volume**: ~10% of the data (~2,275 images)
- **Augmentation**: none — calibration on real distribution to ensure representative threshold setting.
- **Usage**: post-training calibration of:
  - UQ thresholds (at what uncertainty level does the system switch to Unknown?)
  - OOD detection boundaries in latent space (what is the "normal" distribution of known data?)
  - Monitoring baselines (expected Unknown rate, expected confidence distribution per seam type)
- **Important**: the calibration set must preserve the real 98/2 distribution. Using a rebalanced set would produce biased thresholds — the model would be calibrated for a world where defects are common, not for the real production line where they are rare.

### 2.4 Standard Evaluation Dataset

- **Method**: stratified split, representative sample never seen during training or calibration, fully disjoint from all other subsets.
- **Volume**: ~20% of the data (~4,550 images)
- **Augmentation**: none.
- **Usage**: final assessment before deployment — computation of:
  - Performance metrics (F1-score, Recall NOK, Precision NOK, confusion matrix, operational cost matrix, inference latency)
  - Uncertainty metrics (ECE, Brier score, Unknown rate)
  - Per-CNN performance comparison
  - Routing accuracy

## 3. Specialized Evaluation Datasets

These datasets are generated from a **selected subset of high-quality, representative real images** (typically a few hundred source images from the evaluation set), not from the full dataset.

### 3.1 Robustness Dataset

- **Method**: generated from ~500 source images of good quality selected from the standard evaluation set. Controlled perturbations applied at multiple intensity levels per perturbation type. Each source image produces several perturbed variants.
- **Perturbation types**:
  - Blur: Gaussian blur at increasing kernel sizes
  - Brightness: under-exposure and over-exposure at increasing intensity
  - Rotation: ±10° at incremental angles (within ODD limits)
  - Translation: shifts up to ~20px in each direction
- **Volume**: ~500 source images × 4 perturbation types × 4-5 intensity levels = several thousand perturbed images
- **Usage**: robustness evaluation — ΔF1-score per perturbation type, AUC of precision per perturbation level, Unknown switch rate under perturbation. Validates ODD compliance.

### 3.2 OOD Dataset

- **Method**: two complementary approaches:
  - **Real OOD**: selection through a discovery protocol of naturally occurring anomalous images in the existing dataset (extreme blur, occlusions, abnormal lighting, camera artifacts)
  - **Synthetic OOD**: generated from ~200 good-quality source images by applying strong perturbations beyond ODD limits (artificial coloration, extreme brightness/contrast saturation, heavy blur, simulated camera obstruction)
- **Volume**: a few hundred images, mix of real and synthetic OOD
- **Usage**: OOD detection evaluation — AUROC OOD, OOD false negative rate (priority: dangerous cases), OOD false positive rate. Tests the OOD detector's ability to flag inputs that should not be classified.

### 3.3 Generalization Dataset

- **Method**: selection of images from unseen weld seam types (C19, C34, C101), chosen based on visual proximity with training seam types. Ideally provided by the Renault engineering team or sourced from an extended dataset.
- **Volume**: a few hundred images per unseen seam type
- **Augmentation**: none — evaluation on real unseen data.
- **Usage**: generalization evaluation — F1-score on unseen seams, ΔF1 seen vs unseen, confusion matrix on unseen seams, Unknown rate on unseen seams. Tests whether the component can handle similar but unknown weld types without retraining.

### 3.4 Data Drift Dataset

- **Method**: generated from ~500 good-quality source images by applying progressive degradations simulating hardware aging. Multiple intensity levels from mild to severe.
- **Degradation types**:
  - Gaussian noise at increasing intensity
  - Simulated dead pixels (random pixel dropout at increasing rates)
  - Progressive image quality degradation (combined blur + noise + contrast loss)
- **Volume**: ~500 source images × 4-5 degradation levels = a few thousand degraded images
- **Usage**: data drift evaluation — F1-score per degradation level (at which point does the model break down?), OOD trigger point (at which degradation level does OOD detection activate?), AUROC OOD under severe drift, false negative rate under drift. Tests dual behavior: robustness under mild drift + OOD detection under severe drift.

## 4. Dataset Metadata

Each sample across all datasets is associated with the following metadata:

| Field | Description |
|-------|-------------|
| `weld_id` | Unique identifier for the weld |
| `seam_type` | Weld seam type (C20 / C33 / C102, or C19 / C34 / C101 for generalization) |
| `label` | Ground truth class (OK / KO) |
| `annotation_source` | Origin of the label (operator / quality controller / both) |
| `is_augmented` | Boolean — original image or synthetically generated |
| `augmentation_type` | Type of augmentation applied (if augmented): blur, brightness, rotation, translation, noise, coloration, dead_pixels |
| `augmentation_intensity` | Intensity level of the augmentation (if augmented) |
| `original_weld_id` | Reference to source image (if augmented) |
| `blur_level` | Measured blur level of the image |
| `flash_intensity` | Flash intensity at capture time |
| `criticality` | Criticality level of the weld position |
| `dataset_subset` | Which subset this sample belongs to (training / validation / calibration / evaluation / robustness / ood / generalization / drift) |

## 5. Dataset Constitution Methods

Summary of techniques used across datasets:

| Technique | Description | Used in |
|-----------|-------------|---------|
| Stratified split | Preserves class and seam type distribution in each subset | Training, Validation, Calibration, Evaluation |
| Data augmentation (on-the-fly) | Random transformations during training for robustness | Training |
| KO oversampling | Duplicate + augment KO images to rebalance classes | Training |
| Controlled perturbation | Apply perturbations at known intensity levels for evaluation | Robustness, Data Drift |
| Strong perturbation (beyond ODD) | Generate synthetic OOD images with extreme alterations | OOD |
| Discovery protocol | Manual or semi-automatic search for real anomalous images | OOD |
| Proximity-based selection | Select unseen seam types similar to training data | Generalization |

## 6. Dataset Mapping to Lifecycle Phases

| Dataset | Construction | Training | Evaluation | Operation |
|---------|:---:|:---:|:---:|:---:|
| Training | | X | | |
| Validation | | X | | |
| Calibration | | X | | |
| Standard Evaluation | | | X | |
| Robustness | | | X | |
| OOD | | | X | |
| Generalization | | | X | |
| Data Drift | | | X | |
