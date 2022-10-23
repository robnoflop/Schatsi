from typing import List, Tuple
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

class TextCleaner:
    
    stop_words = set(stopwords.words("english"))
    stemmer = PorterStemmer()
    
    def __init__(self) -> None:
        pass    
    
    def clean(self, text: str, monogram_return:bool = False) -> List[str]:
        monogram = nltk.word_tokenize(text)
        monogram = [word.lower() for word in monogram if word.isalpha()]
        monogram = [w for w in monogram if not w.lower() in self.stop_words]
        monogram = [self.stemmer.stem(w) for w in monogram]
        if monogram_return:
            return monogram
        
        return " ".join(monogram)
        
        
