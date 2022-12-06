

from typing import Collection, List, Tuple


class NgramProcessor:
    """_summary_
    """
    
    def __init__(self) -> None:
        """_summary_
        """
        pass
    
    def ngram_filtering(self, term_list):
        """_summary_

        Args:
            term_list (_type_): _description_

        Returns:
            _type_: _description_
        """
        ngram_filterd = list(set(term_list))
        ngram_counts = self.__count_elemtents_in_list(ngram_filterd, term_list)
        return ngram_filterd, ngram_counts

    def __count_elemtents_in_list(self, elements: List[Tuple], list: List[Tuple]) -> List[int]:
        clounters = []
        for element in elements:
            counter = list.count(element)
            clounters.append(counter)
        return clounters