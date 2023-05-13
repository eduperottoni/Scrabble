from classes.exceptions import PositionAlreadyHasCardException
from classes.exceptions import PositionDoesNotHaveCardException
from classes.exceptions import CardNotSelectedException

class Pack:
    def __init__(self):
        self.__cards = [None for _ in range(7)]
        self.__current_selected_cards = []
        self.__any_card_selected = False
    
    @property
    def cards(self):
        return self.__cards
    
    @property
    def current_selected_cards(self):
        return self.__current_selected_cards
    
    @property
    def any_cards_selected(self):
        return self.__any_card_selected
    
    def insert_cards(self, cards: list, coords: list) -> None:
        """
        Inserts cards on the specified positions in pack
        """
        for position in coords:
            if self.__cards[position] != None: raise PositionAlreadyHasCardException
            else: self.__cards[position] = cards[position]
    
    def select_card(self, coord: int) -> None:
        if self.__cards[coord] == None: raise PositionDoesNotHaveCardException
        else: self.__cards[coord].selected(True)

    def deselect_card(self, coord: int) -> None:
        if self.__cards[coord] == None: raise PositionDoesNotHaveCardException
        elif not self.__cards[coord].selected(): raise CardNotSelectedException
        else: self.__cards[coord].selected(True)

    def reset(self):
        self.__cards = [None for _ in range(7)]
        self.__current_selected_cards = []
        self.__any_card_selected = False

    def count_cards(self) -> int:
        return len(self.__cards)
