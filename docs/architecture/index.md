# AI Component Architecture

This document describes the architecture of the AI component for the Welding Quality Detection Challenge.

blk

## Overview

The AI component is designed to detect welding defects from visual and sensor data. It consists of a pre-processing pipeline, a deep learning model for defect classification/localization, and a post-processing module for quality reporting.

## 1. Operation Architecture (Inference)
The operation phase describes how the component behaves in a real-time environment.

```mermaid
flowchart LR

  classDef blue fill:#4a90d9,stroke:#2c5f8a,color:#fff
  classDef orange fill:#e67e22,stroke:#b35a0a,color:#fff
  classDef green fill:#27ae60,stroke:#1a7a42,color:#fff

  subgraph ACQ["Acquisition"]
    direction TB
    CONTEXT["Context"]
    CONTEXT ~~~ DATUM
    DATUM["Datum"]
  end

  subgraph COLLECTION["Collection"]
    direction TB
    SAMPLE["Sample"]
  end

  ACQ --> SAMPLE
  SAMPLE --> PREP_OP

  subgraph OPERATION["AI Component — Operation"]
    direction LR
    PREP_OP["Preprocessor"]
    PREP_OP --> BACKBONE_OP["Backbone"]
    BACKBONE_OP --> LATENT_OP["Latent Space"]
    LATENT_OP --> PREDICTOR_OP["Predictor"]
    LATENT_OP --> UQ_OP["Uncertainty Quantifier"]
    LATENT_OP --> OOD_OP["OOD Detector"]

    PREP_OP --> MONITOR_OP["Online Monitoring"]
    OOD_OP --> MONITOR_OP
    UQ_OP --> MONITOR_OP
    LATENT_OP --> MONITOR_OP
    PREP_OP --> OOD_OP

    PREDICTOR_OP --> METRICS_OP["Metrics' Assembly"]
    UQ_OP --> INNER
    OOD_OP --> INNER
    MONITOR_OP --> INNER

    class BACKBONE_OP,LATENT_OP,PREDICTOR_OP blue
    class PREP_OP orange
    class MONITOR_OP,UQ_OP,OOD_OP green
    
    subgraph INNER[" "]
      direction TB
      FUNC_OUT["Functional Output"]
      AUX_OUT["Auxiliary Outputs"]
    end
  end

  STORAGE[("Storage")]
  BATCH["Batch Control"]

  INNER --> STORAGE
  COLLECTION --> STORAGE
  STORAGE --> BATCH

  subgraph OP_INTERACT["Operator Interaction"]
    direction TB
    PRED_STATUS["Prediction Status"]
    TRUST_ARTEFACTS["Trust Artefacts"]
    USER_DEC_OP["User Decision"]
  end

  USER_DEC_OP --> STORAGE
  subgraph QC["Quality Control"]
    direction TB
    BATCH["Batch Control"]
    TRUST_ARTEFACTS["Trust Artefacts"]
    USER_DEC_OP["User Decision"]
  end

  METRICS_OP --> PRED_STATUS
  INNER --> TRUST_ARTEFACTS
  PRED_STATUS --> USER_DEC_OP
  TRUST_ARTEFACTS --> USER_DEC_OP
```

**PROPOSITION OPUS:**

