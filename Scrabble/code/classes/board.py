from classes.bag import Bag
from classes.dictionary import Dictionary
from constants.cards import CARDS_QUANTITY_BY_LETTER

class Board:
    def __init__(self):
        self.__bag = Bag(CARDS_QUANTITY_BY_LETTER)
        self.__dictionary = Dictionary()
    
    @property
    def bag(self):
        return self.__bag
    
    
    