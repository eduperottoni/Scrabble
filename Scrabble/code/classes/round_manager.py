from classes.enums import State

class RoundManager:
    def __init__(self):
        self.__match_state = State.NOT_INITIALIZED

    @property
    def match_state(self):
        return self.__match_state
