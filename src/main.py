import os
from pathlib import Path
from typing import List, Tuple
from dask import compute, delayed
import pandas as pd
from models.document import Document
from models.ranking import Ranking
from processor.ngram_processor import NgramProcessor
from processor.ranker import Ranker
from processor.text_cleaner import TextCleaner
from reader.reader_facade import ReaderFacade
from variables import *
import nltk
from tqdm import tqdm
from nltk.corpus import stopwords
import collections
from dask.distributed import Client

nltk.download("punkt")

text_cleaner = TextCleaner()
stop_words = set(stopwords.words("english"))
file_reader = ReaderFacade()
ranker = Ranker(SCHATSI_FUNCTIONAL_TERMS)
ngram_porcessor = NgramProcessor()


def main():
    for path, subdirs, files in os.walk(SCHATSI_INPUT_FOLDER):
        for filename in tqdm(files):
            file_path = Path(path) / filename
            process_file(file_path)

def main_dask():
    client = Client(threads_per_worker=1, n_workers=6)
    results =  []
    for path, subdirs, files in os.walk(SCHATSI_INPUT_FOLDER):
        for filename in tqdm(files, desc="Create Dask delayed"):
            file_path = Path(path) / filename
            results.append(delayed(process_file_dask)(file_path))
    
    results = compute(*results)
        
    for terms_df, ranking, doc in results:
        if terms_df is not None and not terms_df.empty:
            create_update_csv("schatsi_terms.csv", terms_df)
        if ranking:
            create_update_csv("schatsi_ranking.csv", pd.DataFrame([ranking.dict()]))
        create_update_csv("documents.csv", pd.DataFrame([doc.dict()]))
        

def process_file_dask(file_path: Path):
    filename = file_path.stem
    doc: Document = file_reader.read(file_path)
    if doc:
        text: str
        references: str
        text, references = split_references_and_content(doc)
        terms_df: pd.DataFrame = create_terms(text)
        terms_df["filename"] = filename
        
        if terms_df is not None and not terms_df.empty:
            ranking: Ranking = ranker.rank(terms_df)
        else:
            ranking = None

        doc = enrich_metadata(
            doc,
            filename,
            text,
            references,
            True,
        )

    else:
        doc = enrich_metadata(doc, filename, None, None, False)
        terms_df = None
        ranking = None

    return terms_df, ranking, doc


def process_file(file_path: Path):
    filename = file_path.stem
    doc: Document = file_reader.read(file_path)
    if doc:
        text: str
        references: str
        text, references = split_references_and_content(doc)
        terms_df: pd.DataFrame = create_terms(text)
        terms_df["filename"] = filename
        if terms_df is not None and not terms_df.empty:
            create_update_csv("schatsi_terms.csv", terms_df)
            ranking: Ranking = ranker.rank(terms_df)
            create_update_csv("schatsi_ranking.csv", pd.DataFrame([ranking.dict()]))

        doc = enrich_metadata(
            doc,
            filename,
            text,
            references,
            True,
        )

    else:
        doc = enrich_metadata(doc, filename, None, None, False)

    create_update_csv("documents.csv", pd.DataFrame([doc.dict()]))


def enrich_metadata(
    doc: Document,
    filename: str,
    text: str,
    references: str,
    include: bool,
) -> Document:
    if text:
        word_count_text: int = len(nltk.word_tokenize(text))
    else:
        word_count_text = None

    if references:
        word_count_reference: int = len(nltk.word_tokenize(references))
    else:
        word_count_reference = None

    doc.filename = filename
    doc.include = include
    doc.word_count_raw_text = word_count_text
    doc.word_count_reference = word_count_reference
    
    return doc


def create_update_csv(filename: str, df: pd.DataFrame) -> None:
    path: Path = Path(SCHATSI_OUTPUT_FOLDER) / filename
    if not path.is_file():
        df.to_csv(path, index=False)
    else:
        df.to_csv(path, mode="a", header=False, index=False)


def split_references_and_content(doc: Document) -> tuple[str, str]:
    low_string: str = doc.raw_text.lower()

    try:
        last_time_reference: str = low_string.rindex("\nreference")
    except:
        return low_string, None

    low_string_without_references: str = low_string[0:last_time_reference]
    references: str = low_string[last_time_reference:]
    return low_string_without_references, references


def create_terms(text: str) -> pd.DataFrame:
    monogram: List[str] = text_cleaner.clean(text, True)
    mono_counts: collections.Counter = collections.Counter(monogram)
    bigram: List[str] = list(nltk.bigrams(monogram))
    bigram_counts: collections.Counter = collections.Counter(bigram)
    trigram: List[str] = list(nltk.trigrams(monogram))
    trigram_counts: collections.Counter = collections.Counter(trigram)

    joined_bigram: List[str] = [" ".join(x) for x in bigram_counts.keys()]
    joined_trigram: List[str] = [" ".join(x) for x in trigram_counts.keys()]

    output_terms: List[tuple[str, int]] = (
        list(zip(mono_counts.keys(), mono_counts.values()))
        + list(zip(joined_trigram, trigram_counts.values()))
        + list(zip(joined_bigram, bigram_counts.values()))
    )
    return pd.DataFrame(output_terms, columns=["term", "term count"])


if __name__ == "__main__":
    main_dask()
    
    