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
        self.match_state = match_state

    @local_player.setter
    def local_player(self, local_player: Player):
        self.__local_player = local_player

    @remote_player.setter
    def remote_player(self, remote_player: Player):
        self.__remote_player = remote_player
    

    def start_game(self, players: dict) -> None:
        """
        Define the players and their turn (who starts the match)

        :param players: dict{'local' or 'remote' : {'id': str,
                                                    'name': str,
                                                    'turn': True or False}}
        """
        self.local_player.initialize(players['local']['id'], players['local']['name'])
        self.remote_player.initialize(players['remote']['id'], players['remote']['name'])
        print(players)
        if players['local']['turn']:
            self.local_player.toogle_turn()
            print('VEZ DE JOGAR É DO JOGADOR LOCAL')
            self.__distribute_cards()
            self.__match_state = State.IN_PROGRESS
            self.__move_type = Move.INITIAL
        else:
            self.remote_player.toogle_turn()
            print('VEZ É DO JOGADOR REMOTO')
            self.__match_state = State.WAITING_REMOTE_MOVE

    def __distribute_cards(self):
        """
        Method to initialize bag's cards and distribute then to players
        """
        print('Construindo board')
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
        if self.__match_state == State.LOCAL_MOVE:
            print('Lidando com a lógica do jogo')
        else:
            self.player_interface.show_message(messages.ERROR_INVALID_OPERATION_TITLE, messages.ERROR_OPERATION_BEFORE_START)

    def convert_move_to_dict(self):
        move = {}
        move['match_status'] = str(self.__match_state).replace('State.', '')
        move['move_type'] = str(self.__move_type).replace('Move.', '')
        move['remote_player'] = self.__remote_player.convert_to_json()
        move['local_player'] = self.__local_player.convert_to_json()
        return move