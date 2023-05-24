from classes.bag import Bag
from classes.dictionary import Dictionary
from constants.cards import CARDS_QUANTITY_BY_LETTER

class Board:
    def __init__(self):
        self.__bag = Bag(CARDS_QUANTITY_BY_LETTER)
        self.__dictionary = Dictionary()
        self.__current_word = []
    
    @property
    def bag(self):
        return self.__bag

    @property
    def current_word(self):
        return self.__current_word
    
    def calculate_player_score(self):
        word = self.__current_word
        word_multiply_const = 1
        pass

    
    