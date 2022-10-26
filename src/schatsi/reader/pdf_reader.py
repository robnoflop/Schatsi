
from importlib.metadata import metadata
from pathlib import Path
from typing import Union
from weakref import ref
from schatsi.models.document import Document
from schatsi.reader.base_reader import BaseReader
from schatsi.reader.reader_type import ReaderType
import fitz


class PdfReader(BaseReader):
    """Reader impelementation to read pdf files.

    Args:
        BaseReader (_type_): The BaseReader.
    """
    
    type = ReaderType.PDF
    
    def __init__(self) -> None:
        super().__init__()
        
    def read(self, file_path: Path) -> Document:
        """Reads the given pdf file an trys to extract alle metadata to completeat 

        Args:
            file_path (Union[str, Path]): The file path to pdf file.

        Returns:
            Document: The document that was read.
        """
        doc = fitz.open(file_path)
        out = ""
        for page in doc:
            text = page.get_text()
            out += text
        return Document(filename=file_path.stem,
                        raw_text=out, 
                        file_type=str(type),
                        title=doc.metadata['title'], 
                        toc=doc.get_toc(),
                        author=doc.metadata['author'], 
                        keywords=doc.metadata['keywords']
                        )
        