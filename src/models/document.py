
from typing import Any, List, Union
from pydantic import BaseModel


class Document(BaseModel):
    raw_text: Union[None,str] = None
    file_type: Union[None,str] = None
    title: Union[None,str] = None
    toc: Union[None,List[Any]] = None
    author: Union[None,str] = None
    abstract: Union[None,str] = None
    keywords: Union[None,str] = None
    content: Union[None,str] = None
    references: Union[None,str] = None