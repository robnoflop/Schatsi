import os

# User specific RUN_ID for aws session
run_id = os.getenv('RUN_ID', default='')
path_prefix = os.path.join("/data", run_id)

# User specific inputs and outputs
SCHATSI_INPUT_FOLDER = os.path.join(path_prefix, "input")
SCHATSI_OUTPUT_FOLDER = os.path.join(path_prefix, "output")
SCHATSI_FUNCTIONAL_TERMS = os.path.join(SCHATSI_INPUT_FOLDER, "functional_terms.csv")
SCHATSI_RUNTIME = os.path.join(SCHATSI_OUTPUT_FOLDER, "schatsi_runtime.csv")

# Static input
SCHATSI_STOPWORDS = os.path.join(path_prefix, "params/stopwords.csv")

