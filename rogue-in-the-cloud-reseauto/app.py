from flask import Flask, render_template, make_response
from flask_socketio import SocketIO
from flask import request
from pyparsing import null_debug_action
import requests
from game_backend import Game
import uuid

app = Flask(__name__)
socketio = SocketIO(app)
game = Game()


number_players = 0 
dico_correspondance = {}
info_partie = {'partie_en_cours': False, 'info_partie': {}}
partie_en_cours = {}
partie_des_joueurs = {}


@app.route("/")
def index():
    global partie_en_cours
    map = game.getMap()
    temp  = render_template("proposition.html", parties = partie_en_cours)    
    return temp

@app.route("/newgame/<string:nom_partie>")
def newgame(nom_partie):
    print('new game begins')
    game = Game()
    dico_correspondance = {}
    number_players = 0
    id_user = get_cookie_id_user()
    dico_correspondance[str(id_user)] = number_players
    number_players += 1
    game.add_player(str(id_user))
    global partie_des_joueurs
    partie_des_joueurs = {id_user: nom_partie}
    partie_en_cours[nom_partie] = game, dico_correspondance, number_players

    

    map = game.getMap()
    temp  = render_template("index.html", mapdata =map, n_row=len(map), n_col=len(map[0]) )
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
    temp  = render_template("index.html", mapdata =map, n_row=len(map), n_col=len(map[0]) )
    return temp


@app.route("/choix_new_partie/")   
def choix_new_partie():
     temp = render_template("new_partie.html")
     return temp


@socketio.on("move")
def on_move_msg(json, methods=["GET", "POST"]):
    print("received move ws message")
    dx = json['dx']
    dy = json["dy"]
    id_user = json["id_user"]
    print(partie_des_joueurs)
    nom_partie = partie_des_joueurs[id_user]
    game, dico_correspondance, number_players = partie_en_cours[nom_partie]
    print(dico_correspondance)
    numero_joueur = dico_correspondance[id_user]
    
    data, ret = game.move(dx,dy, numero_joueur)
    if ret:
        socketio.emit("response", data)

@socketio.on("memorize")



@socketio.on("deconnection")
def on_connection_msg(json, methods=["GET", "POST"]):
    print("received connection ws message")
    global number_players
    global dico_correspondance
    global domain_lists
    
    
    

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


