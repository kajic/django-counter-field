"""Sphinx configuration for django-counter-field documentation."""

from pathlib import Path
import sys

# Add project root to path for autodoc
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Configure Django settings for autodoc
from django.conf import settings

if not settings.configured:
    settings.configure()

# Get version from package
from django_counter_field import __version__

# -- General configuration -----------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.viewcode",
]

templates_path = ["_templates"]
source_suffix = ".rst"
master_doc = "index"

project = "django-counter-field"
copyright = "2013-2025, Robert Kajic"

version = __version__
release = __version__

exclude_patterns = []
pygments_style = "sphinx"

# -- Options for HTML output ---------------------------------------------------

html_theme = "default"
html_static_path = ["_static"]
htmlhelp_basename = "django-counter-fielddoc"

# -- Options for LaTeX output --------------------------------------------------

latex_elements = {}
latex_documents = [
    (
        "index",
        "django-counter-field.tex",
        "django-counter-field Documentation",
        "Robert Kajic",
        "manual",
    ),
]

# -- Options for manual page output --------------------------------------------

man_pages = [
    ("index", "django-counter-field", "django-counter-field Documentation", ["Robert Kajic"], 1)
]

# -- Options for Texinfo output ------------------------------------------------

texinfo_documents = [
    (
        "index",
        "django-counter-field",
        "django-counter-field Documentation",
        "Robert Kajic",
        "django-counter-field",
        "Django counter field for tracking related model counts.",
        "Miscellaneous",
    ),
]

# Example configuration for intersphinx
intersphinx_mapping = {"python": ("https://docs.python.org/3/", None)}
