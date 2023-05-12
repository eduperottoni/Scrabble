from classes.card import Card

class Bag:
    def __init__(self, cards_quantity_by_letter: dict):
        """
        Constructor make a card's dictionary
        keys: letters (A-Z)
        values: card's values (1-8)

        :param cards_quantity_by_letter: dictionary containing
        keys: letters (A-Z)
        values: quantity of cards with this letter
        """
        self.__cards_dict = {}

        '''É desnecessário armazenar os objetos, uma vez que podemos
        apenas criá-los no momento necessário. Portanto, armazenamos
        apenas a quantdade de cada um atualizada na bag. Quando solicitados
        novos cards, eles são criados.
        '''
        for letter, quantity in cards_quantity_by_letter.items():
            self.__cards_dict[f'{letter}'] = quantity

        print(self.__cards_dict)