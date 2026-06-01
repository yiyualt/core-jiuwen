# docs/conf.py — Sphinx configuration for jiuwen
"""Sphinx documentation configuration."""

project = "jiuwen"
copyright = "2025, jiuwen contributors"
author = "jiuwen contributors"
release = "0.0.1"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
]

html_theme = "sphinx_book_theme"
html_title = "jiuwen Documentation"
html_static_path = []
templates_path = []

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# sphinx-book-theme options
html_theme_options = {
    "repository_url": "",
    "use_repository_button": False,
    "use_issues_button": False,
    "use_edit_page_button": False,
}

# Intersphinx
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}
