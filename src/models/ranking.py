

from pydantic import BaseModel

class Ranking(BaseModel):
    filename: str
    sum_functional_terms: int
    sum_terms: int
    rank: float