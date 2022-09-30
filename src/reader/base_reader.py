from abc import ABC, abstractmethod
from typing import Union
from pathlib import Path

from reader.reader_type import ReaderType


class BaseReader(ABC):
    
    def __init__(self) -> None:
        super().__init__()
        
    
    @property
    @abstractmethod
    def type(self) -> ReaderType:
        pass
    
        
    @abstractmethod
    def read(self, file_path: Union[str, Path]) -> str:
        pass