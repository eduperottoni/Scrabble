from classes.enums import State, Move
from classes.player import Player
from classes.board import Board
from constants import messages

class RoundManager:
    def __init__(self):
        self.__match_state = State.NOT_INITIALIZED
        self.__local_player = Player()
        self.__remote_player = Player()
        self.__board = Board()
        self.__player_interface = None
        self.__move_type = None
    
    @property
    def player_interface(self):
        return self.__player_interface
    
    @player_interface.setter
    def player_interface(self, interface):
        self.__player_interface = interface

    @property
    def board(self) -> Board:
        return self.__board       
    
    @property
    def match_state(self) -> State:
        return self.__match_state

    @property
    def local_player(self) -> Player:
        return self.__local_player

    @property
    def remote_player(self) -> Player:
        return self.__remote_player
    
    @property
    def move_type(self) -> Move:
        return self.__move_type

    @move_type.setter
    def move_type(self, move_type: Move):
        self.__move_type = move_type
    
    @match_state.setter
    def match_state(self, match_state: State) -> None:
        self.__match_state = match_state

    @local_player.setter
    def local_player(self, local_player: Player):
        self.__local_player = local_player

    @remote_player.setter
    def remote_player(self, remote_player: Player):
        self.__remote_player = remote_player
    
    def configure_players(self, players: dict) -> None:
        self.local_player.initialize(players['local']['id'], players['local']['name'])
        self.remote_player.initialize(players['remote']['id'], players['remote']['name'])

    def start_game(self, players: dict) -> None:
        """
        Define the players and their turn (who starts the match)

        :param players: dict{'local' or 'remote' : {'id': str,
                                                    'name': str,
                                                    'turn': True or False}}
        """
        self.configure_players(players)
        print(players)
        self.__match_state = State.IN_PROGRESS
        print(f'estado do jogo setado como {self.match_state}')
        self.__move_type = Move.INITIAL
        print(f'tipo de movimento setado como {self.move_type}')
        self.__distribute_cards()
        if players['local']['turn']:
            print('VEZ DE JOGAR É DO JOGADOR LOCAL')
            self.local_player.toogle_turn()
        else:
            self.remote_player.toogle_turn()
            print('VEZ É DO JOGADOR REMOTO')
            self.__match_state = State.WAITING_REMOTE_MOVE
        print(self.__board.bag)

    def __distribute_cards(self):
        """
        Method to initialize bag's cards and distribute then to players
        """
        remote_cards = self.__board.bag.get_random_cards(7)
        local_cards = self.__board.bag.get_random_cards(7)
        self.local_player.pack.insert_cards(local_cards, [0,1,2,3,4,5,6])
        self.remote_player.pack.insert_cards(remote_cards, [0,1,2,3,4,5,6])

    def select_board_position(self, coord: tuple) -> int:
        """
        Method to handle with the SELECT BOARD POSITION use case

        :param coord: tuple indicating the position selectd
        :return int: 0 if the operation is invalid, 1 if the operation is valid 
        """
        print(f'Posição selecionada: {coord}')
        print(f'Estado do round-manager: {self.__match_state}')
        if self.local_player.is_turn:
            if self.move_type == Move.CONSTRUCTION:
                if self.local_player.pack.any_cards_selected:
                    print(f'TEMOS ALGUM CARD SELECIONADO -> {self.local_player.pack.any_cards_selected()}')
                    print(coord[0], coord[1])
                    position = self.board.positions[coord[0]][coord[1]]
                    card = self.local_player.pack.current_selected_cards[0]
                    if position.is_enabled:
                        self.player_interface.update_gui_board_position((coord[0], coord[1]), card.letter)
                        # DESABILITAR POSIÇÃO DO TABULEIRO
                        position.card = card
                        position.disable()
                        self.board.current_word.add_position(position)
                        # LIMPAR POSIÇÃO DO PACK E DESABILITÁ-LA
                        indexes = self.local_player.pack.remove_selected_cards()
                        self.player_interface.update_gui_local_pack(indexes)
                        #ADICIONAR CARD SELECTED NA WORD

                    else:
                        self.player_interface.show_message(messages.ERROR_INVALID_OPERATION_TITLE, "Posição já ocupada")
                else:
                    self.player_interface.show_message("", "")
            else:
                self.player_interface.show_message("", "")
        else:
            self.player_interface.show_message(messages.ERROR_INVALID_OPERATION_TITLE, messages.ERROR_OPERATION_BEFORE_START)

    def convert_move_to_dict(self):
        move = {}
        move['match_status'] = str(self.__match_state).replace('State.', '')
        move['move_type'] = str(self.__move_type).replace('Move.', '')
        move['remote_player'] = self.__remote_player.convert_to_json()
        move['local_player'] = self.__local_player.convert_to_json()
        return move

    def update_player_pack(self, player: Player, letters: 'list[str]', positions: 'list[int]') -> None:
        """
        Sets local player pack (in case the remote made the INITIAL move)
        """
        print(f'PACK DO JOGADOR {player.name} SENDO ATUALIZADO COM AS LETRAS {letters} NAS POSIÇÕES {positions}')
        cards = self.__board.bag.get_cards_by_letters(letters)
        player.pack.insert_cards(cards, positions)

    def select_card_from_pack(self, index: int):
        """
        Verify turn and move type and pass the control to pack

        :param index: index of the position of the pack selected in GUI
        """
        print('LOCAL')
        print(self.__local_player)
        print('REMOTE')
        print(self.__remote_player)
        if self.__local_player.is_turn:
            if self.move_type != Move.CHANGE:
                self.move_type = Move.CONSTRUCTION
            self.proceed_card_selection(index)
        else: self.__player_interface.show_message(title='Mensagem do DOG', message="CÊ TÁ MALUCO?")
    
    def proceed_card_selection(self, index: int):
        """
        Proceeds card selection

        :param index: index of the position of the pack clicked in GUI
        """
        pack = self.__local_player.pack
        if self.move_type == Move.CONSTRUCTION:
            any_selected = pack.any_cards_selected()
            if any_selected:
                # Gets the current selected card index
                selected_index = pack.get_selected_card_index()
                pack.deselect_all_cards()
                self.player_interface.mark_off_card(selected_index)
                print(self.local_player.pack.current_selected_cards)
            # Selects the card
            pack.select_card(index)
            print(self.local_player.pack.current_selected_cards[0].letter)
            self.player_interface.mark_card(index)

    def receive_move(self, move_type: Move, move_dict: dict):
        if move_type == Move.INITIAL:
            # Gets cards distribuited remotely and updates local instances
            print('O tipo de jogada recebida é INITIAL')
            local_initial_letters = [card['letter'] for card in move_dict['remote_player']['pack']['cards']]
            remote_initial_letters = [card['letter'] for card in move_dict['local_player']['pack']['cards']]
            self.update_player_pack(self.local_player, local_initial_letters, range(len(local_initial_letters)))
            self.update_player_pack(self.remote_player, remote_initial_letters, range(len(remote_initial_letters)))
            # Updates state and move type
            self.move_type == Move.INITIAL
            self.state = State.IN_PROGRESS
            print(self.board.bag)