```mermaid
flowchart LR
  classDef blue   fill:#4a90d9,stroke:#2c5f8a,color:#fff
  classDef orange fill:#e67e22,stroke:#b35a0a,color:#fff
  classDef green  fill:#27ae60,stroke:#1a7a42,color:#fff
  classDef purple fill:#8e44ad,stroke:#6c3483,color:#fff

  subgraph ACQ["Acquisition"]
    direction TB
    CONTEXT["Context\n(seam_id, bbox_coord,\nblur_class, luminosity)"]
    DATUM["Datum\n(Image 1920×1080 ou 960×540)"]
    CONTEXT ~~~ DATUM
  end

  subgraph COLLECTION["Collection"]
    SAMPLE["Sample"]
  end

  ACQ --> SAMPLE

  subgraph OPERATION["AI Component — Operation"]
    direction LR

    PREP["Preprocessor\n(resize · normalize\nROI crop via bbox_coord)"]
    PREP --> BAG["MIL Bag Builder\n(extraction de patches)"]
    BAG --> BACKBONE["Backbone\nYOLOv5s-C3CA\n(frozen)"]
    BACKBONE --> LATENT["Latent Space\n(instance embeddings)"]
    LATENT --> MILPOOL["MIL Aggregator\n(attention pooling)"]
    MILPOOL --> PREDICTOR["Predictor\nOK / KO"]
    MILPOOL --> UQ["Uncertainty Quantifier\n(PUNCC — conformal)"]
    MILPOOL --> OOD["OOD Detector\n(OODeel)"]
    PREP --> MONITOR["Online Monitoring\n(drift blur · luminosity)"]
    OOD --> MONITOR

    class BACKBONE,LATENT,MILPOOL,PREDICTOR blue
    class PREP,BAG orange
    class UQ,OOD,MONITOR green
  end

  SAMPLE --> PREP

  subgraph OUT["Output Interface"]
    direction TB
    FUNC["Functional Output\nOK / KO / UNKNOWN"]
    AUX["Auxiliary Outputs\n(score confiance · score OOD)"]
    FUNC ~~~ AUX
  end

  PREDICTOR --> FUNC
  UQ --> FUNC
  OOD --> FUNC
  UQ --> AUX
  OOD --> AUX
  MONITOR --> AUX

  subgraph QC["Quality Control"]
    direction TB
    STATUS["Prediction Status"]
    TRUST["Trust Artefacts"]
    DECISION["Operator Decision"]
  end

  FUNC --> STATUS
  AUX --> TRUST
  STATUS --> DECISION
  TRUST --> DECISION

  STORAGE[("Storage")]
  BATCH["Batch Control"]

  OUT --> STORAGE
  COLLECTION --> STORAGE
  DECISION --> STORAGE
  STORAGE --> BATCH
```


## 2. Training Architecture
The training phase focuses on model construction and optimization.

```mermaid
flowchart LR
  classDef blue fill:#4a90d9,stroke:#2c5f8a,color:#fff
  classDef orange fill:#e67e22,stroke:#b35a0a,color:#fff
  classDef green fill:#27ae60,stroke:#1a7a42,color:#fff

  PRETRAINED_MODEL["Pretrained Models"]
  AIC_DESIGN_SPEC["AIC Design Specification"]

  subgraph DATA["Data"]
    direction TB
    DB1[("Post-op data & Feedback")]
    DB2[("Historical & synthetic data")]
    DB1 ~~~ DB2
  end

  subgraph TRAINING["AI Component — (Training)"]
    direction LR

    subgraph DATASET["Datasets"]
      direction TB
      CAL[("Calibration")]
      TRAINING_SET[("Training")]
      CAL ~~~ TRAINING_SET
    end

    DATASET --> PREP_OP["Preprocessor"]
    PREP_OP --> BACKBONE_OP["Backbone (Freeze)"]
    BACKBONE_OP --> LATENT_OP["Latent Space"]
    LATENT_OP --> PREDICTOR_OP["Predictor (Train)"]
    LATENT_OP --> UQ_OOD["UQ & OOD Calibration"]
    PREP_OP --> MONITOR_OP["Off/Online Monitoring Calibration"]
    LATENT_OP --> MONITOR_OP
    DATASET --> DATA_METRICS["Data Metrics"]

    class BACKBONE_OP,LATENT_OP,PREDICTOR_OP blue

    subgraph IU["Interdependent Updates"]
      direction TB
      MW["Models Weights"]
      PE["Prob. Estimates"]
      TV["Threshold values"]
      UAHP["User-adjustable Hyper-params"]
      MW ~~~ PE
      PE ~~~ TV
      TV ~~~ UAHP
    end
  end

  UQ_OOD --> MONITOR_OP
  UQ_OOD --> IU
  MONITOR_OP --> IU

  PRETRAINED_MODEL --> IU
  PRETRAINED_MODEL --> TRAINING
  AIC_DESIGN_SPEC --> TRAINING
  DATA --> DATASET
  DATA_METRICS --> IU

  IU --> AIC_DESIGN_CAL["AIC Design Calibration"]
```

**PROPOSITION OPUS:**

