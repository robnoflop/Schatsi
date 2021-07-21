# SCHATSI003 - Data Cleansing

import os
import csv
import pdftotext


"""
SCHATSI003.1: Counting words for a paper

1. string_preparation:
- at first: lower all letters, so that there is no difference between "Apple" and "apple"
- split the string in two parts: the text and the references

2. count_words: All words in the 'low_string_without_references' -> Total Words (in the moment with all filling Words
    (later this filling words will be filtered out)

"""


def string_preparation(input_text):
    # lower all letters, so theres no difference between words like "Computer" and "computer" for example
    low_string = input_text.lower()

    try:
        # Position in the string, where the last occurence of "reference" starts
        last_time_reference = low_string.rindex("reference")
    except:
        # If the string didnt contain the word "reference", which means that there arent any references (for example
        # when the pdf is an essay) than the whole document is used as text and the reference string is empty
        low_string_without_references = low_string
        references = ""
    else:
        # Only consider the part of the string without the references -> Use this string for text analysis
        low_string_without_references = low_string[0:last_time_reference]
        # Text which contains all references
        references = low_string[last_time_reference:]

    return low_string_without_references, references


def count_words(input_text):
    num_words = 0
    past_letter = " "
    for i in input_text:
        actual_letter = i
        if past_letter == " " or past_letter == "\n" or past_letter == "\t":
            if actual_letter != " " and actual_letter != "\n" and actual_letter != "\t":
                num_words = num_words + 1
        past_letter = actual_letter

    # total_num_words = len(input_text.strip().split(" "))
    return num_words


# SCHATSI003.2: Extract the Metadata from the Paper
def metadata_author(input_text):
    pass


def metadata_year(input_text):
    pass


def metadata_title(input_text):
    pass


def metadata_origin(input_text):
    pass


# SCHATSI003.3: Extract all References from the paper and store the Information in a new file -> one for each paper
def references(input_text):
    pass


test = "Dies ist ein Test um zu sehen ob das Programm auch wirklich alle Wörter wie zum Beispiel 44 und fünfzig auch richtig zu erkennen. Was ist mit Satzzeichen? \n\n\t Und wie ist es mit Absätzen?   Und bei mehreren Leerzeichen"

anzahl = count_words(test)
print("Anzahl: ", anzahl)