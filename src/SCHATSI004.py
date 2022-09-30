"""
SCHATSI004: Term finding and filtering

Register every term

- register every existing term in the text
- Bigrams: Register every useful phrase with two words, e.g. 'Artifical Intelligence', 'Data Science',...
- Trigrams: Register every useful phrase with three words, e.g. 'Internet of things',...

For this tasks use filter to delete unuseful terms, like filling words (of, the, otherwise,...), or bigrams and
trigrams, which don't make any sense, for example 'on the road', 'of algorithm', 'Use of the'...

- term_filtering
- bigram_filtering
- trigram_filtering

INPUT: string which contains the whole text from a paper
OUTPUT: a list which all terms, bigrams and trigrams, filtered for unuseful terms and unuseful phrases
"""
# NOTE: Ranking Function was deleted from this file and is now part of the "SCHATSI_Ranker" (to find in the other repo with the same name), the code was put in a comment for understanding the history and as a backup

# Function for founding all single terms, contains all, even the unuseful
from typing import Tuple, List
import pandas as pd

def term_filtering(term_list):
    term_list_filtered = list(set(term_list))
    term_count_filtered = _count_elemtents_in_list(term_list_filtered, term_list)
    return term_list_filtered, term_count_filtered


def bigram_filtering(bigram_list):
    bigram_list_filtered = list(set(bigram_list))
    bigram_count_filtered = _count_elemtents_in_list(bigram_list_filtered, bigram_list)
    return bigram_list_filtered, bigram_count_filtered


def trigram_filtering(trigram_list, ):
    trigram_list_filtered = list(set(trigram_list))
    trigram_count_filtered = _count_elemtents_in_list(
        trigram_list_filtered, trigram_list
    )
    return trigram_list_filtered, trigram_count_filtered



def _count_elemtents_in_list(elements: List[Tuple], list: List[Tuple]) -> List[int]:
    # count total number of each trigram expression
    clounters = []
    for element in elements:
        counter = 0
        for trigram in list:
            if element == trigram:
                counter = counter + 1
        clounters.append(counter)
    return clounters


def ranking(functional_terms_input, terms_input):
    terms_df = functional_terms_input.join(terms_input.set_index('term'), on='term', how='inner')
    # preparation for building global sum of filtered words from "SCHATSI_terms.csv", for every file in the csv-file
    # global sum of FILTERED WORDS from SCHATSI_terms.csv
    global_sum_df = terms_input.groupby(by="filename")['term count'].sum().reset_index()
    global_sum_df.columns = ['filename', 'sum_terms']
    
    sum_found_func_terms_df = terms_df.groupby(by="filename")['term count'].sum().reset_index()
    sum_found_func_terms_df.columns = ['filename', 'sum_functional_terms']
        
    # calculate the results by dividing the sum of functional terms by the global sum for each file
    merged_df = sum_found_func_terms_df.merge(global_sum_df, how='inner', on='filename')
    merged_df = merged_df.reindex(columns=['filename', 'sum_functional_terms', 'sum_terms', 'result'])
    merged_df['result'] = merged_df['sum_functional_terms'].div(merged_df['sum_terms'])
    # order them from the highest score to the smallest
    merged_df = merged_df.sort_values('result', ascending=False)
    # Drop out the Columns with the Sum of functional terms and the global sum of terms
    # merged_df.drop(['sum_functional_terms', 'sum_terms'], axis=1)
    return merged_df