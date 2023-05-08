from classes.enums import State
from classes.player import Player

class RoundManager:
    def __init__(self):
        self.__match_state = State.NOT_INITIALIZED
        self.__local_player = Player()
        self.__remote_player = Player()

    @property
    def match_state(self) -> State:
        return self.__match_state

    @property
    def local_player(self) -> Player:
        return self.__local_player

    @property
    def remote_player(self) -> Player:
        return self.__remote_player
    
    @match_state.setter
    def match_state(self, match_state: State) -> None:
        self.match_state = match_state

    @local_player.setter
    def local_player(self, local_player: Player):
        self.__local_player = local_player

    @remote_player.setter
    def remote_player(self, remote_player: Player):
        self.__remote_player = remote_player
    

    def define_players_and_turn(self, players: dict) -> None:
        """
        Define the players and their turn (who starts the match)

        :param players: dict{'local' or 'remote' : {'id': str,
                                                    'name': str,
                                                    'turn': True or False}}
        """
        self.local_player.initialize(players['local']['id'], players['local']['name'])
        self.remote_player.initialize(players['remote']['id'], players['remote']['name'])
        if players['local']['turn']:
            self.local_player.toogle_turn()
            print('VEZ DE JOGAR É DO JOGADOR LOCAL')
            self.__match_state = State.LOCAL_MOVE
        else:
            self.remote_player.toogle_turn()
            print('VEZ É DO JOGADOR REMOTO')
            self.__match_state = State.WAITING_REMOTE_MOVE

