# SCHATSI002: Frame around the whole Application

import os
import csv
import pdftotext
import time
import SCHATSI003  # import string_preparation, count_words, references, reference_data_cutting
import SCHATSI004  # import terms, bigrams, trigrams, term_filtering, ranking,...
import pandas


# Function to normalize the date and time, which is created by using the python module "time", according to the
# description in the Feature "SCHATSI002"
def time_analysis(timestamp):

    day = timestamp[8:10]
    month = timestamp[4:7]

    if month == "Jan":
        month = "01"
    elif month == "Feb":
        month = "02"
    elif month == "Mar":
        month = "03"
    elif month == "Apr":
        month = "04"
    elif month == "May":
        month = "05"
    elif month == "Jun":
        month = "06"
    elif month == "Jul":
        month = "07"
    elif month == "Aug":
        month = "08"
    elif month == "Sep":
        month = "09"
    elif month == "Oct":
        month = "10"
    elif month == "Nev":
        month = "11"
    elif month == "Dec":
        month = "12"

    year = timestamp[20:24]
    hour = timestamp[11:13]
    minute = timestamp[14:16]
    second = timestamp[17:19]
    # normalized String: DD.MM.YYYY HH:MM:SS
    time_string = day + "." + month + "." + year + " " + hour + ":" + minute + ":" + second
    return time_string


# Function for the calculation of the duration of the whole program. It takes two timestamps and calculates the
# duration in minutes (one timestamp at the beginning of the program and another at the end
def duration_calc(timestamp1_normalized, timestamp2_normalized):
    # normalized String: DD.MM.YYYY HH:MM:SS
    # duration is needed in minutes --> MM

    start_time = timestamp1_normalized[11:19]
    finish_time = timestamp2_normalized[11:19]

    start_hour = int(start_time[0:2])
    finish_hour = int(finish_time[0:2])
    start_minute = int(start_time[3:5])
    finish_minute = int(finish_time[3:5])
    start_second = int(start_time[6:8])
    finish_second = int(finish_time[6:8])

    # hour -> 60 minutes
    # normal case
    if finish_hour >= start_hour:
        hour = finish_hour - start_hour
    # special case: i.g. start: 23:55:24;   finish: 00:2:25
    elif finish_hour < start_hour and finish_minute < start_minute:
        hour = 0
    # special case: i.g. start: 23:55:24;   finish: 00:56:25
    else:
        hour = 1

    # minutes
    if finish_minute >= start_minute:
        minutes = hour*60 + (finish_minute - start_minute)
    else:
        minutes = hour*60 + (60-start_minute) + finish_minute

    if finish_minute > start_minute:
        seconds = abs(60 - start_second) + finish_second
    else:
        seconds = abs(finish_second - start_second)
    duration = str(minutes) + "min " + str(seconds) + "sec"
    return duration


"""
Start of the program:
1. First timestamp for the calculation of the runtime
2. One run of the whole programm, incl. SCHATSI002, SCHATSI003, SCHATSI004....
3. Second timestamp for the calculation of the runtime
4. Calculate the duration -> write the timestamps and the duration into the file "SCHATSI_runtime
"""

# Initialising all needed DataFrames, so that they are initialized global for all upcoming loops and functions
runtime_df = pandas.DataFrame(columns=['process', 'start processing', 'end processing', 'duration'])
included_df = pandas.DataFrame(columns=['filename', 'type', 'included', 'excluded'])
datacleansing_df = pandas.DataFrame(columns=['filename', 'type', 'total count'])
rawreferences_df = pandas.DataFrame(columns=['filename', 'raw reference string'])
terms_df = pandas.DataFrame(columns=['filename', 'term', 'term count'])
# used in the included loop, to save all extracted texts from the files, so that every file will be used just one time
# this file will be used to work with the extracted data at nearly all parts of the program
text_df = pandas.DataFrame(columns=['filename', 'text_only', 'reference text', 'type'])


# timestamp at the begin of the program and the normalized version which is written into "SCHATSI_runtime"
start = time.asctime()
start_normalized = time_analysis(start)
print("start time: ", start_normalized, "\n")

"""
Preparation of the Stopwords for use in SCHATSI004 functions - import from file "SCHATSI_stopwords.csv
"""
stopwords_list = []
# LOCAL FOR TESTING:
with open('SCHATSI_stopwords.csv') as stop:
# PATH FOR DOCKER:
# with open(r'/data/input/SCHATSI_stopwords.csv') as stop:
    csv_reader_object = csv.reader(stop)
    for row in csv_reader_object:
        stopwords_list.append(row[0])
# Save the stopwords from 'SCHATSI_stopwords.csv' into a set, bc its the faster data structure in comparision to lists
stopwords = set(stopwords_list)

