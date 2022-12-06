import os
from pathlib import Path
from typing import List
import pandas as pd
from tqdm import tqdm

from schatsi.models.document import Document
from schatsi.models.ranking import Ranking
from . import BaseJob


class SingleJob(BaseJob):
    """_summary_

    Args:
        BaseJob (_type_): _description_
    """
    def __init__(
        self, input_path, output_path, functional_terms, negative_terms
    ) -> None:
        super().__init__(input_path, output_path, functional_terms, negative_terms)

    def process(self):
        """_summary_
        """
        for path, subdirs, files in os.walk(self.input_path):
            for filename in tqdm(files):
                file_path = Path(path) / filename
                self._process_file(file_path)

    def _process_file(self, file_path: Path):
        filename = file_path.stem
        doc: Document = self.file_reader.read(file_path)
        if doc:
            text: str
            references: str
            text, references = self._split_references_and_content(doc)
            terms_df: pd.DataFrame = self._create_terms(text)
            terms_df["filename"] = filename
            if terms_df is not None and not terms_df.empty:
                self._create_update_csv("schatsi_terms.csv", terms_df)
                rankings: List[Ranking] = self.ranker.rank(terms_df, [self.text_cleaner.stemmer.stem])
                self._create_update_csv(
                    "schatsi_ranking.csv", pd.DataFrame([x.dict() for x in rankings])
                )

            doc = self._enrich_metadata(
                doc,
                text,
                references,
            )

            self._create_update_csv("documents.csv", pd.DataFrame([doc.dict()]))
