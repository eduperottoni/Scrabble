from classes.position import Position
import json

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
    
    @positions.setter
    def positions(self, positions: list):
        self.__positions = positions

    def add_position(self, position: Position):
        self.__positions.append(position)
    
    def get_min_max_positions(self) -> 'tuple(Position, Position)':
        """
        Sort the positions array based on the coordinates attribute

        :returns tuple<Position, Position>: 
        """  
        self.__positions = sorted(self.__positions, key=lambda position: position.coordinate[1] if self.__direction == "horizontal" else position.coordinate[0])
        min_position = self.positions[0]
        max_position = self.positions[-1]
        
        for h in self.__positions:
            print(h.coordinate)

        print(f"A POSIÇÃO MAX É: {max_position.coordinate}, e a posição MIN é {min_position.coordinate}")

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
    
    def reset(self):
        positions = [position for position in self.__positions]
        self.__positions = []
        self.__direction = ''
        return positions
    
    def convert_to_json(self):
        move_dict = {'string': self.get_string(), 'positions': [p.coordinate for p in self.__positions]}
        json_string =  json.dumps(move_dict)
        _json = json.loads(json_string)
        return _json