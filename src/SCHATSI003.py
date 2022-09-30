# SCHATSI003 - Data Cleansing

from nltk.tokenize import RegexpTokenizer


def split_references_and_content(input_text):
    low_string = input_text.lower()

    try:
        last_time_reference = low_string.rindex("\nreference")
    except:
        return low_string, None

    low_string_without_references = low_string[0:last_time_reference]
    references = low_string[last_time_reference:]
    return low_string_without_references, references


def count_words(text: str) -> int:
    tokenizer = RegexpTokenizer(r"\w+")
    text = "This is my text. It icludes commas, question marks? and other stuff. Also U.S.."
    tokens = tokenizer.tokenize(text)
    return len(tokens)