"""
Loop for Including/Excluding
"""
# this counter is used to write the entries into the Dataframe at the bottom of the df
file_counter = 0
# Timestamp at the begin of SCHATSI_Included
start_included = time.asctime()
start_included_normalized = time_analysis(start_included)
# For all paths, subdirectories and files in the input-folder do:
# LOCAL PATH FOR TESTING: "r'/home/h/Github/Testpdfs'"
for path, subdirs, files in os.walk(r'/home/h/Downloads/Testpdfs'):
# PATH FOR DOCKER:
# for path, subdirs, files in os.walk(r'/data/input'):
    for filename in files:
        # print(filename)
        # with data path
        g = os.path.join(path, filename)

        # Filename in 'Schatsi_included.txt' schreiben, ohne den Dateipfad/ in csv-Datei
        f = os.path.join(filename)

        # try to read in a pdf and extract text from it
        try:
            with open(g, "rb") as pdffile:
                # create an object which is filled with a raw byte stream, which contains the text from the pdf
                pdf = pdftotext.PDF(pdffile)
                # force python to turn the byte stream into a string
                text = "\n\n".join(pdf)
        except:
            # if there is an exception or an error, they will be catched and the file wont be included in the next steps
            if f.endswith(".pdf") or f.endswith(".PDF"):
                datatype = "pdf"
            elif f.endswith(".txt") or f.endswith(".TXT"):
                datatype = "txt"
            elif f.endswith(".csv") or f.endswith(".CSV"):
                datatype = "csv"
            elif f.endswith(".docx") or f.endswith(".DOCX"):
                datatype = "docx"
            elif f.endswith(".odt") or f.endswith(".ODT"):
                datatype = "odt"
            else:
                datatype = "unknown datatype"
            zeile = [f, datatype, "__", "X"]
        else:
            # if it succeeds do:
            if f.endswith(".pdf") or f.endswith(".PDF"):
                datatype = "pdf"
                # All files that are successfully read in where the type is 'pdf' will be used in the next steps
                text_only, references = SCHATSI003.string_preparation(text)
                text_zeile = [f, text_only, references, datatype]
                text_df.loc[file_counter] = text_zeile

            elif f.endswith(".txt") or f.endswith(".TXT"):
                datatype = "txt"
            elif f.endswith(".csv") or f.endswith(".CSV"):
                datatype = "csv"
            elif f.endswith(".docx") or f.endswith(".DOCX"):
                datatype = "docx"
            elif f.endswith(".odt") or f.endswith(".ODT"):
                datatype = "odt"
            else:
                datatype = "unknown datatype"

            zeile = [f, datatype, "X", "__"]

        included_df.loc[file_counter] = zeile
        file_counter = file_counter + 1

# LOCAL PATH
included_df.to_csv('SCHATSI_included.csv', sep=';', index=False)
# DOCKER PATH
# included_df.to_csv(r'/data/output/SCHATSI_included.csv', sep=';', index=False)

# Second timestamp for SCHATSI_included: append an entry at the runtime dataframe
finish_included = time.asctime()
finish_included_normalized = time_analysis(finish_included)
duration_included = duration_calc(start_included_normalized, finish_included_normalized)
runtime_df = runtime_df.append({'process': 'SCHATSI_included', 'start processing': start_included_normalized,
                                'end processing': finish_included_normalized, 'duration': duration_included},
                               ignore_index=True)


"""
Loop for Data Cleansing
"""
# First timestamp of SCHATSI_datacleansing
start_datacleansing = time.asctime()
start_datacleansing_normalized = time_analysis(start_datacleansing)
for row in text_df.itertuples(index=True):

    # Calls the function of SCHATSI003: Count words
    total_num_words = SCHATSI003.count_words(row[2])
    # this dictionary will be appended to the df of data_cleansing in the next step -> 1 line for every file
    zeile_data_cleansing = {'filename': row[1], 'type': row[4], 'total count': total_num_words}
    datacleansing_df = datacleansing_df.append(zeile_data_cleansing, ignore_index=True)

# LOCAL PATH
datacleansing_df.to_csv('SCHATSI_data_cleansing.csv', sep=';', index=False)
# DOCKER PATH
# datacleansing_df.to_csv(r'/data/output/SCHATSI_data_cleansing.csv', sep=';', index=False)

# second timestamp for SCHATSI_data_cleansing; appending an entry to the runtime dataframe
finish_datacleansing = time.asctime()
finish_datacleansing_normalized = time_analysis(finish_datacleansing)
duration_datacleansing = duration_calc(start_datacleansing_normalized, finish_datacleansing_normalized)
runtime_df = runtime_df.append({'process': 'SCHATSI_datacleansing', 'start processing': start_datacleansing_normalized,
                                'end processing': finish_datacleansing_normalized, 'duration': duration_datacleansing},
                               ignore_index=True)

