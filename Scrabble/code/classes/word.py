from classes.position import Position

class Word:
    def __init__(self):
        self.__positions = []
        self.__direction = ''

    @property
    def positions(self):
        return self.__positions
    
    @property
    def direction(self):
        return self.__direction

    @direction.setter
    def direction(self, direction: str):
        self.__direction = direction    
    
    def add_position(self, position: Position):
        self.__positions.append(position)
    
    def get_min_max_positions(self) -> 'tuple(Position, Position)':
        """
        Sort the positions array based on the coordinates attribute

        :returns tuple<Position, Position>: 
        """
        
        self.__positions = sorted(self.__positions, key=lambda position: position.coordinate[0] if self.__direction == "horizontal" else position.coordinate[1])
        min_position = self.positions[0]
        max_position = self.positions[-1]

        print(f"A POSIÇÃO MAX É: {max_position.card.letter}, e a posição MIN é {min_position.card.letter}")

        return (min_position, max_position)

    def get_string(self) -> str:
        """
        Returns the Word in string format based on the Position.card.letter attribute

        :return string: The string of the word
        """
        string = ''
        for position in self.__positions:
            string += position.card.letter
        return string
