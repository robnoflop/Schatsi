import os
import io
import csv
import pdftotext
import pandas as pd
from datetime import datetime
import SCHATSI003  # import string_preparation, count_words, references, reference_data_cutting
import SCHATSI004  # import terms, bigrams, trigrams, term_filtering,....
from variables import *
import shutil


"""
###############################################
How Does SCHA.T.S.I work? What does SCHATSI do?
###############################################

START

CREATE python lists for every output-file
READ stopwords FROM stopwords.csv
READ functional terms FROM functional_terms.csv

LOOP
    OPEN a file in the Input-Folder 
    CHECK what's the datatype of the file
    IF 
        (datatype IS pdf) 
    THEN 
        EXTRACT whole text from the file
    WRITE filename, Datatype and if text could be extracted or not in an entry in a LIST
    WRITE filename, text, reference text and datatype into a LIST for further working

LOOP over the text list
    COUNT all words in the text of a file 
    WRITE filename, datatype, total number of words in a LIST
    
LOOP over the text list
    IF
        (new word found)
    THEN 
        CREATE a pairwise entry of the word and a counter AND INCREASE counter by 1
    IF
        (already known word found)
    THEN 
        INCREASE counter by 1
    WRITE entries into monogram list
    
LOOP over the monogram list
    TAKE a entry
    TAKE next entry
    CONTATE both entrys 
    IF 
        (already Known)
    THEN 
        INCREASE counter by 1
    ELSE
        WRITE result into bigram list AND CREATE a counter set to 1

LOOP over the monogram list
    TAKE a entry
    TAKE next entry
    TAKE next entry
    CONTATE all three entrys 
    IF 
        (already Known)
    THEN 
        INCREASE counter by 1
    ELSE
        WRITE result into trigram list AND CREATE a counter set to 1

FILTER entries from bigrams and trigrams which doesn't make any sense 
WRITE monograms, bigrams and trigrams in a term list like {filename, monogram/bigram/trigram, counter}
    
LOOP for every file, whose text could be extracted
    LOOP over the term list
        IF
            (term == functional term)
        THEN
            found_functional_terms = found_functional_terms + counter
    SCORE = DEVIDE found_functional_term BY total_number_of_words_in_text
    WRITE {filename, found_functional_terms, total_number_of_words_in_text, Score} in ranking list

TURN every list into Python pandas dataframe 

LOOP for all pandas dataframes 
    WRITE dataframe into a CSV-file

END
"""


