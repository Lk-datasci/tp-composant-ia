from nox import Session, options, param, parametrize
from nox_uv import session

options.error_on_external_run = True
options.default_venv_backend = "uv"
options.sessions = ["lint", "type_check"]


@session(venv_backend="none")
@parametrize(
    "command",
    [
        param(
            [
                "ruff",
                "check",
                "packages",
                "--select",
                "I",
                "--select",
                "F401",
                "--extend-fixable",
                "F401",
                "--fix",
            ],
            id="sort_imports",
        ),
        param(["ruff", "format", "packages"], id="format"),
    ],
)
def fmt(s: Session, command: list[str]) -> None:
    s.run(*command)


@session(venv_backend="none")
@parametrize(
    "command",
    [
        param(["ruff", "check", "packages"], id="lint_check"),
        param(["ruff", "format", "--check", "packages"], id="format_check"),
    ],
)
def lint(s: Session, command: list[str]) -> None:
    s.run(*command)


@session(venv_backend="none")
def type_check(s: Session) -> None:
    s.run("mypy", "packages", "noxfile.py")


doc_env = {"PYTHONPATH": ".:packages"}


@session(
    python=["3.12"],
    uv_groups=["docs"],
)
def docs(s: Session) -> None:
    s.run(
        "mkdocs",
        "build",
        "--strict",
        env=doc_env,
    )


@session(
    python=["3.12"],
    uv_groups=["docs"],
)
def docs_serve(s: Session) -> None:
    s.run(
        "mkdocs",
        "serve",
        env=doc_env,
    )
