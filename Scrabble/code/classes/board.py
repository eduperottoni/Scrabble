from classes.bag import Bag
from classes.word import Word
from classes.dictionary import Dictionary
from constants.cards import CARDS_QUANTITY_BY_LETTER
from constants.measures import BOARD_SIDE
from classes.position import NormalPosition, DWPosition, DLPosition, TWPosition, TLPosition

class Board:
    def __init__(self):
        self.__bag = Bag(CARDS_QUANTITY_BY_LETTER)
        self.__dictionary = Dictionary()
        print(self.__dictionary.search_word('xicara'))
        print(self.__dictionary.search_word('xyz'))
        self.__current_word = Word()
        self.__positions = []
        # self.__premium_spots = [] # premium_spots = [('A', 'TLS'), ('B', 'DLS'), ('C', 'DLS'), ('D', 'DWS'), ('E', 'TLS')]
        # self.__current_adjacent_words_dict = {}
        # TODO colocar essas listas como constantes, visto que também são utilizadas para a interface
        tw = [(0,0), (0,7), (0,14), (7,0), (7,14), (14,0), (14,7), (14,14)]
        dw = [(1,1), (2,2), (3,3), (4,4), (13,13), (12,12), (11,11), (10,10), (1,13), (2,12), (3,11), (4,10), (13,1), (12,2), (11,3), (10,4)]
        dl = [(0,3), (0,11), (2,6), (2,8), (3,0), (3,7), (3,14), (6,2), (6,6), (6,8), (6,12), (7,3), (7,11), (8,2), (8,6), (8,8), (8,12), (11,0), (11,7), (11,14), (12,6), (12,8), (14,3), (14,11)]
        tl = [(1,5), (1,9), (5,1), (5,5), (5,9), (5,13), (9,1), (9,5), (9,9), (9,13), (13,5), (13,9)]
        for line in range(BOARD_SIDE):
            positions_line = []
            for column in range(BOARD_SIDE):
                position = NormalPosition()
                if ((line, column) in tw): position = TWPosition()
                elif ((line, column) in dw): position = DWPosition()
                elif ((line, column) in dl): position = DLPosition()
                elif ((line, column) in tl): position = TLPosition()
                positions_line.append(position)
            self.__positions.append(positions_line)

    @property
    def positions(self):
        return self.__positions
    
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

    
    