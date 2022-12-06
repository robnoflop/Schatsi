import collections
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

import nltk
import pandas as pd
from nltk.corpus import stopwords
from schatsi.models.document import Document
from schatsi.processor.ngram_processor import NgramProcessor
from schatsi.processor.ranker import Ranker
from schatsi.processor.text_cleaner import TextCleaner
from schatsi.reader.reader_facade import ReaderFacade


class BaseJob(ABC):
    """_summary_

    Args:
        ABC (_type_): _description_
    """
    def __init__(
        self, input_path, output_path, functional_terms, negative_terms
    ) -> None:
        """_summary_

        Args:
            input_path (_type_): _description_
            output_path (_type_): _description_
            functional_terms (_type_): _description_
            negative_terms (_type_): _description_
        """
        self.input_path = input_path
        self.output_path = output_path
        self.negative_terms = negative_terms
        self.text_cleaner = TextCleaner()
        self.stop_words = set(stopwords.words("english"))
        self.file_reader = ReaderFacade()
        self.ranker = Ranker(functional_terms)
        self.ngram_porcessor = NgramProcessor()
        
    @abstractmethod
    def process(self):
        """_summary_
        """
        pass

    def _enrich_metadata(
        self,
        doc: Document,
        text: str,
        references: str,
    ) -> Document:
        if text:
            word_count_text: int = len(nltk.word_tokenize(text))
        else:
            word_count_text = None

        if references:
            word_count_reference: int = len(nltk.word_tokenize(references))
        else:
            word_count_reference = None

        doc.word_count_raw_text = word_count_text
        doc.word_count_reference = word_count_reference

        return doc

    def _create_update_csv(self, filename: str, df: pd.DataFrame) -> None:
        path: Path = Path(self.output_path) / filename
        if not path.is_file():
            df.to_csv(path, index=False)
        else:
            df.to_csv(path, mode="a", header=False, index=False)

    def _split_references_and_content(self, doc: Document) -> tuple[str, str]:
        low_string: str = doc.raw_text.lower()

        try:
            last_time_reference: str = low_string.rindex("\nreference")
        except:
            return low_string, None

        low_string_without_references: str = low_string[0:last_time_reference]
        references: str = low_string[last_time_reference:]
        return low_string_without_references, references

    def _create_terms(self, text: str) -> pd.DataFrame:
        monogram: List[str] = self.text_cleaner.clean(text, True)
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
