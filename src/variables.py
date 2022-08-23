"""
In This File  the paths of the files will be specified. This is nessesary because the files lie in a docker container, which uses a debian linux distro as base and local files from the user will be loaded into the container and local directories will be used as volumes, so the path must be specified

In the moment SCHATSI can be used locally and in a cloud environment, so the input- and output paths varie.
"""

import os

# User specific RUN_ID for aws session
run_id = os.getenv('RUN_ID', default='')
if run_id == '':
    # if docker is executed locally, there will be no run_id, and therefore we don't need a path on the cloud for the params
    path_prefix = '/data'
    print("RUN_ID is EMPTY")
else:
    # if docker is executed in the cloud, we define a path with a folder named 'data' in between
    path_prefix = os.path.join("/data", run_id)
    print("RUN_ID is NOT EMPTY")

# User specific inputs and outputs
# This path contains the input files (i.e. the papers)
SCHATSI_INPUT_FOLDER = os.path.join(path_prefix, "input")
# this path specifies where the output of container
SCHATSI_OUTPUT_FOLDER = os.path.join(path_prefix, "output")
# the path for the functional_terms.csv
SCHATSI_FUNCTIONAL_TERMS = os.path.join(SCHATSI_INPUT_FOLDER, "functional_terms.csv")
# the path for the negative_terms.csv
SCHATSI_NEGATIVE_TERMS = os.path.join(SCHATSI_INPUT_FOLDER,"negative_terms.csv")
# the path for the runtime.csv
SCHATSI_RUNTIME = os.path.join(SCHATSI_OUTPUT_FOLDER, "schatsi_runtime.csv")

# Static input
# in the moment there is only the "stopwords.csv" as a parameter file. But when other static input files will be needed /path_prefix/params/FILENAME is the right place for it
SCHATSI_STOPWORDS = "/params/stopwords.csv"



