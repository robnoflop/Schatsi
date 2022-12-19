from asyncio.log import logger
from pathlib import Path
from typing import Union
from schatsi.models.document import Document
from schatsi.reader.base_reader import BaseReader
from schatsi.reader.pdf_reader import PdfReader
from schatsi.reader.docx_reader import DocxReader

from schatsi.reader.reader_type import ReaderType


class ReaderFacade:
    """_summary_

    Raises:
        Exception: _description_

    Returns:
        _type_: _description_
    """
    reader = {
        ReaderType.PDF: PdfReader(),
        ReaderType.DOCX: DocxReader()
    }
    
    def __init__(self) -> None:
        """_summary_
        """
        pass
    
    def __get_reader_type_from_path(self, file_path: Union[str, Path]) -> ReaderType|None:
        file_type = Path(file_path).suffix
        if file_type.lower() == ".pdf":
            return ReaderType.PDF
        elif file_type.lower() == ".docx":
            return ReaderType.DOCX
        else:
            logger.warning(f"Unknown file type {file_type} found.")
            return None
        
    def __get_reader_from_type(self, reader_type:ReaderType) -> BaseReader:
        if reader_type in self.reader.keys():
            return self.reader.get(reader_type)
        else:
            raise Exception(f"Missing implementation for readertype: {reader_type}") 
    
    def read(self, file_path: Union[str, Path]) -> Document|None:
        """_summary_

        Args:
            file_path (Union[str, Path]): _description_

        Returns:
            Document|None: _description_
        """
        reader_type = self.__get_reader_type_from_path(file_path)
        if reader_type:
            reader = self.__get_reader_from_type(reader_type)
            return reader.read(file_path)          
        else:
            return None