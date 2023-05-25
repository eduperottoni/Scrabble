from classes.bag import Bag
from classes.dictionary import Dictionary
from constants.cards import CARDS_QUANTITY_BY_LETTER
from constants.cards import CARDS_VALUES_BY_LETTER

class Board:
    def __init__(self):
        self.__bag = Bag(CARDS_QUANTITY_BY_LETTER)
        self.__dictionary = Dictionary()
        self.__current_word = []
        # self.__premium_spots = [] # premium_spots = [('A', 'TLS'), ('B', 'DLS'), ('C', 'DLS'), ('D', 'DWS'), ('E', 'TLS')]
        # self.__current_adjacent_words_dict = {}
    
    @property
    def bag(self):
        return self.__bag

    @property
    def current_word(self):
        return self.__current_word
    
    @property
    def premium_spots(self):
        return self.__premium_spots
    
    @property
    def current_adjacent_words_dict(self):
        return self.__current_adjacent_words_dict
    
    def calculate_player_score(self):
        word = self.__current_word
        word_multiply_const = 1
        pass
        # word_score = 0
        # for letter in self.current_word:
        #     for spot in self.premium_spots:
        #         if letter == spot[0]:
        #             if spot[1] == "TLS":
        #                 word_score += CARDS_VALUES_BY_LETTER[letter] * 3
        #             elif spot[1] == "DLS":
        #                 word_score += CARDS_VALUES_BY_LETTER[letter] * 2
        #         else:
        #             word_score += CARDS_VALUES_BY_LETTER[letter]
        # for spot in self.premium_spots:
        #     if spot[1] == "TWS":
        #         word_score *= 3
        #     elif spot[1] == "DWS":
        #         word_score *= 2
        # self.player.increase_score(word_score)

    
    