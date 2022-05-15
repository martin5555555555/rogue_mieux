class Projectile:
    def __init__(self, name):
        self.name = name
        self._x = 0
        self._y = 0
   
class Fireball(Projectile):
    def __init__(self, name):
        super().__init__(name)
        self._symbole = "o"
        self._className = "fireball"

    def place(self, map):
        map[self._x][self._y] = self._symbole   
    def init_placement(self, player, direction):
        dx, dy = direction
        x_player = player._x
        y_player = player._y
        self._x = x_player + dx
        self._y = y_player + dy
    
    
