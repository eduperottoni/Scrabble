class Player:
    def __init__(self):
        self.__id = ''
        self.__name = ''
        self.__is_turn = False
        self.__score = 0
        self.__dropouts = 0
        #TODO Criar o atributo pack
        #self.pack = Pack()

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name
    
    @property
    def is_turn(self):
        return self.__is_turn

    @property
    def score(self):
        return self.__score
    
    @property
    def dropouts(self):
        return self.__dropouts
    
    # @property
    # def pack(self):
        # return self.__pack

    @name.setter
    def name(self, name: str):
        self.__name = name

    @id.setter
    def id(self, id: str):
        self.__id = id

    @is_turn.setter
    def is_turn(self, is_turn: bool):
        self.__is_turn = is_turn
    
    @score.setter
    def score(self, score: int):
        self.__score = score

    @dropouts.setter
    def dropouts(self, dropouts: int):
        self.__dropouts = dropouts

    # @pack.setter
    # def pack(self, pack: Pack):
        # self.__pack = pack
    
    def reset(self) -> None:
        """
        Resets the player attributes (in case we start a new game) 
        """
        self.__name = ''
        self.__id = ''
        self.__is_turn = False
        self.__score = 0
        self.__dropouts = 0

    def initialize(self, id: str, name: str) -> None:
        """
        Resets the player and initializes her id and name

        :param id: str
        :param name: str
        """
        self.reset()
        self.__id = id
        self.__name = name

    def toogle_turn(self) -> None:
        """
        Change logically the is_turn attribute (change the turn of the match)
        """
        self.__is_turn = not self.is_turn
