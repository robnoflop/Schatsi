

from typing import Any, List, Union
from pydantic import BaseModel

class Metadata(BaseModel):
    filename: str
    file_type: Union[None,str]
    titel: Union[None,str]
    toc: Union[None,List[Any]]
    text: Union[None,str]
    word_count_text: Union[None,int]
    references: Union[None,str]
    word_count_reference: Union[None,int]
    include: bool