from classes.trie import Trie

class Dictionary:
    def __init__(self):
        self.__valid_words = []
        self.__trie = Trie()
        self.__trie.load_file('src/dictionary/br-sem-acentos.txt')
        print('ÁRVORE CARREGADA')
    
    def is_valid(self, word: str) -> bool:
        # Verifies if the word is already valid
        return word in self.__valid_words
    
    def search_word(self, word: str) -> bool:
        # Calls the Trie.serch method
        return self.__trie.search(word)
    
    def set_new_valid_word(self, word: str):
        # Set new word already in board
        self.__valid_words.append(word)
