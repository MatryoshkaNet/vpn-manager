import datetime


project = "MatryoshkaNet"
copyright = f"{datetime.date.today().year}, MatryoshkaNet"  # noqa: A001
author = "Vlad Korneev"
release = "0.1.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
]

templates_path = ["_templates"]

language = "en"

html_theme = "furo"
html_static_path = ["_static"]
