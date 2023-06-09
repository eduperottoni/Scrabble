from classes.card import Card
from random import randint
from classes.exceptions import NotEnoughCardsOnBagException

class Bag:
    def __init__(self, cards_quantity_per_letter: dict):
        """
        Constructor makes a card's dictionary
        keys: letters (A-Z)
        values: card's values (1-8)

        :param cards_quantity_by_letter: dictionary containing
        keys: letters (A-Z)
        values: quantity of cards with this letter
        """
        self.__cards_amount_per_letter = cards_quantity_per_letter

        '''É desnecessário armazenar os objetos, uma vez que podemos
        apenas criá-los no momento necessário. Portanto, armazenamos
        apenas a quantdade de cada um atualizada na bag. Quando solicitados
        novos cards, eles são criados.
        '''

    def get_cards_amount(self) -> int:
        """
        Return the total of cards in bag
        """
        return sum(list(self.__cards_amount_per_letter.values()))

    def get_random_cards(self, num: int, exceptions: list = []) -> list:
        """
        Get random cards and return as list of Cards

        :param num: number of cards to catch
        :param exceptions: letters that can't be catched

        :return: list of Cards objects
        """
        print(f'Running get_random_cards to catch: {num} cards with the following exceptions: {exceptions}')
        print(f'Número de cards pedidos')
        if self.get_cards_amount() >= num:
            # Calculating if there's card enough without exceptions
            dict_copy = self.__cards_amount_per_letter.copy()

            to_be_removed = []
            # Excluding the exceptions
            for letter, amount in dict_copy.items():
                if amount == 0 or letter in exceptions:
                    to_be_removed.append(letter)

            [dict_copy.pop(letter) for letter in to_be_removed]
                
            # With the possible letters 
            if sum(list(dict_copy.values())) >= num:
                selected_cards = []

                for _ in range(num):
                    while True:
                        random_index = randint(0, len(dict_copy.keys()) - 1)
                        dict_list = list(dict_copy.keys())
                        letter = dict_list[random_index]
                        # If there's the selected card
                        # In case there's not, we will select another
                        if self.__cards_amount_per_letter[letter] > 0:
                            selected_cards.append(Card(letter))
                            self.__cards_amount_per_letter[letter] -= 1
                            dict_copy[letter] -= 1
                            if dict_copy[letter] == 0:
                                dict_copy.pop(letter)
                            break
                return selected_cards
            else:
                # Not enough cards without exceptions
                raise NotEnoughCardsOnBagException
        else:
            #Not enough cards
            raise NotEnoughCardsOnBagException
            
    # def exhange_cards(cards_list: list):
    #     exceptions = []
    #     for card in cards_list:
    #         exceptions.append(card.letter)
    #         del card
    #     cards_to_return = self.get_random_cards

    def get_cards_by_letters(self, letters: list) -> 'list[Card]':
        """
        Returns a list of cards considering the letter passed
        
        :params letters: list of letters to construct the cards
        :return: list of cards
        """

        # 1 - Card's quantity validation
        for letter in letters:
            if self.__cards_amount_per_letter[letter] == 0:
                raise NotEnoughCardsOnBagException
        # 2 - Getting cards
        cards = []
        for letter in letters:
            cards.append(Card(letter))
            self.__cards_amount_per_letter[letter] -= 1
        return cards
    
    def exchange_cards(self, cards: 'list[Card]') -> 'list[Card]':
        """
        Increments cards quantity and returns cards randomly selected from bag
        """
        print(f'Running exchange_cards for {cards}')
        
        # Get random cards
        exceptions_set = set()
        for card in cards:
            exceptions_set.add(card.letter)
        cards_return = self.get_random_cards(len(cards), list(exceptions_set))

        # Put cards that came from the parameter in the bag
        for card in cards:
            self.__cards_amount_per_letter[card.letter] += 1
            del card

        # print(self.__cards_amount_per_letter)
        return cards_return

    def __str__(self):
        return str(self.__cards_amount_per_letter)