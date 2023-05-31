from classes.exceptions import PositionAlreadyHasCardException
from classes.exceptions import PositionDoesNotHaveCardException
from classes.exceptions import CardNotSelectedException

class Pack:
    def __init__(self):
        self.__cards = [None for _ in range(7)]
        self.__current_selected_cards = []
    
    @property
    def cards(self):
        return self.__cards
    
    @property
    def current_selected_cards(self):
        return self.__current_selected_cards
    
    def any_cards_selected(self):
        return self.__current_selected_cards != []
    
    def insert_cards(self, cards: list, coords: list) -> None:
        """
        Inserts cards on the specified positions in pack
        """
        for position in coords:
            if self.__cards[position] != None: raise PositionAlreadyHasCardException
            else: self.__cards[position] = cards[position]
    
    def select_card(self, index: int) -> None:
        if self.__cards[index] == None: raise PositionDoesNotHaveCardException
        else: 
            self.__cards[index].self_select()
            self.current_selected_cards.append(self.cards[index])

    def deselect_card(self, index: int) -> None:
        if self.__cards[index] == None: raise PositionDoesNotHaveCardException
        elif not self.__cards[index].selected : raise CardNotSelectedException
        else: 
            self.__cards[index].self_unselect()
            self.current_selected_cards.remove(self.__cards[index])

    def reset(self):
        self.__cards = [None for _ in range(7)]
        self.__current_selected_cards = []

    def count_cards(self) -> int:
        return len(self.__cards)
    
    # Just to make tests
    # def __str__(self):
    #     string = ''
    #     for card in self.__cards:
    #         string += f'{card.letter} -> {card.value}\n'
    #     return string
