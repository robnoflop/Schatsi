# (f)SCHA.T.S.I

(f)SCHA.T.S.I - An abbreviation for '**f**aster **SCH**eduling *A*lgorithm for **T**ext **S**each **I**ntelligence'.


## Getting Started
https://python-poetry.org/
```
pip install poetry
poetry lock
poetry config virtualenvs.in-project true
poetry install
poetry shell
```

Generate documentation
----------------------

Theme documentation: https://sphinx-rtd-theme.readthedocs.io/en/stable/index.html
apidoc documentation: https://www.sphinx-doc.org/en/master/man/sphinx-apidoc.html


os.environ["SPHINX_APIDOC_OPTIONS"]="members,show-inheritance"

Windows

```shell
cd docs
sphinx-apidoc -lfM -d 0 -o schatsi/ ../src/schatsi
.\make.bat html
```

Mac/Linux

```shell
cd docs
sphinx-apidoc -lfM -d 0 -o schatsi/ ../src/schatsi
make html
```

## Project Structure
```
├── data
│   ├── input
│   ├── metadata
│   └── output
├── docs
│   └── schatsi
└── src
    ├── schatsi
    │   ├── jobs
    │   ├── models
    │   ├── processor
    │   └── reader
    └── schatsi-ui
        └── components
``````