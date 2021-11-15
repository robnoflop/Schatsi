"""
SCHATSI004:

####004.001: Read Ranking

######## 004.001.001: Register every term

- register every existing term in the text
- Bigrams: Register every useful phrase with two words, e.g. 'Artifical Intelligence', 'Data Science',...
- Trigrams: Register every useful phrase with three words, e.g. 'Internet of things',...

For this tasks use filter to delete unuseful terms, like filling words (of, the, otherwise,...), or bigrams and
trigrams, which don't make any sense, for example 'on the road', 'of algorithm', 'Use of the'...

There has to be a filter for characters like '.', ',', ';', '-', '?', '!'..., so that these characters won't be
part of a word.

INPUT: string which contains the whole text from a paper
OUTPUT: a list which all terms, filtered for unuseful terms and unuseful phrases


######## 004.001.002: Ranking

INPUT: list with all terms from 004.001.001 AND Meta data table from SCHATSI003.002 (Data Cleansing)
OUTPUT: A File called "SCHATSI_terms.csv", which contains all entries for every paper in the following style

Filename (as Foreign key)   | Author    | Year  | Title     | Total Count   | Term      | Term Count
-----------------------------------------------------------------------------------------------------
example.pdf                 | Mr. M     | 1999  | Blabla    |  20345        | Pointer   | 15
example.pdf                 | Mr. M     | 1999  | Blabla    |  20345        | Stack     | 2
example.pdf                 | Mr. M     | 1999  | Blabla    |  20345        | Array     | 71
...                             ...         ...     ...         ...             ...         ...
Miller.pdf                  | Mr. X     | 2010  | MyLife    |  10000        | Pointer   | 33
Miller.pdf                  | Mr. X     | 2010  | MyLife    |  10000        | Beer      | 2
Miller.pdf                  | Mr. X     | 2010  | MyLife    |  10000        | Family member   | 45
...                             ...         ...     ...         ...             ...         ...

NOTE: The first 5 coloums are from SCHATSI_datacleansing.csv (1-4) and from SCHATSI_included.csv (5)

- For every Paper there has to be a routine for every element in the list of terms from 004.001.001, so that
the frequency of a term is counted and a line is written in the file "SCHATSI_terms.csv"
"""

def terms(text):
    word = ""
    entry = ""
    term_list = []
    i = 0

    special_chars = [' ', '\n', '\t', '.', ',', '?', '!', '%', '&', '/', '(', ')', '[', ']', '{', '}', '=', '§', '$',
                     '€', ":", ";", "|", "@", "+", "-", "*", "~", "#", "'", "_", ">", "<", "`", "´", "\"", "\'", "/"]

    while i < len(text)-1:
        if text[i] not in special_chars:
            word = word + text[i]
            i = i + 1
        elif text[i] in special_chars and word != "":
            i = i + 1
            break
        else:
            i = i + 1

        # When a word is found: the word is written into an entry and the entry is appended to a term list
        # After that the word is reseted
        # and a new word will be searched
        if word != "" and text[i] in special_chars:
            entry = word
            word = ""
            term_list.append(entry)
            entry = ""
    return term_list


def bigrams(term_list):
    bigram = []
    bigram_list = []
    for i in range(0, len(term_list)-1):
        bigram.append(term_list[i])
        bigram.append(term_list[i+1])
        bigram_list.append(bigram)
        bigram = []
    return bigram_list


def trigrams(term_list):
    trigram = []
    trigram_list = []

    for i in range(0, len(term_list)-2):
        trigram.append(term_list[i])
        trigram.append(term_list[i+1])
        trigram.append(term_list[i+2])
        trigram_list.append(trigram)
        trigram = []
    return trigram_list


def term_filtering(term_list, stopwords):
    # remove duplicates and filter for unuseful words
    term_list_filtered = []
    term_count_filtered = []
    for element in term_list:
        if element not in term_list_filtered and element not in stopwords:
            term_list_filtered.append(element)

    for element in term_list_filtered:
        counter = 0
        for term in term_list:
            if element == term:
                counter = counter + 1
        term_count_filtered.append(counter)

    return term_list_filtered, term_count_filtered


def bigram_filtering(bigram_list, stopwords):
    bigram_list_filtered = []
    bigram_count_filtered = []
    for element in bigram_list:
        if element in bigram_list_filtered:
            continue
        elif element[0] in stopwords or element[1] in stopwords:
            continue
        else:
            bigram_list_filtered.append(element)

    for element in bigram_list_filtered:
        counter = 0
        for bigram in bigram_list:
            if element == bigram:
                counter = counter + 1
        bigram_count_filtered.append(counter)

    return bigram_list_filtered, bigram_count_filtered


def trigram_filtering(trigram_list, stopwords):
    trigram_list_filtered = []
    trigram_count_filtered = []
    for element in trigram_list:
        if element in trigram_list_filtered:
            continue
        elif element[0] not in stopwords and element[1] in stopwords and element[2] not in stopwords:
            trigram_list_filtered.append(element)
        else:
            continue

    for element in trigram_list_filtered:
        counter = 0
        for trigram in trigram_list:
            if element == trigram:
                counter = counter + 1
        trigram_count_filtered.append(counter)

    return trigram_list_filtered, trigram_count_filtered
