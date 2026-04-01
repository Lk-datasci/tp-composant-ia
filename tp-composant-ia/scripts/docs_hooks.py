from pathlib import Path
import shutil


def update_readme_relative_links():
    index = Path("docs/index.md")
    if not index.exists():
        return
    with index.open() as f:
        md = f.read()
        updated_md = md.replace("./docs/", "./")
        updated_md = updated_md.replace(
            "(packages/",
            "(https://github.com/loic/tp-composant-ia/tree/main/packages/",
        )
    with index.open("w") as f:
        f.write(updated_md)


def copy_readme():
    shutil.copy("README.md", "docs/index.md")


def pre_build(*args, **kwargs):
    copy_readme()
    update_readme_relative_links()
