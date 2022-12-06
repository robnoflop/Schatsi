from typing import Callable, List
import pandas as pd
from pyparsing import condition_as_parse_action

from schatsi.models.ranking import Ranking


class Ranker:
    """_summary_
    """
    def __init__(self, path_functional_terms: str):
        """_summary_

        Args:
            path_functional_terms (str): _description_
        """
        self.functional_terms = pd.read_csv(path_functional_terms)

    def rank(
        self, terms_df: pd.DataFrame, condition: List[Callable] = None
    ) -> List[Ranking]:
        """_summary_

        Args:
            terms_df (pd.DataFrame): _description_
            condition (List[Callable], optional): _description_. Defaults to None.

        Returns:
            List[Ranking]: _description_
        """
        if condition:
            for c in condition:
                self.functional_terms.term = self.functional_terms.term.apply(
                    lambda x: c(x)
                )

        sum_terms = terms_df["term count"].sum()
        filename = terms_df["filename"].values[0]

        terms_df = self.functional_terms.join(
            terms_df.set_index("term"), on="term", how="inner"
        )
        rankings: List[Ranking] = []
        for k, g in terms_df.groupby(by="cluster"):
            sum_functional_terms = g["term count"].sum()
            rank = sum_functional_terms / sum_terms

            rankings.append(
                Ranking(
                    filename=filename,
                    sum_functional_terms=sum_functional_terms,
                    sum_terms=sum_terms,
                    cluster=k,
                    rank=rank,
                )
            )

        sum_functional_terms = terms_df["term count"].sum()
        rank = sum_functional_terms / sum_terms

        rankings.append(
            Ranking(
                filename=filename,
                sum_functional_terms=sum_functional_terms,
                sum_terms=sum_terms,
                cluster=None,
                rank=rank,
            )
        )

        return rankings
