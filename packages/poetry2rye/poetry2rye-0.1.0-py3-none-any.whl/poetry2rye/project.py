from pathlib import Path
import re
from typing import Optional

import slugify
import pyproject_parser
from pydantic import BaseModel
from dataclasses import dataclass

from poetry.core.constraints.version.version_constraint import VersionConstraint
from poetry.core.version.helpers import format_python_constraint
from poetry.core.constraints.version.parser import parse_constraint


# unused
def poetry_canonicalize_name(project_name: str) -> str:
    """
    Convert a project name to a canonical form by Poetry-Style.
    """
    return re.sub(r"[-_.]+", "-", project_name).lower()


# memo: How does Poetry decide on module names?


def rye_canonicalize_name(project_name: str) -> str:
    return slugify.slugify(project_name)


def rye_module_name(project_name: str) -> str:
    return rye_canonicalize_name(project_name).replace("-", "_")


@dataclass
class Dependency:
    name: str
    version: VersionConstraint
    extras: Optional[list[str]]
    is_dev: bool


class PoetryProject:
    def __init__(self, project_path: Path) -> None:
        self.path = project_path
        self.project_name = rye_canonicalize_name(self.path.name)
        self.module_name = rye_module_name(self.path.name)

        assert (self.path / "pyproject.toml").exists(), "pyproject.toml not found"

        self.pyproject = pyproject_parser.PyProject.load(self.path / "pyproject.toml")
        self.poetry = self.pyproject.tool["poetry"]

        assert self.pyproject.project is None, "for now, poetry2rye only supports " \
                                               "pyproject.toml written using " \
                                               "tool.poetry. this may change in the " \
                                               "future."
        assert self.poetry is not None, "poetry section not found in pyproject.toml"

        self.src_path: Path
        # this method is not exact, but tentatively we do this
        if (self.path / "src").exists():
            self.src_path = self.path / "src"
        else:
            self.src_path = self.path

        self.module_path = self.src_path / self.module_name
        assert self.module_path.exists(), "module not found"

    @property
    def dependencies(self) -> list[Dependency]:
        res = []

        dep = self.poetry["dependencies"]
        if dep is not None:
            for name, item in dep.items():
                if isinstance(item, str):
                    res.append(Dependency(name=name, version=parse_constraint(item), extras=None, is_dev=False))
                else:
                    res.append(
                        Dependency(
                            name=name,
                            version=parse_constraint(item["version"]),
                            extras=item["extras"],
                            is_dev=False,
                        )
                    )

        try:
            dev_dep = self.poetry["group"]["dev"]["dependencies"]
        except KeyError:
            dev_dep = None
        if dev_dep is not None:
            for name, item in dev_dep.items():
                if isinstance(item, str):
                    res.append(Dependency(name=name, version=parse_constraint(item), extras=None, is_dev=True))
                else:
                    res.append(
                        Dependency(
                            name=name,
                            version=parse_constraint(item["version"]),
                            extras=item["extras"],
                            is_dev=True,
                        )
                    )

        return res
