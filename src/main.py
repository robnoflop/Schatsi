import os
import csv
from pathlib import Path
from typing import List, Union
import fitz
import pandas as pd
import SCHATSI003
import SCHATSI004
from processor.text_cleaner import TextCleaner
from reader.reader_facade import ReaderFacade
from variables import *
import shutil
from loguru import logger
import nltk
from execution_logger import ExcutionLogger
from tqdm import tqdm
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

nltk.download("punkt")

file_reader = ReaderFacade()

def main():
    programm_execution_logger = ExcutionLogger()
    programm_execution_logger.start()
    logger.info("SCHA.T.S.I Data Cleanser - Version1.4.2")
    programm_execution_logger.log_start()

    output_data_cleansing = []
    output_references = []
    output_terms = []

    execution_logger = ExcutionLogger()
    execution_logger.start()
    logger.info("Processing files for run:")
    text_df, output_included = process_input()
    execution_logger.log_end("SCHATSI_included")

    execution_logger = ExcutionLogger()
    execution_logger.start()
    for row in text_df.itertuples(index=True):
        total_num_words = SCHATSI003.count_words(row[2])
        zeile_data_cleansing = {
            "filename": row[1],
            "type": row[4],
            "total count": total_num_words,
        }
        output_data_cleansing.append(zeile_data_cleansing)

    datacleansing_df = pd.DataFrame(
        output_data_cleansing, columns=["filename", "type", "total count"]
    )
    execution_logger.log_end("SCHATSI_datacleansing")

    execution_logger = ExcutionLogger()
    execution_logger.start()
    stop_words = set(stopwords.words("english"))
    ps = PorterStemmer()
    for row in tqdm(text_df.itertuples(index=True)):
        monogram = nltk.word_tokenize(row[2])
        monogram = [word.lower() for word in monogram if word.isalpha()]
        monogram = [w for w in monogram if not w.lower() in stop_words]
        monogram = [ps.stem(w) for w in monogram]
        mono_filtered, mono_number = SCHATSI004.term_filtering(monogram)

        bigram = list(nltk.bigrams(monogram))
        bigram_filtered, bigram_number = SCHATSI004.bigram_filtering(bigram)

        trigram = list(nltk.trigrams(monogram))
        trigram_filtered, trigram_number = SCHATSI004.trigram_filtering(trigram)

        filename_as_list = [row[1]] * len(mono_filtered)
        output_terms = output_terms + list(
            zip(filename_as_list, mono_filtered, mono_number)
        )

        joined_bigram = [" ".join(x) for x in bigram_filtered]
        output_terms = output_terms + list(
            zip(filename_as_list, joined_bigram, bigram_number)
        )

        joined_trigram = [" ".join(x) for x in trigram_filtered]
        output_terms = output_terms + list(
            zip(filename_as_list, joined_trigram, trigram_number)
        )

    execution_logger.log_end("SCHATSI_terms")

    execution_logger = ExcutionLogger()
    execution_logger.start()
    for row in text_df.itertuples(index=True):
        refs_raw_zeile = [row[1], row[3]]
        output_references.append(refs_raw_zeile)
    execution_logger.log_end("SCHATSI_references")

    execution_logger = ExcutionLogger()
    execution_logger.start()
    terms_df = pd.DataFrame(output_terms, columns=["filename", "term", "term count"])
    functional_terms = pd.read_csv(SCHATSI_FUNCTIONAL_TERMS, sep=";")
    try:
        ranking_df = SCHATSI004.ranking(functional_terms, terms_df)
    except Exception as e:
        ranking_df = pd.DataFrame(
            columns=["X", "filename", "sum_functional_terms", "sum_terms", "result"]
        )
        logger.warning(str(e))
    execution_logger.log_end("SCHATSI_ranking")

    execution_logger = ExcutionLogger()
    execution_logger.start()
    terms_df = pd.DataFrame(output_terms, columns=["filename", "term", "term count"])
    logger.info("Saving output files...", end="", flush=True)
    outputs = [
        ["schatsi_data_cleansing.csv", datacleansing_df],
        [
            "schatsi_references.csv",
            pd.DataFrame(
                output_references, columns=["filename", "raw reference string"]
            ),
        ],
        ["schatsi_ranking.csv", ranking_df],
        ["schatsi_terms.csv", terms_df],
        [
            "schatsi_included.csv",
            pd.DataFrame(
                output_included, columns=["filename", "type", "included", "excluded"]
            ),
        ],
    ]
    for output in outputs:
        output[1].to_csv(
            r"{}/{}".format(SCHATSI_OUTPUT_FOLDER, output[0]),
            mode="wb",
            encoding="utf-8",
            sep=";",
            index=False,
        )

    shutil.copy(
        SCHATSI_FUNCTIONAL_TERMS,
        os.path.join(SCHATSI_OUTPUT_FOLDER, "functional_terms.csv"),
    )
    shutil.copy(
        SCHATSI_NEGATIVE_TERMS,
        os.path.join(SCHATSI_OUTPUT_FOLDER, "negative_terms.csv"),
    )

    programm_execution_logger.log_end("whole Program")
    logger.info("done")


text_cleaner = TextCleaner()

def process_file(file_path: Union(str,Path)):
    text: str = file_reader.read(file_path)
    monogram : List[str] = text_cleaner.clean(text, True)
    bigram: List[str] = list(nltk.bigrams(monogram))
    bigram_filtered, bigram_number = SCHATSI004.bigram_filtering(bigram)
    trigram: List[str] = list(nltk.trigrams(monogram))
    trigram_filtered, trigram_number = SCHATSI004.trigram_filtering(trigram)


def process_input():
    results = []
    output_included = []

    for path, subdirs, files in os.walk(SCHATSI_INPUT_FOLDER):
        for filename in files:
            file_path = os.path.join(path, filename)
            try:
                text = file_reader.read(file_path)
            except Exception as e:
                datatype = "unreadable file"
                row = [filename, datatype, "__", "X"]
                logger.warning(str(e))

            else:
                filename_lower = filename.lower()
                if filename_lower.endswith(".pdf"):
                    datatype = "pdf"
                    # All files that are successfully read in where the type is 'pdf' will be used in the next steps
                    text, references = SCHATSI003.split_references_and_content(text)
                    results.append([filename, text, references, datatype])

                row = [filename, datatype, "X", "__"]

            output_included.append(row)

    text_df = pd.DataFrame(
        results, columns=["filename", "text_only", "reference text", "type"]
    )
    return text_df, output_included


if __name__ == "__main__":
    main()