```mermaid
flowchart LR
  classDef blue   fill:#4a90d9,stroke:#2c5f8a,color:#fff
  classDef orange fill:#e67e22,stroke:#b35a0a,color:#fff
  classDef green  fill:#27ae60,stroke:#1a7a42,color:#fff

  PRETRAINED["YOLOv5s-C3CA\n(pré-entraîné ImageNet)"]
  AIC_SPEC["AIC Design Specification"]

  subgraph DATA["Data"]
    direction TB
    DB1[("Post-op data & Feedback")]
    DB2[("Historical & Synthetic data")]
    DB1 ~~~ DB2
  end

  subgraph TRAINING["AI Component — Training"]
    direction LR

    subgraph DATASETS["Datasets"]
      direction TB
      TRAIN_SET[("Training\n(MIL bags — labels image)")]
      CAL_SET[("Calibration\n(PUNCC · OODeel · Monitoring)")]
      TRAIN_SET ~~~ CAL_SET
    end

    DATASETS --> PREP["Preprocessor\n(resize · normalize\nROI crop via bbox_coord)"]
    PREP --> BAG["MIL Bag Builder\n(extraction patches)"]
    BAG --> BACKBONE["Backbone\nYOLOv5s-C3CA\n(frozen)"]
    BACKBONE --> LATENT["Latent Space"]
    LATENT --> MILPOOL["MIL Aggregator\n(attention pooling — train)"]
    MILPOOL --> PREDICTOR["Predictor\n(train — loss déséquilibre 98/2)"]
    MILPOOL --> UQ_CAL["Calibration UQ\n(PUNCC — conformal)"]
    MILPOOL --> OOD_CAL["Calibration OOD\n(OODeel)"]
    PREP --> MON_CAL["Calibration Monitoring\n(seuils blur · luminosity)"]
    LATENT --> MON_CAL
    DATASETS --> DATA_METRICS["Data Metrics\n(diversité · déséquilibre)"]

    class BACKBONE,LATENT,MILPOOL,PREDICTOR blue
    class PREP,BAG orange
    class UQ_CAL,OOD_CAL,MON_CAL green

    subgraph IU["Interdependent Updates"]
      direction TB
      MW["Model Weights\n(backbone · MIL pooling · predictor)"]
      PE["Probability Estimates\n(scores confiance PUNCC)"]
      TV["Threshold Values\n(OOD · UNKNOWN · monitoring)"]
      UAHP["User-adjustable Hyper-params"]
      MW ~~~ PE
      PE ~~~ TV
      TV ~~~ UAHP
    end
  end

  UQ_CAL --> IU
  OOD_CAL --> IU
  MON_CAL --> IU
  DATA_METRICS --> IU
  PRETRAINED --> BACKBONE
  PRETRAINED --> IU
  AIC_SPEC --> TRAINING
  DATA --> DATASETS

  IU --> AIC_CAL["AIC Design Calibration"]
```


## 3. Evaluation Architecture

The evaluation phase validates the model's performance on unseen data.

```mermaid
flowchart LR
  classDef blue fill:#4a90d9,stroke:#2c5f8a,color:#fff
  classDef orange fill:#e67e22,stroke:#b35a0a,color:#fff
  classDef green fill:#27ae60,stroke:#1a7a42,color:#fff

  AIC_DESIGN_CAL["AIC Design Calibration"]

  subgraph VALIDATION["AI Component — (Validation)"]
    direction LR

    subgraph DATASET_VAL["Datasets"]
      direction TB
      VAL[("Validation")]
      PER[("Perturbation")]
      TEST[("Test")]
      VAL ~~~ PER
      PER ~~~ TEST
    end

    DATASET_VAL --> PREP_VAL["Preprocessor"]
    PREP_VAL --> BACKBONE_VAL["Backbone (Freeze)"]
    BACKBONE_VAL --> LATENT_VAL["Latent Space"]
    LATENT_VAL --> PREDICTOR_VAL["Predictor"]
    LATENT_VAL --> UQ_VAL["Uncertainty Quantifier"]
    LATENT_VAL --> OOD_VAL["OOD Detector"]
    PREP_VAL --> MONITOR_VAL["Monitoring"]
    OOD_VAL --> MONITOR_VAL
    UQ_VAL --> MONITOR_VAL

    class BACKBONE_VAL,LATENT_VAL,PREDICTOR_VAL blue

    subgraph METRICS["Metrics Assembly"]
      direction TB
      RECALL["Recall / F1 / AUC"]
      ECE["Calibration Error (ECE)"]
      OOD_RATE["OOD Detection Rate"]
      DRIFT["Drift Indicators"]
      RECALL ~~~ ECE
      ECE ~~~ OOD_RATE
      OOD_RATE ~~~ DRIFT
    end
  end

  PREDICTOR_VAL --> METRICS
  UQ_VAL --> METRICS
  OOD_VAL --> METRICS
  MONITOR_VAL --> METRICS

  AIC_DESIGN_CAL --> VALIDATION

  subgraph PO_INTERFACE["Product Owner Interaction"]
    direction TB
    HIST_ARTEFACTS["History of Artefacts"]
    TRUST_ARTEFACTS["Trust Artefacts"]
    USER_DEC_OP["User Decision"]
  end

  METRICS --> HIST_ARTEFACTS
  METRICS --> TRUST_ARTEFACTS
  HIST_ARTEFACTS --> USER_DEC_OP
  TRUST_ARTEFACTS --> USER_DEC_OP

  USER_DEC_OP --> DEPLOY["Component Operational"]

  class DEPLOY green
```

