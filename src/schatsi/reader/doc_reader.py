
from importlib.metadata import metadata
from pathlib import Path
from typing import Union
from weakref import ref
from schatsi.models.document import Document
from schatsi.reader.base_reader import BaseReader
from schatsi.reader.reader_type import ReaderType
from doc2python import reader


class DocReader(BaseReader):
    """Reader impelementation to read .doc files.

    Args:
        BaseReader (_type_): The BaseReader.
    """
    
    type = ReaderType.PDF
    
    def __init__(self) -> None:
        super().__init__()
        
    def read(self, file_path: Path) -> Document:
        """Reads the given .doc file an tries to extract all text.

        Args:
            file_path (Union[str, Path]): The file path to .doc file.

        Returns:
            Document: The document that was read.
        """
        out = reader.toString(file_path)
        return Document(filename=file_path.stem,
                        raw_text=out, 
                        file_type=str(type),
                        )
        