"""
Loop for term processing
"""
# first timestamp of SCHATSI_terms
start_terms = time.asctime()
start_terms_normalized = time_analysis(start_terms)
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
    term_list = []
    for i in range(0, len(mono_filtered)):
        zeile_terms = [row[1], mono_filtered[i], mono_number[i]]
        term_list.append(zeile_terms)
    for j in range(0, len(bigram_filtered)):
        bi = bigram_filtered[j][0] + " " + bigram_filtered[j][1]
        zeile_terms = [row[1], bi, bigram_number[j]]
        term_list.append(zeile_terms)
    for k in range(0, len(trigram_filtered)):
        tri = trigram_filtered[k][0] + " " + trigram_filtered[k][1] + " " + trigram_filtered[k][2]
        zeile_terms = [row[1], tri, trigram_number[k]]
        term_list.append(zeile_terms)
    # Transform the list of terms into a dataframe and append it to term_df
    terms_df = terms_df.append(
        pandas.DataFrame(term_list, columns=['filename', 'term', 'term count']), ignore_index=True)

# LOCAL PATH
terms_df.to_csv('SCHATSI_terms.csv', sep=';', index=False)
# DOCKER PATH
# terms_df.to_csv(r'/data/output/SCHATSI_terms.csv', sep=';', index=False)

# Second timestamp of SCHATSI_terms; appending an entry to runtime_df
finish_terms = time.asctime()
finish_terms_normalized = time_analysis(finish_terms)
duration_terms = duration_calc(start_terms_normalized, finish_terms_normalized)
runtime_df = runtime_df.append({'process': 'SCHATSI_terms', 'start processing': start_terms_normalized,
                                'end processing': finish_terms_normalized, 'duration': duration_terms},
                               ignore_index=True)

"""
Loop for Reference processing
"""
# first timestamp of SCHATSI_references
start_references = time.asctime()
start_references_normalized = time_analysis(start_references)
for row in text_df.itertuples(index=True):

    """
    reference_list = SCHATSI003.references(references)
    for element in reference_list:
    author, year, title = SCHATSI003.reference_data_cutting(element)
    refs_zeile = [filename, author, year, title]
    refs_file.writerow(refs_zeile)
    """
    # raw output of the reference string for further analysis; build a line containing the filename and the ref-text
    refs_raw_zeile = [[row[1], row[3]]]
    rawreferences_df = rawreferences_df.append(
        pandas.DataFrame(refs_raw_zeile, columns=['filename', 'raw reference string']), ignore_index=True)

# LOCAL PATH
rawreferences_df.to_csv('SCHATSI_references_raw.csv', sep=';', index=False)
# DOCKER PATH
# rawreferences_df.to_csv(r'/data/output/SCHATSI_references_raw.csv', sep=';', index=False)

# second timestamp for SCHATSI_references; appending an entry to runtime dataframe
finish_references = time.asctime()
finish_references_normalized = time_analysis(finish_references)
duration_references = duration_calc(start_references_normalized, finish_references_normalized)
runtime_df = runtime_df.append({'process': 'SCHATSI_references', 'start processing': start_references_normalized,
                                'end processing': finish_references_normalized, 'duration': duration_references},
                               ignore_index=True)


"""
Loop for the Ranking
"""
# first timestamp for SCHATSI_ranking
start_ranking = time.asctime()
start_ranking_normalized = time_analysis(start_ranking)
# call the function from SCHATSI004 to build the ranking, write it into a dataframe and write it into a csv-file
SCHATSI004.ranking()
# seconnd timestamp for SCHATSI_ranking; appending an entry to runtime_df
finish_ranking = time.asctime()
finish_ranking_normalized = time_analysis(finish_ranking)
duration_ranking = duration_calc(start_ranking_normalized, finish_ranking_normalized)
runtime_df = runtime_df.append(
    {'process': 'SCHATSI_ranking', 'start processing': start_ranking_normalized,
     'end processing': finish_ranking_normalized, 'duration': duration_ranking}, ignore_index=True)


# Calculate the runtime -> last step of the program
# second timestamp of the whole program
finish = time.asctime()
finish_normalized = time_analysis(finish)
print("finish time: ", finish_normalized, "\n")
# calculation of the duration
duration_program = duration_calc(start_normalized, finish_normalized)
runtime_df = runtime_df.append(
    {'process': 'whole Program', 'start processing': start_normalized, 'end processing': finish_normalized,
     'duration': duration_program}, ignore_index=True)

# write the runtime dataframe into a csv-File
# LOCAL PATH
runtime_df.to_csv('SCHATSI_runtime.csv', sep=';', index=False)
# DOCKER PATH
# merged_df.to_csv('/data/output/SCHATSI_ranking.csv', sep=';', index=False)
