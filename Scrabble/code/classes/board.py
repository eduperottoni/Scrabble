from classes.bag import Bag
from constants.cards import CARDS_QUANTITY_BY_LETTER

class Board:
    def __init__(self):
        self.__bag = Bag(CARDS_QUANTITY_BY_LETTER)
    
    @property
    def bag(self):
        return self.__bag