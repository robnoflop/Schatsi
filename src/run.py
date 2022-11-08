import nltk


from schatsi.jobs import *

nltk.download("punkt")

if __name__ == "__main__":
    job = SingleJob("data/input", "data/output", "data/metadata/functional_terms.csv", "data/metadta/negative_terms.csv")
    job.process()
    
    