import os
import io
import csv
import pdftotext
import pandas as pd
from datetime import datetime
import SCHATSI003  # import string_preparation, count_words, references, reference_data_cutting
import SCHATSI004  # import terms, bigrams, trigrams, term_filtering,....
from variables import *


"""
Start of the program:
1. First timestamp for the calculation of the runtime
2. One run of the whole programm, incl. SCHATSI002, SCHATSI003, SCHATSI004....
3. Second timestamp for the calculation of the runtime
4. Calculate the duration -> write the timestamps and the duration into the file "SCHATSI_runtime
"""


def main():
    # Runtime
    # open file for runtime

    # LOCAL PATH FOR TESTING:
    # runtime = open("SCHATSI_runtime.csv", 'w', newline='')
    # PATH FOR DOCKER:
    #runtime = open(SCHATSI_RUNTIME, 'w', newline='')
    #runtime_file = csv.writer(runtime, delimiter=';', quoting=csv.QUOTE_MINIMAL)
    # writing a headline into the file
    #kopfzeile_runtime = ["start processing", "end processing", "duration (minutes)"]
    #runtime_file.writerow(kopfzeile_runtime)

    # timestamp at the begin of the program and the normalized version which is written into "SCHATSI_runtime"
    start = datetime.now()
    start_total = start
    print("Execution started at", start.isoformat())

    output_included = []
    output_data_cleansing = []
    output_references = []
    output_terms = []
    runtime = []
    text_array = []
    datetime_format = "%m/%d/%Y %H:%M:%S"

    print("Fetching parameters...", end="", flush=True)

    """
    Preparation of the Stopwords for use in SCHATSI004 functions - import from file "SCHATSI_stopwords.csv
    """
    stopwords_list = []
    with open(SCHATSI_STOPWORDS) as stop:
        csv_reader_object = csv.reader(stop)
        for row in csv_reader_object:
            stopwords_list.append(row[0])
    stopwords = set(stopwords_list)

    try:
        functional_terms = pd.read_csv(SCHATSI_FUNCTIONAL_TERMS, sep=';')
    except:
        pass

    print("done")
    print("Processing files for run:")

    for path, subdirs, files in os.walk(SCHATSI_INPUT_FOLDER):
        for filename in files:
            print(filename)

            # with data path
            g = os.path.join(path, filename)

            # Filename in 'Schatsi_included.txt' schreiben, ohne den Dateipfad/ in csv-Datei
            f = os.path.join(filename)

            try:
                with open(g, "rb") as pdffile:
                    # create an object which is filled with a raw byte stream, which contains the text from the pdf
                    pdf = pdftotext.PDF(pdffile)
                    # force python to turn the byte stream into a string
                    text = "\n\n".join(pdf)
            except:
                if filename.endswith(".pdf") or filename.endswith(".PDF"):
                    datatype = "pdf"
                elif filename.endswith(".txt") or filename.endswith(".TXT"):
                    datatype = "txt"
                elif filename.endswith(".csv") or filename.endswith(".CSV"):
                    datatype = "csv"
                elif filename.endswith(".docx") or filename.endswith(".DOCX"):
                    datatype = "docx"
                elif filename.endswith(".odt") or filename.endswith(".ODT"):
                    datatype = "odt"
                else:
                    datatype = "unknown datatype"
                zeile = [filename, datatype, "__", "X"]

            else:
                if filename.endswith(".pdf") or filename.endswith(".PDF"):
                    datatype = "pdf"
                    # All files that are successfully read in where the type is 'pdf' will be used in the next steps
                    text_only, references = SCHATSI003.string_preparation(text)
                    text_zeile = [f, text_only, references, datatype]
                    text_array.append(text_zeile)

                elif filename.endswith(".txt") or filename.endswith(".TXT"):
                    datatype = "txt"
                elif filename.endswith(".csv") or filename.endswith(".CSV"):
                    datatype = "csv"
                elif filename.endswith(".docx") or filename.endswith(".DOCX"):
                    datatype = "docx"
                elif filename.endswith(".odt") or filename.endswith(".ODT"):
                    datatype = "odt"
                else:
                    datatype = "unknown datatype"

                zeile = [f, datatype, "X", "__"]

            output_included.append(zeile)

            # the outputfile will get a layout like this
            """
            filename | type | included | excluded
            --------------------------------------
            abc.pdf  | pdf  |     X    |    __        <-- The text of this document could be extracted without any problems
            err.pdf  | pdf  |    __    |     X        <-- There was a problem and the document text could not be extracted,
            ...                                           the files wont be included in the next steps 
            ...
            """
    
    text_df = pd.DataFrame(text_array, columns=['filename', 'text_only', 'reference text', 'type'])


    finish = datetime.now()
    duration_program = (finish - start).seconds / 60
    runtime.append(['SCHATSI_included', start.strftime(datetime_format), finish.strftime(datetime_format), duration_program])
    start = datetime.now()

    for row in text_df.itertuples(index=True):
        # Calls the function of SCHATSI003: Count words
        total_num_words = SCHATSI003.count_words(row[2])
        # this dictionary will be appended to the df of data_cleansing in the next step -> 1 line for every file
        zeile_data_cleansing = {'filename': row[1], 'type': row[4], 'total count': total_num_words}
        output_data_cleansing.append(zeile_data_cleansing)

    finish = datetime.now()
    duration_program = (finish - start).seconds / 60
    runtime.append(['SCHATSI_datacleansing', start.strftime(datetime_format), finish.strftime(datetime_format), duration_program])
    start = datetime.now()

    for row in text_df.itertuples(index=True):
        # Aufruf SCHATSI004: Filtering the expressions from the text and rank the Papers at the Base of the
        # functional terms given by the User
        monogram = SCHATSI004.terms(row[2])
        bigram = SCHATSI004.bigrams(monogram)
        trigram = SCHATSI004.trigrams(monogram)
        # filter the terms, bigrams and trigrams, to cut of unuseful filling words; and count the number of each expression
        mono_filtered, mono_number = SCHATSI004.term_filtering(monogram, stopwords)
        bigram_filtered, bigram_number = SCHATSI004.bigram_filtering(bigram, stopwords)
        trigram_filtered, trigram_number = SCHATSI004.trigram_filtering(trigram, stopwords)
        # Result: 2 lists each: one with the filtered terms, the other with the counts of the terms
        # Writing in "SCHATSI_terms.csv"
        i, j, k = 0, 0, 0
        for i in range(0, len(mono_filtered)):
            zeile_terms = [row[1], mono_filtered[i], mono_number[i]]
            output_terms.append(zeile_terms)
        for j in range(0, len(bigram_filtered)):
            bi = bigram_filtered[j][0] + " " + bigram_filtered[j][1]
            zeile_terms = [row[1], bi, bigram_number[j]]
            output_terms.append(zeile_terms)
        for k in range(0, len(trigram_filtered)):
            tri = trigram_filtered[k][0] + " " + trigram_filtered[k][1] + " " + trigram_filtered[k][2]
            zeile_terms = [row[1], tri, trigram_number[k]]
            output_terms.append(zeile_terms)
    
    finish = datetime.now()
    duration_program = (finish - start).seconds / 60
    runtime.append(['SCHATSI_terms', start.strftime(datetime_format), finish.strftime(datetime_format), duration_program])
    start = datetime.now()

    for row in text_df.itertuples(index=True):
        """
        reference_list = SCHATSI003.references(references)
        for element in reference_list:
        author, year, title = SCHATSI003.reference_data_cutting(element)
        refs_zeile = [filename, author, year, title]
        refs_file.writerow(refs_zeile)
        """
        # raw output of the reference string for further analysis; build a line containing the filename and the ref-text
        refs_raw_zeile = [row[1], row[3]]
        output_references.append(refs_raw_zeile)

    finish = datetime.now()
    duration_program = (finish - start).seconds / 60
    runtime.append(['SCHATSI_references', start.strftime(datetime_format), finish.strftime(datetime_format), duration_program])
    start = datetime.now()

    terms_df = pd.DataFrame(output_terms, columns=["filename", "term", "term count"])

    try:
        ranking_df = SCHATSI004.ranking(functional_terms, terms_df)
    except:
        ranking_df = pd.DataFrame(columns=["X","filename","sum_functional_terms","sum_terms","result"])
		
    finish = datetime.now()
    duration_program = (finish - start).seconds / 60
    runtime.append(['SCHATSI_ranking', start.strftime(datetime_format), finish.strftime(datetime_format), duration_program])
    duration_program = (finish - start_total).seconds / 60
    runtime.append(['whole Program', start.strftime(datetime_format), finish.strftime(datetime_format), duration_program])

    print("Saving output files...", end="", flush=True)

    outputs = [
        ['schatsi_included.csv', pd.DataFrame(output_included, columns=["filename", "type", "included", "excluded"])],
        ['schatsi_data_cleansing.csv', pd.DataFrame(output_data_cleansing, columns=["filename", "type", "Total Count"])],
        ['schatsi_references.csv', pd.DataFrame(output_references, columns=['filename', 'raw reference string'])],
        ['schatsi_terms.csv', terms_df],
        ['schatsi_ranking.csv', ranking_df],
        ['schatsi_runtime.csv', pd.DataFrame(runtime, columns=['process', 'start processing', 'end processing', 'duration'])]
    ]

    for output in outputs:
        output[1].to_csv(r"{}/{}".format(SCHATSI_OUTPUT_FOLDER, output[0]), mode="wb", encoding="utf-8", sep=';', index=False)

    print("done")


if __name__ == "__main__":
    main()
