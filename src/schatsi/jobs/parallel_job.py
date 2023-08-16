import os
from pathlib import Path
import pandas as pd
from dask import compute, delayed
from distributed import Client
from tqdm import tqdm

from schatsi.models.document import Document
from schatsi.models.ranking import Ranking

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
        """_summary_"""
        self._setup_dask_client()
        results = self._process_files_parallel()
        self._process_results(results)


    def _setup_dask_client(self):
        """_summary_"""
        client = Client(threads_per_worker=1, n_workers=6)
        return client
    
    def _process_files_parallel(self):
        results = []
        for path, subdirs, files in os.walk(self.input_path):
            for filename in tqdm(files, desc="Create Dask delayed"):
                file_path = Path(path) / filename
                results.append(delayed(self._process_file)(file_path))
        results = compute(*results)
        return results
    
    def _process_file(self, file_path: Path):
        filename = file_path.stem
        doc, text, references = self._read_document(file_path)
        terms_df, ranking, doc = self._process_document(doc, text, references, filename)
        return terms_df, ranking, doc
        
    def _read_document(self, file_path: Path):
        doc = self.file_reader.read(file_path)
        if doc:
            text: str
            references: str
            text, references = self._split_references_and_content(doc)
            return doc, text, references
        return None, None, None

    def _process_document(self, doc, text, references, filename):
        if doc:
            terms_df = self._create_terms(text)
            terms_df["filename"] = filename

            ranking: Ranking = self.ranker.rank(terms_df) if terms_df is not None and not terms_df.empty else None
            
            enriched_doc = self._enrich_metadata(doc, text, references)
            return terms_df, ranking, enriched_doc
        return None, None, None
    
    def _process_results(self, results):
        
        for terms_df, ranking, doc in results:
            if terms_df is not None and not terms_df.empty:
                self._create_update_csv("schatsi_terms.csv", terms_df)
            if ranking is not None:
                self._create_update_csv(
                    "schatsi_ranking.csv", pd.DataFrame([x.dict() for x in ranking])
                )
            if doc is not None:
                self._create_update_csv("documents.csv", pd.DataFrame([doc.dict()]))