import nltk

nltk.download("punkt")
nltk.download("stopwords")

from schatsi.jobs import *

nltk.download("punkt")

if __name__ == "__main__":
    job = ParallelJob("data/input", "data/output", "data/metadata/functional_terms.csv", "data/metadta/negative_terms.csv")
    job.process()
    
    