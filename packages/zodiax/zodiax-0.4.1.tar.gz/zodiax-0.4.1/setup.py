import setuptools
import os
import codecs
import re

long_description = "Extending Equinox for scientific programming"

here = os.path.abspath(os.path.dirname(__file__))
def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

# DEPENDENCIES
# 1. What are the required dependencies?
with open('requirements.txt') as f:
    install_requires = f.read().splitlines()
# 2. What dependencies required to run the unit tests? (i.e. `pytest --remote-data`)
tests_require = ['pytest']
docs_require = ['optax', 'matplotlib', 'jupyter', 'jupyterlab', 'tqdm',
    'chainconsumer', 'numpyro', "mkdocs", "mkdocs-jupyter", 
    "mkdocs-same-dir", "mkdocs-autorefs", "mkdocs-simple-plugin", 
    "mkdocstrings-python", "jupyter_contrib_nbextensions"]


setuptools.setup(
    python_requires='>=3.8, <4',
    name="zodiax",
    version=find_version("zodiax", "__init__.py"),
    description="Equinox extension for scientific programming",
    long_description=long_description,

    author="Louis Desdoigts",
    author_email="Louis.Desdoigts@sydney.edu.au",
    url="https://github.com/LouisDesdoigts/zodiax",

    project_urls={
        "Bug Tracker": "https://github.com/LouisDesdoigts/zodiax/issues",
    },

    install_requires=install_requires,
    extras_require={
        'docs': docs_require, 
        'tests' : tests_require
        },

    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],

    packages = ["zodiax", "zodiax/experimental"],
)
