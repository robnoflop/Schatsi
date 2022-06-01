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
SCHATSI_INPUT_FOLDER = os.path.join(path_prefix, "input")
SCHATSI_OUTPUT_FOLDER = os.path.join(path_prefix, "output")
SCHATSI_FUNCTIONAL_TERMS = os.path.join(SCHATSI_INPUT_FOLDER, "functional_terms.csv")
SCHATSI_NEGATIVE_TERMS = os.path.join(SCHATSI_INPUT_FOLDER,"negative_terms.csv")
SCHATSI_RUNTIME = os.path.join(SCHATSI_OUTPUT_FOLDER, "schatsi_runtime.csv")

# Static input
if run_id == '':
    SCHATSI_STOPWORDS = "params/stopwords.csv"
else:
    SCHATSI_STOPWORDS = os.path.join(path_prefix, "params/stopwords.csv")



