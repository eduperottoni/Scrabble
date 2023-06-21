import copy
import json
from classes.bag import Bag
from classes.word import Word
from classes.card import Card
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
        for i in range(15):
            for j in range(15):
                self.__valid_words_search_dict[(i, j)] = {'horizontal': None, 'vertical': None}

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
    def dictionary(self):
        return self.__dictionary
    
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
        print("Entrando no calculate player score")
        total_score = 0
        word = self.__current_word

        word_multiply_const = 1
        for position in word.positions:
            if isinstance(position, DWPosition):
                print("entrou DW")
                word_multiply_const *= 2
            if isinstance(position, TWPosition):
                print("entrou TW")
                word_multiply_const *= 3

        for position in word.positions:
            letter_multiply_const = 1 
            if isinstance(position, DLPosition):
                print("entrou DL")
                letter_multiply_const *= 2
            if isinstance(position, TLPosition):
                print("entrou TL")
                letter_multiply_const *= 3
        
            letter_Score = position.card.value
            print("Valor da letra: ", letter_Score)
            total_score += (letter_Score * letter_multiply_const * word_multiply_const)
            print("total score:")
            print(total_score)

        return total_score

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
        # self.verify_words_existance_and_validity()
        # total = self.calculate_player_score()
        # print(total)
        self.update_search_dict()
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
        print("-----------------------------------------------")
        print("determine_adjacent_words")
        self.__current_adjacent_words_dict['current'] = copy.deepcopy(self.current_word)
        print(self.__current_adjacent_words_dict)
        print(self.__valid_words_search_dict)
        #TODO: TESTAR SE O POSIÇÃO CORRENTE ESTÁ COM DADOS NO SEARCH_DICT. SE ESTIVER: NO PRECISO DAR APPEND COM ELA. CASO CONTRÁRIO, PRECISO DAR APPEND COM ELA.
        #TODO: não tem como testar isso agora, só depois que der pra enviar a jogada pro outro jogador
        for position in self.current_word.positions:
            print("POSITION: ", position.coordinate)
            if self.current_word.direction == 'horizontal':
                # Coordenada abaixo
                coord_below = (position.coordinate[0] + 1, position.coordinate[1])
                # Coordenada acima
                coord_above = (position.coordinate[0] - 1, position.coordinate[1])

                already_valid_word_below = copy.deepcopy(self.__valid_words_search_dict[coord_below]['vertical']) if self.__valid_words_search_dict[coord_below]['vertical'] != None else None
                already_valid_word_above = copy.deepcopy(self.__valid_words_search_dict[coord_above]['vertical']) if self.__valid_words_search_dict[coord_above]['vertical'] != None else None
                print(f'PALAVRA JÁ VÁLIDA - VERTICAL abaixo:')
                if already_valid_word_below:
                    for position in already_valid_word_below.positions:
                        print(position.card.letter)
                print(f'PALAVRA JÁ VÁLIDA - VERTICAL acima:')
                if already_valid_word_above:
                    for position in already_valid_word_above.positions:
                        print(position.card.letter)
                if already_valid_word_below and already_valid_word_above:
                    already_valid_word_above.add_position(position)
                    [already_valid_word_above.add_position(position) for position in already_valid_word_below.positions]
                    self.__current_adjacent_words_dict['adjacents'].append(already_valid_word_above)   
                elif already_valid_word_above:
                    already_valid_word_above.add_position(position)
                    self.__current_adjacent_words_dict['adjacents'].append(already_valid_word_above)   
                elif already_valid_word_below:
                    already_valid_word_above.add_position(position)
                    self.__current_adjacent_words_dict['adjacents'].append(already_valid_word_above)   
            
            elif self.current_word.direction == 'vertical':
                print(f'POSIÇÃO {position.coordinate}')
                # Coordenada esquerda
                coord_left = (position.coordinate[0], position.coordinate[1] - 1)
                # Coordenada direita
                coord_right = (position.coordinate[0], position.coordinate[1] + 1)
                print(f'POSIÇÃO {coord_left}')
                print(f'POSIÇÃO {coord_right}')

                already_valid_word_left = copy.deepcopy(self.__valid_words_search_dict[coord_left]['horizontal']) if self.__valid_words_search_dict[coord_left]['horizontal'] != None else None
                already_valid_word_right = copy.deepcopy(self.__valid_words_search_dict[coord_right]['horizontal']) if self.__valid_words_search_dict[coord_right]['horizontal'] != None else None
                print(f'PALAVRA JÁ VÁLIDA - HORIZONTAL left:')
                print(self.__valid_words_search_dict[coord_left]['horizontal'])
                
                if already_valid_word_left:
                #     print(self.__valid_words_search_dict[coord_left]['horizontal'].direction)
                #     print(already_valid_word_left)
                #     print(already_valid_word_left.direction)
                #     print(already_valid_word_left.positions)
                    for position1 in already_valid_word_left.positions:
                        print(position1.card.letter)
                print(f'PALAVRA JÁ VÁLIDA - HORIZONTAL right:')
                print(self.__valid_words_search_dict[coord_right]['horizontal'])
                if already_valid_word_right:
                #     print(self.__valid_words_search_dict[coord_right]['horizontal'].direction)
                #     print(already_valid_word_right)
                #     print(already_valid_word_right.direction)
                #     print(already_valid_word_right.positions)
                    for position2 in already_valid_word_right.positions:
                        print(position2.card.letter)
                if already_valid_word_left and already_valid_word_right:
                    already_valid_word_left.add_position(position)
                    [already_valid_word_left.add_position(position) for position in already_valid_word_right.positions]
                    self.__current_adjacent_words_dict['adjacents'].append(already_valid_word_left)   
                elif already_valid_word_left:
                    print(position.coordinate)
                    already_valid_word_left.add_position(position)
                    self.__current_adjacent_words_dict['adjacents'].append(already_valid_word_left)   
                elif already_valid_word_right:
                    already_valid_word_right.add_position(position, 0)
                    self.__current_adjacent_words_dict['adjacents'].append(already_valid_word_right) 

        #TODO PEGAR A PALAVRA DE MESMA DIREÇÃO ANTERIOR E POSTERIOR  

            print(f'LETRA DA POSIÇÃO: {position.card.letter}')
        print("PALAVRAS ADJACENTES DETERMINADAS!")

        print(self.__current_adjacent_words_dict['adjacents'])
        for word in self.__current_adjacent_words_dict['adjacents']:
            print(word.get_string())
        print("-----------------------------------------------")

    def update_search_dict(self):
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
        print("ENTRANDO NO UPDATE SEARCH DICT")
        # current_adjacent_words = self.__current_adjacent_words_dict
        current_word = copy.deepcopy(self.__current_adjacent_words_dict['current'])
        direction = current_word.direction
        current_direction_key = ''
        adjacent_direction_key = ''
        for position in current_word.positions:
            coordinate = position.coordinate
            if direction == 'horizontal':
                current_direction_key = 'horizontal'
                adjacent_direction_key = 'vertical'
            elif direction == 'vertical':
                current_direction_key = 'vertical'
                adjacent_direction_key = 'horizontal'

            self.__valid_words_search_dict[coordinate][current_direction_key] = current_word
            print(f'palavra {current_word} adicionada em {coordinate} -> {current_direction_key}')
            for position in self.current_word.positions: print(position.card.letter)

        adjacents_words = copy.deepcopy(self.__current_adjacent_words_dict['adjacents'])
        for word in adjacents_words:
            positions_list = word.positions
            for position in positions_list:
                coordinate = position.coordinate
                self.__valid_words_search_dict[coordinate][adjacent_direction_key] = word
                print(position.card.letter)
            print(f'palavra {word} adicionada em {coordinate} -> {adjacent_direction_key}')

        for position in current_word.positions:
            coordinate = position.coordinate
            word = self.__valid_words_search_dict[coordinate][adjacent_direction_key]
            if word == None:
                self.__valid_words_search_dict[coordinate][adjacent_direction_key] = position.card.letter

        # print(self.current_adjacent_words_dict)
        # print(self.valid_words_search_dict)
        print("TERMINOU UPDATE SEARCH DICT")
        print(self.valid_words_search_dict)
        print(self.bag)
        print(self.dictionary.valid_words)

    def verify_words_existance_and_validity(self):
        print("verify_words_existance_and_validity")

        print(f'--palavra atual: ')
        print([position.card.letter for position in self.__current_adjacent_words_dict["current"].positions])
        current_string = (self.__current_adjacent_words_dict['current'].get_string()).lower()
        print(f"--AVALIANDO A PALAVRA: {current_string}")
        already_valid_words = self.__dictionary.valid_words
        if not self.__dictionary.search_word(current_string) and current_string not in already_valid_words:
            print(f"PALAVRA {current_string} NÃO EXISTE!")
            raise WordDoesNotExistException

        for word in self.__current_adjacent_words_dict['adjacents']:
            adjacent_string = word.get_string().lower()
            print(f"--AVALIANDO A PALAVRA: {adjacent_string}")
            if not self.__dictionary.search_word(adjacent_string) and current_string not in already_valid_words:
                print(f"PALAVRA {adjacent_string} NÃO EXISTE!")
                raise WordDoesNotExistException

        print("PALAVRAS VÁLIDADAS NO DICIONÁRIO!")
        self.__dictionary.set_new_valid_word(current_string)
        for word in self.__current_adjacent_words_dict['adjacents']:
            adjacent_string = word.get_string().lower()
            self.__dictionary.set_new_valid_word(adjacent_string)

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
        for index, coord in enumerate(all_coords):
            position = self.get_position(board_coord=coord)

            if position.is_enabled:
                print(f"{position.coordinate}")
                print("verificação de palavra totalmente conexa ERRO")
                return False
            elif position not in self.__current_word.positions:
                self.__current_word.add_position(position, index)

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

    def update(self, string, positions):
        for index, coord in enumerate(positions):
                letter = string[index]
                card = Card(letter)
                position = self.positions[coord[0]][coord[1]]
                position.card = card
                position.disable()
                self.current_word.add_position(position)
        # valida as regras gerais da palavra
        self.determine_adjacent_words()
        self.update_search_dict()
        if not self.first_word_created: self.first_word_created = True

        
