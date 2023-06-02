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
        self.__first_word = False
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
                position = NormalPosition((line, column))
                if ((line, column) in tw): position = TWPosition((line, column))
                elif ((line, column) in dw): position = DWPosition((line, column))
                elif ((line, column) in dl): position = DLPosition((line, column))
                elif ((line, column) in tl): position = TLPosition((line, column))
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
    def first_word(self):
        return self.__first_word

    @property
    def premium_spots(self):
        return self.__premium_spots
    
    @property
    def current_adjacent_words_dict(self):
        return self.__current_adjacent_words_dict
    
    def first_word_created(self):
        self.__first_word = True

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

    def verify_first_word_rules(self):
        print("VERIFICANDO AS REGRAS DA PRIMEIRA PALAVRA")

        # verificar se há um card no centro do tabuleiro
        card_in_center = False
        for position in self.__current_word.positions:
            print(position.coordinate)
            if position.coordinate == (7, 7):
                print("EXISTE UM CARD NO CENTRO")
                card_in_center = True
                break
    
        more_then_one_card = True if len(self.__current_word.positions) > 1 else False

        if more_then_one_card and card_in_center:
            print("TODAS AS REGRAS DE 1 PALAVRA FORAM RESPEITADAS")
            return True
        else:
            print("AS REGRAS DE PRIMEIRA PALAVRA NÃO FORAM RESPEITADAS")
            return False
    
    def verify_valid_word(self):
        print("VERIFICANDO AS REGRAS GERAIS DA PALAVRA!")

        connected = self.verify_connected_positions()
        self.determine_adjacent_words()
        valid = self.verify_words_existance_and_validity()

        if connected and valid:
            return True
        else:
            return False

    def verify_connected_positions(self):
        print("VERIFICANDO CONEXÃO DOS CARDS DA PALAVRA")

        aux = self.verify_current_word_same_line_or_column()
        direction = aux[1]
        if direction != None:
            print(f"A PALAVRA ESTÁ na {aux[1]}")
            self.current_word.direction = direction
            self.current_word.get_min_max_positions()

            return True
        return False
    
    def determine_adjacent_words(self):
        print("determine_adjacent_words")
    
        return False

    def verify_words_existance_and_validity(self):
        print("verify_words_existance_and_validity")

        return False
    
    def verify_current_word_same_line_or_column(self):
        """
        Called whenever a submission of word is running
        Returns if the current word's cards are positioned in same line or column in the board
        """
        word = self.current_word
        line = None
        column = None
        direction = None

        for position in word.positions:
            x = position.coordinate[0]
            y = position.coordinate[1]

            # só entra aqui na primeira posição
            if line == None:
                line = x
                column = y
            # só entra aqui na segunda posição
            elif direction == None:
                same_line = position.coordinate[0] - line

                if same_line == 0:
                    direction = 'horizontal'
                else:
                    same_column = position.coordinate[1] - column

                    if same_column == 0:
                        direction = 'vertical'
                    else:
                        return (False, None)
            # entra aqui em todas as outras posições
            else:
                if direction == 'horizontal':
                    if (position.coordinate[0] - line) != 0:
                        return (False, None)

                if direction == 'vertical':
                    if (position.coordinate[1] - column) != 0:
                        return (False, None)

        return (True, direction)