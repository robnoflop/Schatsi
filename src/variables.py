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
<<<<<<< HEAD
SCHATSI_STOPWORDS = os.path.join(path_prefix, "params/stopwords.csv")
=======
SCHATSI_STOPWORDS = os.path.join(path_prefix, "/params/stopwords.csv")

>>>>>>> 9e50e758a057d337c2536f473dcad0df681b506d
