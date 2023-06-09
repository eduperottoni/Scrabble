from constants.messages import NOT_ENOUGH_CARDS_ON_BAG_EXCEPTION_MESSAGE
from constants.messages import POSITION_ALREADY_HAS_CARD_EXCEPTION
from constants.messages import POSITION_DOES_NOT_HAVE_CARD_EXCEPTION
from constants.messages import CARD_NOT_SELECTED_EXCEPTION

from constants.messages import FIRST_WORD_RULES_NOT_RESPECTED_EXCEPTION
from constants.messages import WORD_NOT_CONNECTED_EXCEPTION
from constants.messages import WORD_DOES_NOT_EXIST_EXCEPTION
# from constants.messages import 

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

class FirstWordRulesNotRespectedException(Exception):
    def __init__(self):
        self.message = FIRST_WORD_RULES_NOT_RESPECTED_EXCEPTION
        super().__init__(self.message)

class WordNotConnectedException(Exception):
    def __init__(self):
        self.message = WORD_NOT_CONNECTED_EXCEPTION
        super().__init__(self.message)

class WordDoesNotExistException(Exception):
    def __init__(self):
        self.message = WORD_DOES_NOT_EXIST_EXCEPTION
        super().__init__(self.message)