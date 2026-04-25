# Contributing to TP Composant IA

Thank you for your interest in contributing to TP Composant IA! This project is designed to be a modular workspace for AI components.

## Development Environment Setup

We use `uv` for workspace management and `nox` for automation.

### 1. Prerequisites

- Install `uv`: [astral.sh/uv](https://astral.sh/uv)
- Install `git`

### 2. Workspace Initialization

Synchronize the workspace and install all dependencies:

```bash
uv sync
```

### 3. Quality Standards

We enforce strict quality checks via `nox`. Please ensure all checks pass before submitting a PR.

* `uv run nox -s lint`: Check for style issues (ruff).
* `uv run nox -s fmt`: Automatically format code.
* `uv run nox -s type_check`: Static type analysis with MyPy.
* `uv run nox -s docs`: Build the documentation.

## Creating a New Component

To add a new component to the workspace:

1.  Create a new directory in `packages/`.
2.  Initialize a new Python package with its own `pyproject.toml`.
3.  Add the package to the root `pyproject.toml` workspace members (already configured for `packages/*`).
4.  Run `uv sync` to update the workspace.

## Documentation

To preview the documentation locally:

```bash
uv run nox -s docs_serve
```

Or directly using mkdocs:

```bash
uv run mkdocs serve
```
