# User Guide

This guide will walk you through how to use the `tp-composant-ia` workspace.

## Prerequisites

Ensure you have `uv` installed. Follow the installation guide at [astral.sh/uv](https://astral.sh/uv).

## Adding a Package

To add a new AI component package to the workspace:

```bash
mkdir -p packages/my-new-component/src/my_new_component
touch packages/my-new-component/pyproject.toml
touch packages/my-new-component/src/my_new_component/__init__.py
```

Add a `pyproject.toml` to the new package:

```toml
[project]
name = "my-new-component"
version = "0.1.0"
description = "A new AI component"
dependencies = []

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

Then run:

```bash
uv sync
```

## Running Tasks

Tasks are managed with `nox`:

```bash
uv run nox -s lint
uv run nox -s type_check
uv run nox -s docs
```
