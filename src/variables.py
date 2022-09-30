"""
In This File  the paths of the files will be specified. This is nessesary because the files lie in a docker container, which uses a debian linux distro as base and local files from the user will be loaded into the container and local directories will be used as volumes, so the path must be specified

In the moment SCHATSI can be used locally and in a cloud environment, so the input- and output paths varie.
"""

import os

path_prefix = "data"

SCHATSI_INPUT_FOLDER = os.path.join(path_prefix, "input")
SCHATSI_OUTPUT_FOLDER = os.path.join(path_prefix, "output")
SCHATSI_METADATA_FOLDER = os.path.join(path_prefix, "metadata")

SCHATSI_FUNCTIONAL_TERMS = os.path.join(SCHATSI_METADATA_FOLDER, "functional_terms.csv")
SCHATSI_NEGATIVE_TERMS = os.path.join(SCHATSI_METADATA_FOLDER, "negative_terms.csv")
SCHATSI_STOPWORDS = os.path.join(SCHATSI_METADATA_FOLDER, "stopwords.csv")
SCHATSI_RUNTIME = os.path.join(SCHATSI_OUTPUT_FOLDER, "schatsi_runtime.csv")
