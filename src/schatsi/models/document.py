
from typing import Any, List, Union
from pydantic import BaseModel


class Document(BaseModel):
    """
        Model that represents a Documente with all it's imporant components.

    Args:
        BaseModel (_type_): Thy pydantic base class.
    """
    filename: str
    raw_text: Union[None,str] = None
    word_count_raw_text: Union[None,int] = None
    file_type: Union[None,str] = None
    title: Union[None,str] = None
    toc: Union[None,List[Any]] = None
    author: Union[None,str] = None
    abstract: Union[None,str] = None
    keywords: Union[None,str] = None
    content: Union[None,str] = None
    references: Union[None,str] = None
    word_count_reference: Union[None,int] = None
    include: bool = True