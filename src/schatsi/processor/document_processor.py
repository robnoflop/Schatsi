

from ast import keyword
from models.document import Document


class DocumentProcessor:
    """_summary_
    """
    
    def __init__(self) -> None:
        """_summary_
        """
        pass
    
    def split_into_parts(self, text:str) -> Document:
        """_summary_

        Args:
            text (str): _description_

        Returns:
            Document: _description_
        """
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