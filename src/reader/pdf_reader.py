
from pathlib import Path
from typing import Union
from reader.base_reader import BaseReader
from reader.reader_type import ReaderType
import fitz



class PdfReader(BaseReader):
    
    type = ReaderType.PDF
    
    def __init__(self) -> None:
        super().__init__()
        
    def read(self, file_path: Union[str, Path]) -> str:
        doc = fitz.open(file_path)
        out = ""
        for page in doc:
            text = page.get_text()
            out += text
        return out
        