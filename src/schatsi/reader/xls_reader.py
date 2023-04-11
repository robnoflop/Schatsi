import pandas as pd
from pathlib import Path
from schatsi.models.document import Document
from schatsi.reader.base_reader import BaseReader
from schatsi.reader.reader_type import ReaderType


class XlsReader(BaseReader):
    """Reader impelementation to read Xls files.

    Args:
        BaseReader (_type_): The BaseReader.
    """

    type = ReaderType.XLS

    def __init__(self) -> None:
        super().__init__()

    def read(self, file_path: Path) -> Document:
        """Reads the given Xls file an tries to extract all metadata to complete it.

        Args:
            file_path (Union[str, Path]): The file path to Xls file.

        Returns:
            Document: The document that was read.
        """

        table_text = pd.read_excel(file_path).to_string(na_rep="")
        clean_text = " ".join(table_text.split())

        return Document(
            filename=file_path.stem,
            raw_text=clean_text,
            file_type=str(type)
        )