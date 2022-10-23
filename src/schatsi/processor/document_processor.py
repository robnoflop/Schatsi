

from ast import keyword
from models.document import Document


class DocumentProcessor:
    
    def __init__(self) -> None:
        pass
    
    def split_into_parts(self, text:str) -> Document:
        title = self.__get_title(text)
        abstrct = self.__get_abstract(text)
        content = self.__get_content(text)
        keywords = self.__get_keywords(text)
        return Document(text, title, abstrct, content, keywords)
    
    def __get_title(self, text: str) -> str:
        pass
    
    def __get_abstract(self, text: str) -> str:
        pass
    
    def __get_content(self, text: str) -> str:
        pass
    
    def __get_keywords(self, text: str) -> str:
        pass