from classes.card import Card

class Position:
    def __init__(self):
        self.__coordinate = ()
        self.__card = None
        self.__is_enabled = True

    @property
    def coordinate(self):
        return self.__coordinate

    @property
    def card(self):
        return self.__card
    
    @property
    def is_enabled(self):
        return self.__is_enabled
    
    @card.setter
    def card(self, card: Card):
        self.__card = card
    
    @coordinate.setter
    def coordinate(self, coordinate: 'tuple(int, int)'):
        self.__coordinate = coordinate

    def disable(self) -> None:
        self.__is_enabled = False

class SpecialPosition(Position):
    def __init__(self):
        super().__init__()

class NormalPosition(Position):
    def __init__(self):
        super().__init__()

class DWPosition(SpecialPosition):
    def __init__(self):
        super().__init__()

class DLPosition(SpecialPosition):
    def __init__(self):
        super().__init__()

class TLPosition(SpecialPosition):
    def __init__(self):
        super().__init__()

class TWPosition(SpecialPosition):
    def __init__(self):
        super().__init__()