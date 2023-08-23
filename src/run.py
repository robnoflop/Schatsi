import nltk
from schatsi.jobs import *

# the punkt tokenizer model helps to split text into sentences
# the stopwords corpus helps to identify words that are not relevant for the analysis
nltk.download("punkt")
nltk.download("stopwords")

if __name__ == "__main__":
    job = ParallelJob("data/input", "data/output", "data/metadata/functional_terms.csv", "data/metadta/negative_terms.csv")
    job.process()
    
    