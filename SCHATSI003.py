# SCHATSI003 - Data Cleansing

import re

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
        last_time_reference = low_string.rindex("\nreference")
    except:
        # If the string didnt contain the word "reference", which means that there arent any references (for example
        # when the pdf is just an abstract) the whole document is used as text and the reference string is empty
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


"""SCHATSI003.2: Extract the Metadata from the Paper

"""
def metadata_author(input_text):
    pass


def metadata_year(input_text):
    pass


def metadata_title(input_text):
    pass


def metadata_origin(input_text):
    pass


"""SCHATSI003.3: Extract all References from the paper and store the Information in a new file -> one for each paper

"""


def reference_data_cutting(input_text):
    # Input: String, every String contains 1 reference
    # for different sorts of literature the cutting could be different
    if input_text == "":
        return "No REFERENCES FOUND" "NO REFERENCES FOUND" "NO REFERENCES FOUND"
    reference_year = ""
    # search for the year
    numbers_in_string = re.findall('([0-9]*)', input_text)
    for element in numbers_in_string:
        # for every Reference, there can only be one number for the year
        # and the will appear before other numbers like the DOI
        # if found: break out
        try:
            if (int(element) > 1950) and (int(element) < 2040):
                reference_year = element
                break
        except:
            continue
    # search for the author
    reference_author = input_text[:input_text.find(":")]

    # search for the title
    reference_title = input_text[input_text.find(":")+1:]
    if "In:" in reference_title:
        reference_title = reference_title[:reference_title.find("In:")]
    elif "available at:" in reference_title:
        reference_title = reference_title[:reference_title.find("available at:")]
    elif ". " in reference_title:
        reference_title = reference_title[:reference_title.find(". ")]
    elif "(" in reference_title:
        reference_title = reference_title[:reference_title.find("(")]
    elif str(reference_year) in reference_title:
        reference_title = reference_title[:reference_title.find(reference_year)]

    print("REFERENCE AUTHOR: " + reference_author + " REFERENCE YEAR: " + reference_year + " REFERENCE TITLE: " + reference_title)
    return reference_author, reference_year, reference_title

def references(input_text):
    ref_list = []
    number = 1

    # check if there are any References in the File: If empty, return empty list
    if len(input_text) == 0 or len(input_text) == 1:
        return ref_list

    else:
        # Seperatorstyle detection
        if input_text.find("[1]") >= 0:
            seperator = "[" + str(number) + "] "
            next_sep = "[" + str(number+1) + "] "
            style = 0
        elif input_text.find("1.") >= 0:
            seperator = str(number) + ". "
            next_sep = str(number+1) + ". "
            style = 1
        elif input_text.find("1 ") >= 0:
            seperator = str(number) + " "
            next_sep = str(number+1) + " "
            style = 2
        else:
            # Files which lists the references without any seperator
            seperator = "\n"
            next_sep = "\n"
            style = 3

        # Textpreparation: Cutting of all things before the first appearence of the seperator
        first_appearence_sep = input_text.find(seperator)
        pure_references = input_text[first_appearence_sep:]

        # Ausgangspunkt: Text, welcher mit dem Seperator beginnt.
        # For Style 0,1,2:
        if style < 3:
            while next_sep in pure_references:
                # For every reference style create a seperator for the beginning and for the end of one reference
                if style == 0:
                    seperator = "[" + str(number) + "]"
                    next_sep = "[" + str(number + 1) + "]"
                elif style == 1:
                    seperator = str(number) + "."
                    next_sep = str(number + 1) + "."
                elif style == 2:
                    seperator = str(number) + " "
                    next_sep = str(number + 1) + " "

                # If there are more then one Reference
                if next_sep in pure_references:
                    ref = pure_references[pure_references.find(seperator):pure_references.find(next_sep)]
                    pure_references = pure_references[pure_references.find(next_sep):]
                    ref = ref.replace(seperator, "", 1)
                    ref_list.append(ref)

                    number = number + 1
                # for the last reference -> Everything left from the input-text into the last entry
                else:
                    ref = pure_references[pure_references.find(seperator):]
                    ref = ref.replace(seperator, "", 1)
                    ref_list.append(ref)
                    number = number + 1
        # For style 3, which dont use numbers
        else:
            while len(pure_references) > 1:
                ref = pure_references[pure_references.find(seperator):pure_references.find(next_sep)]
                pure_references = pure_references.replace(ref, "", 1)
                ref = ref.replace(seperator, "", 1)
                ref_list.append(ref)


        return ref_list


