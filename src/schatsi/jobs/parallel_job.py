import os
from pathlib import Path

import pandas as pd
from dask import compute, delayed
from distributed import Client
from schatsi.models.document import Document
from schatsi.models.ranking import Ranking
from tqdm import tqdm

from . import BaseJob


class ParallelJob(BaseJob):
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
        client = Client(threads_per_worker=1, n_workers=6)
        results = []
        for path, subdirs, files in os.walk(self.input_path):
            for filename in tqdm(files, desc="Create Dask delayed"):
                file_path = Path(path) / filename
                results.append(delayed(self._process_file)(file_path))

        results = compute(*results)

        for terms_df, rankings, doc in results:
            if terms_df is not None and not terms_df.empty:
                self._create_update_csv("schatsi_terms.csv", terms_df)
            if rankings:
                self._create_update_csv(
                    "schatsi_ranking.csv", pd.DataFrame([x.dict() for x in rankings])
                )
            if doc:
                self._create_update_csv("documents.csv", pd.DataFrame([doc.dict()]))

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
                ranking: Ranking = self.ranker.rank(terms_df)
            else:
                ranking = None

            doc = self._enrich_metadata(
                doc,
                text,
                references,
            )

        else:
            terms_df = None
            ranking = None

        return terms_df, ranking, doc
