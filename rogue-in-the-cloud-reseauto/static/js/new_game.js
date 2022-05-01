

window.addEventListener("DOMContentLoaded", (event) => {
    var input_nom_partie = document.getElementById('nom_partie');
    
    var start_new_game = document.getElementById("start");
    start_new_game.onclick = function(e) {
        var nom_partie = input_nom_partie.value;
        console.log(nom_partie);
        console.log('a')

        window.location = `http://127.0.0.1:5001/newgame/${nom_partie}`
    }


         
        
    })