
from importlib.metadata import metadata
from pathlib import Path
from typing import Union
from weakref import ref
from models.document import Document
from reader.base_reader import BaseReader
from reader.reader_type import ReaderType
import fitz


class PdfReader(BaseReader):
    
    type = ReaderType.PDF
    
    def __init__(self) -> None:
        super().__init__()
        
    def read(self, file_path: Union[str, Path]) -> Document:
        doc = fitz.open(file_path)
        out = ""
        for page in doc:
            text = page.get_text()
            out += text
        return Document(raw_text=out, 
                        file_type=str(type),
                        title=doc.metadata['title'], 
                        toc=doc.get_toc(),
                        author=doc.metadata['author'], 
                        abstract=None, 
                        keywords=doc.metadata['keywords'], 
                        content=None,
                        references= None)
        