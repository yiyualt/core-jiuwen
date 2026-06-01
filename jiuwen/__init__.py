# coding: utf-8
"""jiuwen — An educational reproduction of an AI agent SDK."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("jiuwen")
except PackageNotFoundError:
    import tomllib
    from pathlib import Path

    __version__ = "unknown"
    pyproject = Path(__file__).parents[1] / "pyproject.toml"
    if pyproject.exists():
        project_metadata = tomllib.loads(pyproject.read_text(encoding="utf-8")).get("project", {})
        version_parsed = project_metadata.get("version")
        if version_parsed:
            __version__ = version_parsed

__all__ = ["__version__"]
