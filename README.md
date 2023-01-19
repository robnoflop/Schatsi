# (f)SCHA.T.S.I

(f)SCHA.T.S.I - An abbreviation for '**f**aster **SCH**eduling *A*lgorithm for **T**ext **S**each **I**ntelligence'.


## Getting Started
https://python-poetry.org/
```
pip install poetry
poetry lock
.venv\Scripts\activate
poetry config virtualenvs.in-project true
poetry install
```

Generate documentation
----------------------

Theme documentation: https://sphinx-rtd-theme.readthedocs.io/en/stable/index.html
apidoc documentation: https://www.sphinx-doc.org/en/master/man/sphinx-apidoc.html


os.environ["SPHINX_APIDOC_OPTIONS"]="members,show-inheritance"

Windows

```shell
cd docs
sphinx-apidoc -lfM -d 0 -o drg_analytic/ ../src/drg_analytic
.\make.bat html
```

Mac/Linux

```shell
cd docs
sphinx-apidoc -lfM -d 0 -o drg_analytic/ ../src/drg_analytic
make html
```