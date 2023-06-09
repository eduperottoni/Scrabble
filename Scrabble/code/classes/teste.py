from random import randint

CARDS_QUANTITY_BY_LETTER = {
    'A': 14,
    'B': 3,
    'C': 4,
    'D': 2,
    'E': 11,
    'F': 2,
    'G': 2,
    'H': 2,
    'I': 10,
    'J': 1,
    'L': 4,
    'M': 6,
    'N': 4,
    'O': 10,
    'P': 4,
    'Q': 1,
    'R': 6,
    'S': 8,
    'T': 5,
    'U': 7,
    'V': 2,
    'X': 1,
    'Z': 1
}

CARDS_QUANTITY_BY_LETTER = {
    'A': 0,
    'B': 0,
    'C': 0,
    'D': 5,
    'E': 2,
    'F': 2,
    'G': 0,
    'H': 0,
    'I': 0,
    'J': 0,
    'L': 0,
    'M': 0,
    'N': 0,
    'O': 0,
    'P': 0,
    'Q': 0,
    'R': 0,
    'S': 0,
    'T': 0,
    'U': 0,
    'V': 0,
    'X': 0,
    'Z': 0
}


def get_cards_amount() -> int:
    return sum(list(CARDS_QUANTITY_BY_LETTER.values()))

# TODO nesse caso, retorna lista de letras, mas deve devolver uma lista de cards
def get_random_cards(num: int, exceptions: 'list[str]') -> 'list[str]':
    print(f'Running get_random_cards to catch: {num} cards with the following exceptions: {exceptions}')
    if get_cards_amount() >= num:
        # Calculating if there's card enough without exceptions
        dict_copy = CARDS_QUANTITY_BY_LETTER.copy()
        dict_copy.pop('A')

        print(CARDS_QUANTITY_BY_LETTER)
        print(dict_copy)

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
                    if CARDS_QUANTITY_BY_LETTER[letter] > 0:
                        selected_cards.append(letter)
                        CARDS_QUANTITY_BY_LETTER[letter] -= 1
                        dict_copy[letter] -= 1
                        if dict_copy[letter] == 0:
                            dict_copy.pop(letter)
                        break

            print('&'*30)
            print(CARDS_QUANTITY_BY_LETTER)
            print('&'*30)
            print(dict_copy)
            print('&'*30)
            return selected_cards
        else:
            # Not enough cards without exceptions
            print('Não há cards suficientes para a troca')
    else:
        #Not enough cards
        print('Não dá pra trocar')

cards = get_random_cards(7, ['B', 'C', 'D'])
print(cards)