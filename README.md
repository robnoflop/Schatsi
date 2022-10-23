# SCHA.T.S.I
(GERMAN VERSION AT THE BOTTOM OF EACH CHAPTER)

SCHA.T.S.I - An abbreviation for '**SCH**eduling *A*lgorithm for **T**ext **S**each **I**ntelligence'.
This project is located at the Chair of Service Operation at the University of Rostock. As development progresses, the software is intended to accelerate the analysis of scientific papers and publications and to provide the user with an overview of the interrelationships between papers and a prioritization of publications for the user with respect to his self-imposed specifications, even when hundreds of publications are involved.
In addition to the analysis, the results will be provided not only in tabular form, but additionally in a graphical overview to be able to penetrate the relationships between the papers and their authors.
For this purpose, techniques of text analysis, natural language processing (NLP) and machine learning (ML) are used.

Currently, SCHA.T.S.I can be used on Windows and Linux and with Release 1.3 a Beta version for MacOS accessible (No Guarrentee - Feedback is Welcome) :-)

## Getting Started

pip install poetry
poetry install



poetry build
poetry config pypi-token.pypi <token>
poetry publish