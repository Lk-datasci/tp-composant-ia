# TP Composant IA

A workspace for AI components, inspired by `dqm-ml-workspace`.

## Setup

1.  Install `uv` (https://docs.astral.sh/uv/getting-started/installation/)
2.  Install dependencies:
    ```bash
    uv sync
    ```

## Documentation

To build and serve the documentation locally:
```bash
uv run nox -s docs
```
or
```bash
uv run mkdocs serve
```

## Structure

- `packages/`: Directory for workspace packages.
- `docs/`: Documentation sources.
- `noxfile.py`: Automation scripts.
