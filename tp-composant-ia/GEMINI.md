# Project Requirements

Mode: Execute

## Objective: "Travaux Pratique" (TP) Structure for Students
Create a structured repository and documentation for an AI component project based on the [Welding Quality Detection Challenge](https://etaia.github.io/Welding-Quality-Detection-Challenge/).

### Scope
- **Documentation**: Heavy focus on Markdown and Mermaid diagrams for the 4 pillars.
- **Implementation**: Limited to Python interface definitions (abstract classes or stubs returning random values).
- **Structure**: Future-proof `uv` workspace layout.

---

## Execution Plan

### Phase 1: Infrastructure & Navigation
- [x] Configure `mkdocs.yml` to include the 4 pillars in the navigation sidebar.
- [x] Ensure the `packages/tp-welding` structure is correctly registered in the `uv` workspace.
- [x] Create the directory skeleton: `docs/{architecture,datasets,kpi,artefacts}`.

### Phase 2: Pillar 1 - Architecture
- [x] **Docs**: Create `docs/architecture/index.md`.
    - Mermaid diagrams: Operation, Training, Evaluation.
    - MD blocks describing the AI component, data flow, and software constituents.
- [x] **Code**: Define `packages/tp-welding/src/tp_welding/interfaces/architecture.py` with the main component interface.

### Phase 3: Pillar 2 - Datasets
- [x] **Docs**: Create `docs/datasets/index.md`.
    - MD blocks for constitution methods (e.g., data augmentation for welding defects).
    - Usage descriptions and metadata identification (e.g., weld type, material).
- [x] **Code**: Define `packages/tp-welding/src/tp_welding/interfaces/datasets.py` for data generation and selection.

### Phase 4: Pillar 3 - KPIs
- [x] **Docs**: Create `docs/kpi/index.md`.
    - Descriptions of robustness and confidence KPIs.
    - Mapping KPIs to lifecycle phases (Construction, Training, Eval, Ops).
- [x] **Code**: Define `packages/tp-welding/src/tp_welding/interfaces/kpi.py` for metric calculation.

### Phase 5: Pillar 4 - Artefacts
- [x] **Docs**: Create `docs/artefacts/index.md`.
    - MD blocks describing aggregation methods.
    - Visual representation placeholders (e.g., mock bar graphs or Mermaid charts).
    - Usage/Validation scenarios for stakeholders.

### Phase 6: Git History Simulation
- [ ] Execute commits with distinct author profiles (if supported) or clear message headers to simulate student collaboration.

# Project-Wide `GEMINI.md` Registry

*   `/GEMINI.md`
*   `/packages/tp-welding/GEMINI.md`
