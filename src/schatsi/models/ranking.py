from typing import Union
from pydantic import BaseModel


class Ranking(BaseModel):
    """Model that represents the ranking of a file.

    Args:
        BaseModel (_type_): _description_
    """

    filename: str
    sum_functional_terms: int
    sum_terms: int
    cluster: Union[None, str]
    rank: float
