from classes.bag import Bag
from classes.word import Word
from classes.dictionary import Dictionary
from constants.cards import CARDS_QUANTITY_BY_LETTER
from constants.measures import BOARD_SIDE
from constants.positions import TW, DW, DL, TL
from classes.position import NormalPosition, DWPosition, DLPosition, TWPosition, TLPosition
from classes.exceptions import FirstWordRulesNotRespectedException , WordNotConnectedException, WordDoesNotExistException

class Board:
    def __init__(self):
        self.__bag = Bag(CARDS_QUANTITY_BY_LETTER)
        self.__dictionary = Dictionary()
        print(self.__dictionary.search_word('xicara'))
        print(self.__dictionary.search_word('xyz'))
        self.__current_word = Word()
        
        """
        This is a dictionary with current and adjacent words,
        populated during the submission process
        {'current': Word,
        'adjacents' = [Word, Word, Word]}
        """
        self.__current_adjacent_words_dict = {'current': None, 'adjacents': []}

        '''
        This attribute is a dictionary with the following structure:
        {(0,0) : {'horizontal': <WORD_IN_0,0_HORIZONTAL>,
                    'vertical': <WORD_IN_0,0_VERTICAL>},
        (0,1) : {'horizontal': <WORD_IN_0,1_HORIZONTAL>,
                    'vertical': <WORD_IN_0,1_VERTICAL>}}
        '''
        self.__valid_words_search_dict = {}

        self.__positions = []
        self.__first_word_created = False
        # self.__premium_spots = [] # premium_spots = [('A', 'TLS'), ('B', 'DLS'), ('C', 'DLS'), ('D', 'DWS'), ('E', 'TLS')]
        # # TODO colocar essas listas como constantes, visto que também são utilizadas para a interface
        # tw = [(0,0), (0,7), (0,14), (7,0), (7,14), (14,0), (14,7), (14,14)]
        # dw = [(1,1), (2,2), (3,3), (4,4), (13,13), (12,12), (11,11), (10,10), (1,13), (2,12), (3,11), (4,10), (13,1), (12,2), (11,3), (10,4)]
        # dl = [(0,3), (0,11), (2,6), (2,8), (3,0), (3,7), (3,14), (6,2), (6,6), (6,8), (6,12), (7,3), (7,11), (8,2), (8,6), (8,8), (8,12), (11,0), (11,7), (11,14), (12,6), (12,8), (14,3), (14,11)]
        # tl = [(1,5), (1,9), (5,1), (5,5), (5,9), (5,13), (9,1), (9,5), (9,9), (9,13), (13,5), (13,9)]
        for line in range(BOARD_SIDE):
            positions_line = []
            for column in range(BOARD_SIDE):
                position = NormalPosition((line, column))
                if ((line, column) in TW): position = TWPosition((line, column))
                elif ((line, column) in DW): position = DWPosition((line, column))
                elif ((line, column) in DL): position = DLPosition((line, column))
                elif ((line, column) in TL): position = TLPosition((line, column))
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
    def valid_words_search_dict(self):
        return self.__valid_words_search_dict
    
    @property
    def first_word_created(self):
        return self.__first_word_created

    @property
    def premium_spots(self):
        return self.__premium_spots
    
    @property
    def current_adjacent_words_dict(self):
        return self.__current_adjacent_words_dict
    
    @first_word_created.setter
    def first_word_created(self, created: bool):
        self.__first_word_created = created

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
            raise FirstWordRulesNotRespectedException
    
    def verify_valid_word(self) -> bool:
        print("VERIFICANDO AS REGRAS GERAIS DA PALAVRA!")
        self.verify_connected_positions()
        self.determine_adjacent_words()
        self.verify_words_existance_and_validity()
        return True

    def verify_connected_positions(self):
        print("--VERIFICANDO CONEXÃO DOS CARDS DA PALAVRA")

        aux = self.verify_current_word_same_line_or_column()
        direction = aux[1]
        
        if direction != None:
            print(f"---A PALAVRA ESTÁ NA {aux[1]}")
            self.current_word.direction = direction
            max_min_positions = self.current_word.get_min_max_positions()
            
            min_position = max_min_positions[0]
            max_position = max_min_positions[1]
            
            fill = self.verify_positions_filling(min_position.coordinate, max_position.coordinate)
            
            if not fill:
                print("--PALAVRA NÃO ESTÁ CONEXA")
                raise WordNotConnectedException
            else:
                print("--PALAVRA ESTÁ CONEXA")
                return True
        else:
            print("--Erro ao tentar encontrar direção da palavra.")
            raise WordNotConnectedException
    
    def determine_adjacent_words(self):
        """
        self.__current_adjacent_words_dict = 
        {'current': Word,
        'adjacents' = [Word, Word, Word]}

        
        self.__valid_words_search_dict =
        {(0,0) : {'horizontal': <WORD_IN_0,0_HORIZONTAL>,
                    'vertical': <WORD_IN_0,0_VERTICAL>},
        (0,1) : {'horizontal': <WORD_IN_0,1_HORIZONTAL>,
                    'vertical': <WORD_IN_0,1_VERTICAL>}}
        """

        print("determine_adjacent_words")
        
        self.__current_adjacent_words_dict['current'] = self.current_word

        #TODO: não tem como testar isso agora, só depois que der pra enviar a jogada pro outro jogador
        # for position in self.current_word.positions:
        #     if self.current_word.direction == 'horizontal':
        #         coord1 = (position.coordinate[0], position.coordinate[1] + 1)
        #         coord2 = (position.coordinate[0], position.coordinate[1] - 1)
                
        #         if self.__valid_words_search_dict[coord1]['vertical']:
        #             self.__current_adjacent_words_dict['adjacents'].append(self.__valid_words_search_dict[coord1]['vertical'])
        #         elif self.__valid_words_search_dict[coord2]['vertical']:
        #             self.__current_adjacent_words_dict['adjacents'].append(self.__valid_words_search_dict[coord2]['vertical'])   
        #     elif self.current_word.direction == 'vertical':
        #         coord1 = (position.coordinate[0] + 1, position.coordinate[1])
        #         coord2 = (position.coordinate[0] - 1, position.coordinate[1])
                
        #         if self.__valid_words_search_dict[coord1]['horizontal']:
        #             self.__current_adjacent_words_dict['adjacents'].append(self.__valid_words_search_dict[coord1]['horizontal'])
        #         elif self.__valid_words_search_dict[coord2]['horizontal']:
        #             self.__current_adjacent_words_dict['adjacents'].append(self.__valid_words_search_dict[coord2]['horizontal'])
        
        # print("PALAVRAS ADJACENTES DETERMINADAS!")

    def verify_words_existance_and_validity(self):
        print("verify_words_existance_and_validity")

        print(f'--palavra atual: ')
        print([position.card.letter for position in self.__current_adjacent_words_dict["current"].positions])
        current_string = (self.__current_adjacent_words_dict['current'].get_string()).lower()
        print(f"--AVALIANDO A PALAVRA: {current_string}")
        if not self.__dictionary.search_word(current_string):
            print(f"PALAVRA {current_string} NÃO EXISTE!")
            raise WordDoesNotExistException

        for word in self.__current_adjacent_words_dict['adjacents']:
            adjacent_string = (word.get_string()).lower()
            print(f"--AVALIANDO A PALAVRA: {adjacent_string}")
            if not self.__dictionary.search_word(adjacent_string):
                print(f"PALAVRA {adjacent_string} NÃO EXISTE!")
                raise WordDoesNotExistException

        print("PALAVRAS VÁLIDADAS NO DICIONÁRIO!")
        return True
    
    def verify_current_word_same_line_or_column(self):
        """
        Called whenever a submission of word is running
        Returns if the current word's cards are positioned in same line or column in the board
        """
        #TODO: mudar no diagrama pq a lógica mudou
        print('Running verify_current_word_same_line_or_column')
        word = self.current_word
        line = None
        column = None
        direction = None

        for position in word.positions:
            l = position.coordinate[0]
            c = position.coordinate[1]

            # só entra aqui na primeira posição (eixo do vetor)
            if line == None:
                line = l
                column = c
            # só entra aqui na segunda posição (direção do vetor)
            elif direction == None:
                same_line = l - line

                if same_line == 0:
                    direction = 'horizontal'
                else:
                    same_column = c - column

                    if same_column == 0:
                        direction = 'vertical'
                    else:
                        print("1 - verificação de mesma linha ou coluna NOP")
                        raise WordNotConnectedException
            # entra aqui em todas as outras posições
            else:
                if direction == 'horizontal':
                    if (position.coordinate[0] - line) != 0:
                        print("2 - verificação de mesma linha ou coluna NOP")
                        raise WordNotConnectedException

                if direction == 'vertical':
                    if (position.coordinate[1] - column) != 0:
                        print("3 - verificação de mesma linha ou coluna NOP")
                        raise WordNotConnectedException

        print("verificação de mesma linha ou coluna OK")
        print(f"DIREÇÃO: {direction}")
        return (True, direction)
    
    def verify_positions_filling(self, min_position: tuple, max_position: tuple) -> bool:
        print(min_position, max_position)

        all_coords = self.generate_coords(min_coord=min_position, max_coord=max_position, direction=self.current_word.direction)
        print(f'Coordenadas geradas pelo generate_copordenates : {all_coords}')
        for coord in all_coords:
            position = self.get_position(board_coord=coord)

            if position.is_enabled:
                print(f"{position.coordinate}")
                print("verificação de palavra totalmente conexa ERRO")
                return False
            elif position not in self.__current_word.positions:
                self.__current_word.add_position(position)

        print("verificação de palavra totalmente conexa OK")
        return True
    
    def get_position(self, board_coord: tuple):
        return self.__positions[board_coord[0]][board_coord[1]]

    def generate_coords(self, min_coord: tuple, max_coord: tuple, direction: str) -> list:
        """
        Gets the min and max coordinates and generate the full range of the coordinates
        """

        coords = []

        if direction == 'horizontal':
            for x in range(min_coord[1], max_coord[1]+1):
                print((max_coord[0], x))
                coords.append((max_coord[0], x))

        elif direction == 'vertical':
            for y in range(min_coord[0], max_coord[0]+1):
                print((y, min_coord[1]))
                coords.append((y, min_coord[1]))

        return coords
    
    def reset_curr_adj_words_dict(self):
        self.__current_adjacent_words_dict = {'current': None, 'adjacents': []}