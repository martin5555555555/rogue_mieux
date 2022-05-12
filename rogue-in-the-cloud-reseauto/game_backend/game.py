from .map_generator import Generator
from .player import Player
from .monstre import Monstre_1

 
class Game:
    def __init__(self, width=96, height=32):
        self._generator = Generator(width=width, height=height)
        self._generator.gen_level()
        self._generator.gen_tiles_level()
        self._map = self._generator.tiles_level
        self._players = []
        self._monsters = []
        
    def getMap(self):
        return self._map

    def move(self, dx, dy, numero_player):
        animation = {"name": ""}
        die = False #le joueur n'est pas mort
        player = self._players[numero_player]
        data, ret = player.move(dx, dy, self._map)
        new_x = player._x
        new_y = player._y
        #check monstre:
        for monster in self._monsters:
            x = monster._x
            y = monster._y
            print(abs(x-new_y))
            if (abs(x-new_y) < monster._range) and (abs(y - new_x) < monster._range):
                print('zone de danger')
                json = {"name" : monster._name, "range" : str(monster._range), "x":str(monster._x), "y": str(monster._y)}
                animation =  json

                player._vie += - monster._damage
                print(player._vie)

            if player._vie <= 0 :
                player.die(self._map)
                die = True
                    
        return data, ret, animation, die
    
    
    def add_player(self, id_user):
        self._players.append(Player(id_user))
        self._players[-1].initPos(self._map)
    
    def add_monsters(self, name):
        if name == "monstre_1":
            monster = Monstre_1("monstre_1")
            monster.init_placement(self._map)
            self._monsters.append(monster)
    
   
    
        
    