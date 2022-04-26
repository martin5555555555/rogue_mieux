from .map_generator import Generator
from .player import Player

 
class Game:
    def __init__(self, width=96, height=32):
        self._generator = Generator(width=width, height=height)
        self._generator.gen_level()
        self._generator.gen_tiles_level()
        self._map = self._generator.tiles_level
        self._players = []
        
    def getMap(self):
        return self._map

    def move(self, dx, dy, numero_player):
        return self._players[numero_player].move(dx, dy, self._map)
    
    def add_player(self, id_user):
        self._players.append(Player(id_user))
        self._players[-1].initPos(self._map)

    