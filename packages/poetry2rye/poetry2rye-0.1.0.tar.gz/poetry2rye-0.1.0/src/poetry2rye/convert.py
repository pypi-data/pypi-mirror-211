import os
from pathlib import Path

from poetry.core.constraints.version import Version, VersionUnion

from poetry2rye.project import PoetryProject
from poetry.core.constraints.version.version_constraint import VersionConstraint
from poetry.core.version.helpers import format_python_constraint, PYTHON_VERSION
from poetry.core.constraints.version.parser import parse_constraint

from copy import deepcopy

import shutil

from itertools import filterfalse

import tomlkit


def convert(project_path: Path) -> None:
    backup_path = project_path.parent / f"__p2r_backup_{project_path.name}"
    shutil.rmtree(backup_path, ignore_errors=True)
    shutil.copytree(project_path, backup_path, dirs_exist_ok=True)
    print(f"created backup: {backup_path}")

    poetry_project = PoetryProject(project_path)

    project_sec = {}
    urls_sec = {}

    # required
    project_sec["name"] = poetry_project.project_name
    project_sec["version"] = poetry_project.poetry["version"]
    project_sec["description"] = poetry_project.poetry["description"]

    # license (not used due to different format)
    if poetry_project.poetry.get("license"):
        pass

    # authors / maintainers
    authors = []
    for author in poetry_project.poetry["authors"]:
        seps = author.split()
        assert len(seps) == 2
        authors.append({"name": seps[0], "email": seps[1][1:-1]})
    if authors:
        project_sec["authors"] = tomlkit.array()
        project_sec["authors"].extend(authors)

    maintainers = []
    for maintainer in poetry_project.poetry.get("maintainers", []):
        seps = maintainer.split()
        assert len(seps) == 2
        maintainers.append({"name": seps[0], "email": seps[1][1:-1]})
    if maintainers:
        project_sec["maintainers"] = tomlkit.array()
        project_sec["maintainers"].extend(maintainers)

    # readme
    if poetry_project.poetry.get("readme"):
        project_sec["readme"] = poetry_project.poetry["readme"]

    # urls
    if poetry_project.poetry.get("homepage"):
        urls_sec["Homepage"] = poetry_project.poetry["homepage"]
    if poetry_project.poetry.get("repository"):
        urls_sec["Repository"] = poetry_project.poetry["repository"]
    if poetry_project.poetry.get("documentation"):
        urls_sec["Documentation"] = poetry_project.poetry["documentation"]

    # keywords / classifiers
    if poetry_project.poetry.get("keywords"):
        project_sec["keywords"] = poetry_project.poetry["keywords"]
    if poetry_project.poetry.get("classifiers"):
        project_sec["classifiers"] = poetry_project.poetry["classifiers"]

    # packages
    if poetry_project.poetry.get("packages"):
        # ToDo
        pass

    # dependencies
    project_sec["dependencies"] = []
    for dep in poetry_project.dependencies:
        if dep.name == "python":
            project_sec["requires-python"] = format_python_constraint(dep.version)
        else:
            project_sec["dependencies"].append(f"{dep.name}{format_python_constraint(dep.version)}")

    with open(project_path / "pyproject.toml") as f:
        pyproject = tomlkit.load(f)

    # create result
    result = tomlkit.document()

    result["project"] = project_sec
    if urls_sec:
        result["project.urls"] = urls_sec

    for name in pyproject.keys():
        if name == "project":
            continue
        elif name == "tool":
            result["tool"] = deepcopy(pyproject["tool"])
            result["tool"].pop("poetry")
        elif name == "build-system":
            result["build-system"] = deepcopy(pyproject["build-system"])
            result["build-system"]["requires"] = list(filterfalse(lambda x: "poetry-core" in x, result["build-system"]["requires"]))
            result["build-system"]["requires"].append("hatchling")
            result["build-system"]["build-backend"] = "hatchling.build"
        else:
            result[name] = deepcopy(pyproject[name])

    result["tool"]["rye"] = {"managed": True}
    result["tool"]["hatch"] = {
        "metadata": {"allow-direct-references": True}
    }

    with open(project_path / "pyproject.toml", "w") as f:
        f.write(tomlkit.dumps(result))

    # find "poetry" in pyproject.toml and print it
    with open(project_path / "pyproject.toml") as f:
        for num, content in enumerate(f.readlines(), start=1):
            if "poetry" in content:
                print(f"Found 'poetry' in line {num}: {content}")

    os.remove(project_path / "poetry.lock")
    if not (project_path / "src").exists():
        (project_path / "src").mkdir()
        shutil.move(poetry_project.module_path, project_path / "src" / poetry_project.module_name)
