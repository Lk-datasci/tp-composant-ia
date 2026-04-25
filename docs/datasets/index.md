# Datasets Definition

This document describes the datasets used for training, validating, and testing the welding quality detection component.

## 1. Dataset Constitution Methods

### Data Augmentation for Welding Defects

To improve model robustness, the following augmentations are planned:

* **Visual Effects**: Simulated camera flash (overexposure), motion blur, and sensor noise.
* **Geometric**: Random cropping of weld seams, rotations, and perspective shifts.
* **Contextual**: Inserting synthetic defects (e.g., porosity) into "clean" weld images.

### Filtering and Selection
- **Negative Mining**: Selecting samples where no water is present near the weld (specific use case).
- **Metadata-based Filtering**: Extracting samples by material type (e.g., Aluminum vs Steel).

## 2. Metadata Identification
Each sample in the dataset is associated with the following metadata:
- `weld_id`: Unique identifier for the weld seam.
- `material`: Type of material being welded.
- `defect_type`: Ground truth label (NONE, POROSITY, SPLASH).
- `flash_intensity`: Localisation and intensity of simulated camera flash.
- `sensor_sync_offset`: Time offset between video and sensor logs.

## 3. Usage Description
| Dataset | Purpose | Sample Count (Planned) |
|---------|---------|------------------------|
| `train_base` | Initial model training | 5000 |
| `train_augmented` | Robustness training (with flash/noise) | 10000 |
| `val_standard` | Hyperparameter tuning | 1000 |
| `test_edge_cases`| Final validation on flash/occlusion cases | 500 |

## 4. Dataset Interface (Python)
The following code defines how datasets are accessed and manipulated.
