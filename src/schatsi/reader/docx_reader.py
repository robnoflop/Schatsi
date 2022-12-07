from importlib.metadata import metadata
from pathlib import Path
from typing import Union
from weakref import ref
from schatsi.models.document import Document
from schatsi.reader.base_reader import BaseReader
from schatsi.reader.reader_type import ReaderType
from docx2python import docx2python


class DocxReader(BaseReader):
    """Reader impelementation to read Docx files.

    Args:
        BaseReader (_type_): The BaseReader.
    """

    type = ReaderType.DOCX

    def __init__(self) -> None:
        super().__init__()

    def read(self, file_path: Path) -> Document:
        """Reads the given Docx file an trys to extract alle metadata to completeat

        Args:
            file_path (Union[str, Path]): The file path to Docx file.

        Returns:
            Document: The document that was read.
        """

        doc = docx2python(file_path)
        out = doc.text

        return Document(
            filename=file_path.stem,
            raw_text=out,
            file_type=str(type),
            title=doc.metadata["title"],
            toc=doc.get_toc(),
            author=doc.metadata["author"],
            keywords=doc.metadata["keywords"],
        )
