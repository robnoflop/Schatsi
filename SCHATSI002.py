# SCHATSI002: Frame around the whole Application

import os
import csv
import pdftotext
import time
import SCHATSI003  # import string_preparation, count_words, references, reference_data_cutting
import SCHATSI004  # import terms, bigrams, trigrams, term_filtering, ranking,...


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
    print("Timestring: " + time_string + "\n")
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

    # hour -> 60 minutes + minutes + 1 minute, if there are more than 30 seconds left
    duration = (finish_hour - start_hour)*60 + (finish_minute - start_minute)
    if (finish_second - start_second) >= 30:
        duration = duration + 1
    return duration


"""
Start of the program:
1. First timestamp for the calculation of the runtime
2. One run of the whole programm, incl. SCHATSI002, SCHATSI003, SCHATSI004....
3. Second timestamp for the calculation of the runtime
4. Calculate the duration -> write the timestamps and the duration into the file "SCHATSI_runtime
"""
# Runtime
# open file for runtime

# LOCAL PATH FOR TESTING:
# runtime = open("SCHATSI_runtime.csv", 'w', newline='')
# PATH FOR DOCKER:
runtime = open("/data/output/SCHATSI_runtime.csv", 'w', newline='')
runtime_file = csv.writer(runtime, delimiter=';', quoting=csv.QUOTE_MINIMAL)
# writing a headline into the file
kopfzeile_runtime = ["start processing", "end processing", "duration (minutes)"]
runtime_file.writerow(kopfzeile_runtime)

# timestamp at the begin of the program and the normalized version which is written into "SCHATSI_runtime"
start = time.asctime()
start_normalized = time_analysis(start)
print("start time: ", start_normalized, "\n")

# At first: open the Output-File --> "SCHATSI_included.csv"
# LOCAL PATH FOR TESTING:
# output = open("SCHATSI_included.csv", 'w', newline='')
# PATH FOR DOCKER:
output = open("/data/output/SCHATSI_included.csv", 'w', newline='')
# create a writer object, which is used to write the lines into the csv
file = csv.writer(output, delimiter=';', quoting=csv.QUOTE_MINIMAL)
# onetime writing of a headline into the csv
kopfzeile = ["filename", "type", "included", "excluded"]
file.writerow(kopfzeile)

"""
preparation of data_cleansing.csv 
"""
# LOCAL PATH FOR TESTING:
# data_cleansing = open("SCHATSI_data_cleansing.csv", 'w', newline='')
# PATH FOR DOCKER:
data_cleansing = open("/data/output/SCHATSI_data_cleansing.csv", 'w', newline='')
data_cleansing_file = csv.writer(data_cleansing, delimiter=';', quoting=csv.QUOTE_MINIMAL)
kopfzeile_data_cleansing = ["filename", "type", "Total Count"]
data_cleansing_file.writerow(kopfzeile_data_cleansing)


"""
preparation of schatsi_references.csv
"""
# LOCAL PATH FOR TESTING:
# refs = open("SCHATSI_references.csv", 'w', newline='')
# PATH FOR DOCKER:
refs = open("/data/output/SCHATSI_references.csv", 'w', newline='')
refs_file = csv.writer(refs, delimiter=';', quoting=csv.QUOTE_MINIMAL)
kopfzeile_refs = ["filename", "reference_author", "reference_year", "reference_title"]
refs_file.writerow(kopfzeile_refs)

"""
preparation of schatsi_terms.csv
"""
# LOCAL PATH FOR TESTING:
# terms = open("SCHATSI_terms.csv", 'w', newline='')
# PATH FOR DOCKER:
terms = open("/data/output/SCHATSI_terms.csv", 'w', newline='')
terms_file = csv.writer(terms, delimiter=';', quoting=csv.QUOTE_MINIMAL)
kopfzeile_terms = ["filename", "term", "term count"]
terms_file.writerow(kopfzeile_terms)

