from abc import ABC, abstractmethod
from typing import Union
from pathlib import Path
    
from schatsi.models.document import Document

from schatsi.reader.reader_type import ReaderType


class BaseReader(ABC):
    """Base class that defines a FileReader. A FileReader is used to read, decode and format text on the file to 

    Args:
        ABC (_type_): _description_
    """
    
    def __init__(self) -> None:
        super().__init__()
        
    
    @property
    @abstractmethod
    def type(self) -> ReaderType:
        """The filetype the reader is implemented for.

        Returns:
            ReaderType: The type of the Reader.
        """
        pass
    
        
    @abstractmethod
    def read(self, file_path: Union[str, Path]) -> Document:
        """
            Reads the file with the given file. 

        Args:
            file_path (Union[str, Path]): _description_

        Returns:
            Document: _description_
        """
        pass