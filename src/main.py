import os
from typing import List
import pandas as pd
from models.document import Document
from processor.ngram_processor import NgramProcessor
from processor.ranker import Ranker
from processor.text_cleaner import TextCleaner
from reader.reader_facade import ReaderFacade
from variables import *
import nltk
from tqdm import tqdm
from nltk.corpus import stopwords
import collections


nltk.download("punkt")

text_cleaner = TextCleaner()
stop_words = set(stopwords.words("english"))
file_reader = ReaderFacade()
ranker = Ranker(SCHATSI_FUNCTIONAL_TERMS)
ngram_porcessor = NgramProcessor()


def main():
    for path, subdirs, files in os.walk(SCHATSI_INPUT_FOLDER):
        for filename in tqdm(files):
            file_path = os.path.join(path, filename)
            doc: Document = file_reader.read(file_path)
            if doc:
                print(doc.title)
                text, references = split_references_and_content(doc)
                terms_df = create_terms(text)
                terms_df["filename"] = filename
                if terms_df is not None and not terms_df.empty:
                    create_update_csv("schatsi_terms.csv", terms_df)
                    ranking = ranker.rank(terms_df)
                    ranking_df = pd.DataFrame([ranking])
                    create_update_csv("schatsi_ranking.csv", ranking_df)
                    
                word_count_text = len(nltk.word_tokenize(text))
                if references:
                    word_count_reference = len(nltk.word_tokenize(references))
                else:
                    references = None
                    word_count_reference = None

                paper_metadata = pd.DataFrame(
                    [
                        create_metadata(
                            doc,
                            filename,
                            text,
                            word_count_text,
                            references,
                            word_count_reference,
                            True,
                        )
                    ]
                )

            else:
                paper_metadata = pd.DataFrame(
                    [create_metadata(doc, filename, None, None, None, None, False)]
                )

            create_update_csv("paper_metadata.csv", paper_metadata)


def create_metadata(
    doc: Document,
    filename: str,
    text: str,
    word_count_text: int,
    references: str,
    word_count_reference: int,
    include: bool,
) -> None:
    return {
        "filename": filename,
        "file_type": doc.file_type if doc else None,
        "titel": doc.title if doc else None,
        "toc": doc.toc if doc else None,
        "text": text,
        "word_count_text": word_count_text,
        "references": references,
        "word_count_reference": word_count_reference,
        "include": include,
    }


def create_update_csv(filename, df):
    path = os.path.join(SCHATSI_OUTPUT_FOLDER, filename)
    if not os.path.isfile(path):
        df.to_csv(path, index=False)
    else:
        df.to_csv(path, mode="a", header=False, index=False)


def split_references_and_content(doc: Document):
    low_string = doc.raw_text.lower()

    try:
        last_time_reference = low_string.rindex("\nreference")
    except:
        return low_string, None

    low_string_without_references = low_string[0:last_time_reference]
    references = low_string[last_time_reference:]
    return low_string_without_references, references

def create_terms(text: str):
    monogram: List[str] = text_cleaner.clean(text, True)
    mono_counts = collections.Counter(monogram)
    bigram: List[str] = list(nltk.bigrams(monogram))
    bigram_counts = collections.Counter(bigram)
    trigram: List[str] = list(nltk.trigrams(monogram))
    trigram_counts = collections.Counter(trigram)

    joined_bigram = [" ".join(x) for x in bigram_counts.keys()]
    joined_trigram = [" ".join(x) for x in trigram_counts.keys()]

    output_terms = (
        list(zip(mono_counts.keys(), mono_counts.values()))
        + list(zip(joined_trigram, trigram_counts.values()))
        + list(zip(joined_bigram, bigram_counts.values()))
    )
    terms_df = pd.DataFrame(output_terms, columns=["term", "term count"])
    return terms_df

if __name__ == "__main__":
    main()
