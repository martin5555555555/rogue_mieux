from glob import glob
from flask import Flask, g, render_template, make_response
from flask_socketio import SocketIO
from flask import request
from numpy import diff
from pyparsing import *
import requests
from game_backend import Game, player
import uuid

from game_backend.Projectiles import Fireball

app = Flask(__name__)
socketio = SocketIO(app)
game = Game()


number_players = 0 
difficulte = 0
dico_correspondance = {}
info_partie = {'partie_en_cours': False, 'info_partie': {}}
partie_en_cours = {}
partie_des_joueurs = {}
direction = (0,0)


@app.route("/")
def index():
    global partie_en_cours
    map = game.getMap()
    temp  = render_template("proposition.html", parties = partie_en_cours)    
    return temp

@app.route("/newgame/<string:info_partie>")
def newgame(info_partie):
    print(info_partie)
    info_partie = info_partie.split('+')
    nom_partie = info_partie[0]
    print(nom_partie)
    global difficulte
    difficulte = int(info_partie[1])
    print('new game begins')
    game = Game()
    dico_correspondance = {}
    number_players = 0
    id_user = get_cookie_id_user()
    dico_correspondance[str(id_user)] = number_players
    number_players += 1
    game.add_player(str(id_user))
    for i in range (difficulte):
        game.add_monsters("monstre_1")

    global partie_des_joueurs
    partie_des_joueurs = {id_user: nom_partie}
    partie_en_cours[nom_partie] = game, dico_correspondance, number_players

    

    map = game.getMap()
    player = game._players[0]
    print(player._vie)
    temp  = render_template("index.html", mapdata =map, n_row=len(map), n_col=len(map[0]), vie = str(player._vie) )
    resp = make_response(temp)
    return resp

@app.route("/partie/<string:nom_partie>")
def join_partie(nom_partie):
    game, dico_correspondance, number_players = partie_en_cours[nom_partie] 
    id_user = get_cookie_id_user()
    if id_user not in dico_correspondance.keys():
        dico_correspondance[str(id_user)] = number_players
        number_players += 1
        game.add_player(str(id_user))
    
    partie_en_cours[nom_partie] = game, dico_correspondance, number_players
    partie_des_joueurs[id_user] = nom_partie
    map = game.getMap()
    player = game._players[dico_correspondance[id_user]]
    if not player._is_alive:
        temp = render_template("die.html")
    else :
        temp  = render_template("index.html", mapdata =map, n_row=len(map), n_col=len(map[0]), vie = str(player._vie) )
    return temp


@app.route("/choix_new_partie/")   
def choix_new_partie():
     temp = render_template("new_partie.html")
     return temp


@socketio.on("move")
def on_move_msg(json, methods=["GET", "POST"]):
    print("received move ws message")
    global direction
    dx = json['dx']
    dy = json["dy"]
    direction = (dx, dy)
    id_user = json["id_user"]
    print(partie_des_joueurs)
    nom_partie = partie_des_joueurs[id_user]
    game, dico_correspondance, number_players = partie_en_cours[nom_partie]
    print(dico_correspondance)
    numero_joueur = dico_correspondance[id_user]
    
    data, ret, animation_json, die = game.move(dx,dy, numero_joueur)
    
    if die:
        socketio.emit("die")

    if ret:
        socketio.emit("response", data)
        socketio.emit("animation", animation_json )
    
@socketio.on("shot")
def ignit_fireball(json):
    global direction
    print("ignition")
    id_user = json["id_user"]
    dx = direction[0]
    dy = direction[1]
    print(id_user)
    nom_partie = partie_des_joueurs[id_user]
    game, dico_correspondance, number_players = partie_en_cours[nom_partie]
    print(dico_correspondance)
    numero_joueur = dico_correspondance[id_user]
    player = game._players[numero_joueur]
    fireball = Fireball("fireball")
    fireball.init_placement(player, direction)
    map = game.getMap()
    x = fireball._x
    y = fireball._y
    data = {"x" : str(x), "y": str(y), "dx" :str(dx), "dy" :str(dy), "className" : fireball._className, "x_max" : str(len(map)), "y_max" : str(len(map[0]))}
    socketio.emit("ignit_fireball", data)
    



@app.route("/die/")
def die():
    temp = render_template("die.html")
    return temp


@socketio.on("deconnection")
def on_connection_msg(json, methods=["GET", "POST"]):
    print("received connection ws message")
    global number_players
    global dico_correspondance
    global domain_lists
    

@socketio.on("monster touched")
def monster_hurt(json):
    print("monster touched")
    id_user = json["id_user"]
    x = int(json["x"])
    y = int(json["y"])
    print(id_user)
    nom_partie = partie_des_joueurs[id_user]
    game, dico_correspondance, number_players = partie_en_cours[nom_partie]
    print(x,y)
    monster = game.find_monsters(x,y)
    monster_die, data = monster.is_hurt(100, game.getMap())
    print(monster._vie)
    if monster_die:
        socketio.emit("monster_died", data)
    
    


def setcookie(resp):
    id_user = uuid.uuid1()
    global dico_correspondance
    global number_players
    dico_correspondance[str(id_user)] = number_players
    number_players += 1
    game.add_player(str(id_user))
    print(dico_correspondance)


    
    resp.set_cookie('id_user', str(id_user))
    return resp

def get_cookie_id_user():
   username = request.cookies.get('id_user')
   return username

@app.route('/cookie/', methods = ['POST', 'GET'])
def cookie():
        resp = requests.request("POST", 'http://127.0.0.1:5001/set-cookie/')
        return resp




 
        

if __name__=="__main__":
    socketio.run(app, port=5001)


