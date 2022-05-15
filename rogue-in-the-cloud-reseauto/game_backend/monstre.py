from re import A
from socket import socket
import numpy as np

class Monstre:
    
    def __init__(self, name):
        self._x = 0
        self._y = 0 
        self._name = name

    def die(self, map, symbole_monstre_mort):
        map[self._x][self._y] = symbole_monstre_mort
    

class Monstre_1(Monstre):
    def __init__(self, name):
        super().__init__(name)
        self._vie = 100
        self._range = 2
        self._damage = 10
        self._symbole = "O"
        self._className = "monster"
    
    def place(self, map):
        map[self._x][self._y] = self._symbole

    def init_placement(self, map):
        n_row = len(map)
        n_col = len(map[0])
        stop = False
        trials = 0
        while not stop :
            x = np.random.randint(0,n_row)
            y = np.random.randint(0, n_col)
            if map[x][y] == '.':
                stop = True
                print('placé')
            else :
                trials +=1
           
        self._x = x
        self._y = y
        self.place(map)

    def animation(self, game):
        map = game.getMap()
        map_inter = map.copy()
        x_max = len(map)
        y_max = len(map[0])
        x = self._x
        y = self._y
        alentours_x = [x-1, x, x+1]
        alentours_y = [y-1, y, y+1]
        for x in alentours_x:
            for y in alentours_y:
                if x<x_max and y<y_max:
                    map_inter[x][y] = 'O'
        game._map = map_inter
    def is_hurt(self, damage, map):
        self._vie += - damage
        if self._vie <=0:
            return self.die(map) 
        else:
            return False, {}
        
          

    def die(self, map):
        self._symbole = 'T'
        self._damage = 0
        map[self._x][self._y] = self._symbole
        return True, {"x": self._y, "y": self._x, "symbole": self._symbole}



    
        
        