def main():
    # Runtime
    # open file for runtime

    # LOCAL PATH FOR TESTING:
    # runtime = open("SCHATSI_runtime.csv", 'w', newline='')
    # PATH FOR DOCKER:
    # runtime = open(SCHATSI_RUNTIME, 'w', newline='')
    # runtime_file = csv.writer(runtime, delimiter=';', quoting=csv.QUOTE_MINIMAL)
    # writing a headline into the file
    # kopfzeile_runtime = ["start processing", "end processing", "duration (minutes)"]
    # runtime_file.writerow(kopfzeile_runtime)

    # timestamp at the begin of the program and the normalized version which is written into "SCHATSI_runtime"
    start = datetime.now()
    start_total = start
    print("SCHA.T.S.I Data Cleanser - Version1.4.2")
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
    Preparation of the Stopwords for use in SCHATSI004 functions - import from file "stopwords.csv"
    """
    stopwords_list = []
    with open(SCHATSI_STOPWORDS) as stop:
        csv_reader_object = csv.reader(stop)
        for row in csv_reader_object:
            stopwords_list.append(row[0])
        print("\nstopwords found")
    stopwords = set(stopwords_list)

    print("done")

    print("Processing files for run:")
    # This block contains all functions which for SCHATSI002 and SCHATSI003.002 -> Included files with meta data
    for path, subdirs, files in os.walk(SCHATSI_INPUT_FOLDER):
        for filename in files:
            print(filename)

            # with data path
            g = os.path.join(path, filename)

            # write Filename in 'Schatsi_included.txt' without data path
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

            """
            the outputfile will get a layout like this:
            
            filename | type | included | excluded
            --------------------------------------
            abc.pdf  | pdf  |     X    |    __        <-- The text of this document could be extracted without any problems
            err.pdf  | pdf  |    __    |     X        <-- There was a problem and the document text could not be extracted,
            ...                                           the files wont be included in the next steps 
            ...
            """

    # This DataFrame  is used as a working dataframe, it contains the filename, datatype, raw text and raw references
    text_df = pd.DataFrame(text_array, columns=['filename', 'text_only', 'reference text', 'type'])
    finish = datetime.now()
    duration_program = (finish - start).seconds / 60
    runtime.append(['SCHATSI_included', start.strftime(datetime_format), finish.strftime(datetime_format), duration_program])
    start = datetime.now()

    # This block contains all functions of SCHATSI003.001 -> Counting total number of words
    for row in text_df.itertuples(index=True):
        # Calls the function of SCHATSI003: Count words
        total_num_words = SCHATSI003.count_words(row[2])
        # this dictionary will be appended to the df of data_cleansing in the next step -> 1 line for every file
        zeile_data_cleansing = {'filename': row[1], 'type': row[4], 'total count': total_num_words}
        output_data_cleansing.append(zeile_data_cleansing)

    datacleansing_df = pd.DataFrame(output_data_cleansing, columns=["filename", "type", "total count"])
    finish = datetime.now()
    duration_program = (finish - start).seconds / 60
    runtime.append(['SCHATSI_datacleansing', start.strftime(datetime_format), finish.strftime(datetime_format), duration_program])
    start = datetime.now()

    # This block contains all function of SCHATSI004.001 -> Counting functional terms
    for row in text_df.itertuples(index=True):
        # call SCHATSI004: Filtering the expressions from the text and rank the Papers at the Base of the
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

    # This block contains all function calls of SCHATSI003.003 -> Extracting Reference Data
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

    # This block contains all function calls of SCHATSI004.002 -> Create a Ranking of the the Files
    terms_df = pd.DataFrame(output_terms, columns=["filename", "term", "term count"])

    """
    try:
        ranking_df = SCHATSI004.ranking(functional_terms, terms_df)
    except:
        ranking_df = pd.DataFrame(columns=["X", "filename", "sum_functional_terms", "sum_terms", "result"])

    
    duration_program = (finish - start).seconds / 60
    runtime.append(['SCHATSI_ranking', start.strftime(datetime_format), finish.strftime(datetime_format), duration_program])
    """


    # Creating the dataframes, which will be saved as .csv-Files
    print("Saving output files...", end="", flush=True)
    outputs = [
        ['schatsi_data_cleansing.csv', datacleansing_df],
        ['schatsi_references.csv', pd.DataFrame(output_references, columns=['filename', 'raw reference string'])],
        ['schatsi_terms.csv', terms_df],
        # ['schatsi_ranking.csv', ranking_df],
        ['schatsi_runtime.csv', pd.DataFrame(runtime, columns=['process', 'start processing', 'end processing', 'duration'])],
        ['schatsi_included.csv', pd.DataFrame(output_included, columns=["filename", "type", "included", "excluded"])]
    ]
    # Creating the output-files
    for output in outputs:
        output[1].to_csv(r"{}/{}".format(SCHATSI_OUTPUT_FOLDER, output[0]), mode="wb", encoding="utf-8", sep=';', index=False)

    # Move functional_terms.csv and negative_terms.csv into the output-folder, required for the SCHATSI_RANKER
    shutil.move(SCHATSI_FUNCTIONAL_TERMS, os.path.join(SCHATSI_OUTPUT_FOLDER, 'functional_terms.csv'))
    shutil.move(SCHATSI_NEGATIVE_TERMS, os.path.join(SCHATSI_OUTPUT_FOLDER, 'negative_terms.csv'))

    finish = datetime.now()
    duration_program = (finish - start_total).seconds / 60
    runtime.append(['whole Program', start.strftime(datetime_format), finish.strftime(datetime_format), duration_program])

    print("done")


if __name__ == "__main__":
    main()