"""
Preparation of the Stopwords for use in SCHATSI004 functions - import from file "SCHATSI_stopwords.csv
"""
stopwords_list = []
# LOCAL FOR TESTING:
# with open('SCHATSI_stopwords.csv') as stop:
# PATH FOR DOCKER:
with open(r'/data/input/SCHATSI_stopwords.csv') as stop:
    csv_reader_object = csv.reader(stop)
    for row in csv_reader_object:
        stopwords_list.append(row[0])
stopwords = set(stopwords_list)

# For all paths, subdirectories and files in the input-folder do:
# LOCAL PATH FOR TESTING: "r'/home/h/Github/Testpdfs'"
# for path, subdirs, files in os.walk(r'/home/h/Downloads/Testpdfs'):
# PATH FOR DOCKER:
for path, subdirs, files in os.walk(r'/data/input'):
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
        # if there is an exception or an error, they will be catched and the file wont be included in the next steps
        except:
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
        # if it succeeds do:
        else:
            if f.endswith(".pdf") or f.endswith(".PDF"):
                datatype = "pdf"
                # All files that are successfully read in where the type is 'pdf' will be used in the next steps
                text_only, references = SCHATSI003.string_preparation(text)
                total_num_words = SCHATSI003.count_words(text_only)
                zeile_data_cleansing = [filename, datatype, total_num_words]
                data_cleansing_file.writerow(zeile_data_cleansing)

                reference_list = SCHATSI003.references(references)
                for element in reference_list:
                    author, year, title = SCHATSI003.reference_data_cutting(element)
                    refs_zeile = [filename, author, year, title]
                    refs_file.writerow(refs_zeile)

                # Aufruf SCHATSI004: Filtering the expressions from the text and rank the Papers at the Base of the
                # functional terms given by the User
                monogram = SCHATSI004.terms(text_only)
                bigram = SCHATSI004.bigrams(monogram)
                trigram = SCHATSI004.trigrams(monogram)
                mono_filtered, mono_number = SCHATSI004.term_filtering(monogram, stopwords)
                bigram_filtered, bigram_number = SCHATSI004.bigram_filtering(bigram, stopwords)
                trigram_filtered, trigram_number = SCHATSI004.trigram_filtering(trigram, stopwords)
                # Result: 2 lists each: one with the filtered terms, the other with the counts of the terms
                # Writing in "SCHATSI_terms.csv"
                i, j, k = 0, 0, 0
                for i in range(0, len(mono_filtered)):
                    zeile_terms = [filename, mono_filtered[i], mono_number[i]]
                    terms_file.writerow(zeile_terms)
                for j in range(0, len(bigram_filtered)):
                    bi = bigram_filtered[j][0] + " " + bigram_filtered[j][1]
                    zeile_terms = [filename, bi, bigram_number[j]]
                    terms_file.writerow(zeile_terms)
                for k in range(0, len(trigram_filtered)):
                    tri = trigram_filtered[k][0] + " " + trigram_filtered[k][1] + " " + trigram_filtered[k][2]
                    zeile_terms = [filename, tri, trigram_number[k]]
                    terms_file.writerow(zeile_terms)

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

        file.writerow(zeile)

        # the outputfile will get a layout like this
        """
        filename | type | included | excluded
        --------------------------------------
        abc.pdf  | pdf  |     X    |    __        <-- The text of this document could be extracted without any problems
        err.pdf  | pdf  |    __    |     X        <-- There was a problem and the document text could not be extracted,
        ...                                           the files wont be included in the next steps 
        ...
        """

# Call the Ranking function from SCHATSI004.002
SCHATSI004.ranking()


# Calculate the runtime -> last step of the programm
# second timestamp
finish = time.asctime()
finish_normalized = time_analysis(finish)
print("finish time: ", finish_normalized, "\n")
# calculation of the duration
duration_program = duration_calc(start_normalized, finish_normalized)

# write start_normalized, finish_normalized and duration into "SCHATSI_runtime.csv"
zeile_runtime = [start_normalized, finish_normalized, duration_program]
runtime_file.writerow(zeile_runtime)