**PROPOSITION OPUS:**

```mermaid
flowchart LR
  classDef blue   fill:#4a90d9,stroke:#2c5f8a,color:#fff
  classDef orange fill:#e67e22,stroke:#b35a0a,color:#fff
  classDef green  fill:#27ae60,stroke:#1a7a42,color:#fff

  AIC_CAL["AIC Design Calibration"]

  subgraph VALIDATION["AI Component — Evaluation"]
    direction LR

    subgraph DATASETS_VAL["Datasets"]
      direction TB
      TEST[("Test\n(cordons c20 · c102 · c33)")]
      PERTURB[("Perturbation\n(blur · flash · luminosity)")]
      OOD_SET[("OOD\n(hors ODD)")]
      TEST ~~~ PERTURB
      PERTURB ~~~ OOD_SET
    end

    DATASETS_VAL --> PREP_V["Preprocessor"]
    PREP_V --> BAG_V["MIL Bag Builder"]
    BAG_V --> BACKBONE_V["Backbone\nYOLOv5s-C3CA (frozen)"]
    BACKBONE_V --> LATENT_V["Latent Space"]
    LATENT_V --> MILPOOL_V["MIL Aggregator"]
    MILPOOL_V --> PREDICTOR_V["Predictor"]
    MILPOOL_V --> UQ_V["Uncertainty Quantifier\n(PUNCC)"]
    MILPOOL_V --> OOD_V["OOD Detector\n(OODeel)"]
    PREP_V --> MONITOR_V["Monitoring"]
    OOD_V --> MONITOR_V

    class BACKBONE_V,LATENT_V,MILPOOL_V,PREDICTOR_V blue
    class PREP_V,BAG_V orange
    class UQ_V,OOD_V,MONITOR_V green

    subgraph METRICS["Metrics Assembly\n(6 attributs de confiance)"]
      direction TB
      PERF["Performance\n(Recall · F1 · AUC)"]
      UNC["Uncertainty\n(ECE · couverture conforme)"]
      ROB["Robustesse\n(F1 sur perturbations)"]
      OOD_M["OOD Monitoring\n(taux détection OOD)"]
      GEN["Généralisation\n(cross-seam c20/c102/c33)"]
      DRIFT["Data Drift\n(indicateurs monitoring)"]
      PERF ~~~ UNC
      UNC ~~~ ROB
      ROB ~~~ OOD_M
      OOD_M ~~~ GEN
      GEN ~~~ DRIFT
    end
  end

  PREDICTOR_V --> METRICS
  UQ_V --> METRICS
  OOD_V --> METRICS
  MONITOR_V --> METRICS

  AIC_CAL --> VALIDATION

  subgraph PO["Product Owner Interaction"]
    direction TB
    HIST["History of Artefacts"]
    TRUST_V["Trust Artefacts\n(agrégation multi-critères)"]
    DECISION_V["User Decision\n(déploiement ou retour entraînement)"]
  end

  METRICS --> HIST
  METRICS --> TRUST_V
  HIST --> DECISION_V
  TRUST_V --> DECISION_V

  DECISION_V --> DEPLOY["Component Operational"]
  class DEPLOY green
```


## Software Constituents

- **ML Model_1** : xxx
- **ML Model_2** : xxx
- **ML Model_x** : xxx
- **Pre-processor**: xxx
- **Post-processor**: xxx

### ML Model_1

