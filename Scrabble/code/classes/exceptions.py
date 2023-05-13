from constants.messages import NOT_ENOUGH_CARDS_ON_BAG_EXCEPTION_MESSAGE
from constants.messages import POSITION_ALREADY_HAS_CARD_EXCEPTION
from constants.messages import POSITION_DOES_NOT_HAVE_CARD_EXCEPTION
from constants.messages import CARD_NOT_SELECTED_EXCEPTION

class NotEnoughCardsOnBagException(Exception):
    def __init__(self):
        self.message = NOT_ENOUGH_CARDS_ON_BAG_EXCEPTION_MESSAGE
        super().__init__(self.message) 

class PositionAlreadyHasCardException(Exception):
    def __init__(self):
        self.message = POSITION_ALREADY_HAS_CARD_EXCEPTION
        super().__init__(self.message)

class PositionDoesNotHaveCardException(Exception):
    def __init__(self):
        self.message = POSITION_DOES_NOT_HAVE_CARD_EXCEPTION
        super().__init__(self.message)

class CardNotSelectedException(Exception):
    def __init__(self):
        self.message = CARD_NOT_SELECTED_EXCEPTION
        super().__init__(self.message)