import pandas as pd

class Ranker:
    
    def __init__(self, path_functional_terms) -> None:
        self.functional_terms = pd.read_csv(path_functional_terms)
    
    def rank(self, terms_df: pd.DataFrame) -> dict:
        sum_terms = terms_df["term count"].sum()
        filename = terms_df["filename"].values[0]

        terms_df = self.functional_terms.join(terms_df.set_index("term"), on="term", how="inner")
        sum_functional_terms = terms_df["term count"].sum()
        rank = sum_functional_terms / sum_terms

        return {
            "filename": filename,
            "sum_functional_terms": sum_functional_terms,
            "sum_terms": sum_terms,
            "rank": rank,
        }