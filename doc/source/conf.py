# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

from __future__ import print_function

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import shutil
# import sys
# sys.path.insert(0, os.path.abspath('.'))

on_rtd = os.environ.get('READTHEDOCS') == 'True'
# https://docs.readthedocs.io/en/latest/builds.html#build-environment
# https://docs.readthedocs.io/en/latest/faq.html#how-do-i-change-behavior-for-read-the-docs


# -- Project information -----------------------------------------------------

project = u'adaptive​heatmap'  # Note: "ZERO WIDTH SPACE" before "heatmap"
copyright = '2018, Takafumi Arakaki'
author = 'Takafumi Arakaki'

# The short X.Y version
version = '0'
# The full version, including alpha/beta/rc tags
release = '0'


# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx_gallery.gen_gallery',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'en'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path .
exclude_patterns = []

# The reST default role (used for this markup: `text`) to use for all
# documents.
default_role = 'py:obj'

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
# https://alabaster.readthedocs.io/en/latest/customization.html
html_theme_options = {
    'github_user': 'tkf',
    'github_repo': 'adaptiveheatmap',
    'fixed_sidebar': True,
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
# https://alabaster.readthedocs.io/en/latest/installation.html
html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'relations.html',
        'searchbox.html',
        'donate.html',
    ]
}


# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'adaptiveheatmapdoc'


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'adaptiveheatmap.tex', 'adaptiveheatmap Documentation',
     'Takafumi Arakaki', 'manual'),
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'adaptiveheatmap', 'adaptiveheatmap Documentation',
     [author], 1)
]


# -- Options for Texinfo output ----------------------------------------------

# -- Options for autodoc extension -------------------------------------------
# http://www.sphinx-doc.org/en/master/ext/autodoc.html

autodoc_default_flags = [
    'members',
]

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'adaptiveheatmap', 'adaptiveheatmap Documentation',
     author, 'adaptiveheatmap', 'One line description of project.',
     'Miscellaneous'),
]


# -- Extension configuration -------------------------------------------------

# -- Options for intersphinx extension ---------------------------------------

intersphinx_mapping = {
    'python': ('http://docs.python.org/', None),
    'numpy': ('http://docs.scipy.org/doc/numpy/', None),
    # 'scipy': ('http://docs.scipy.org/doc/scipy/reference/', None),
    'matplotlib': ('http://matplotlib.org/', None),
    # 'pandas': ('http://pandas.pydata.org/pandas-docs/stable/', None),
}

# -- Options for todo extension ----------------------------------------------

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

# -- Options for Sphinx-Gallery extension ------------------------------------

sphinx_gallery_conf = {
    # path to your examples scripts
    'examples_dirs': '../../examples',
    # path where to save gallery generated examples
    'gallery_dirs': 'gallery',
    # Link code to documentation
    'reference_url': {
        'adaptiveheatmap': None,  # None for local document
    },
    # Reference examples from code:
    'backreferences_dir': 'backreferences',
    'doc_module': ('adaptiveheatmap',),
}
# http://sphinx-gallery.readthedocs.io/en/latest/advanced_configuration.html


def _remove_gallery():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gallery')
    if os.path.exists(path):
        print("*** doc/source/gallery exists! ***")
        print("Removing", path, "...")
        shutil.rmtree(path, ignore_errors=True)
        print(path, "removed!")

if on_rtd:
    _remove_gallery()
