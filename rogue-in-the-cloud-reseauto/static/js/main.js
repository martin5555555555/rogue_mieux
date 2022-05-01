function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for(let i = 0; i <ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
  }

window.addEventListener("DOMContentLoaded", (event) => {
    var socket = io.connect("http://" + document.domain + ":" + location.port );
    socket.emit("connection", {domain : document.domain})
    id_user = getCookie("id_user")
    console.log(id_user)

    document.onkeydown = function(e){
        switch(e.keyCode){
            case 37:
                socket.emit("move", {dx:-1, dy:0, id_user : id_user});
                break;
            case 38:
                socket.emit("move", {dx:0, dy:-1, id_user : id_user});
                break;
            case 39:
                socket.emit("move", {dx:1, dy:0, id_user: id_user});
                break;
            case 40:
                socket.emit("move", {dx:0, dy:1, id_user : id_user});
                console.log(id_user)
                break;
        }


    };
    
    var btn_n = document.getElementById("go_n");
    btn_n.onclick = function(e) {
        console.log("Clicked on button north");
        socket.emit("move", {dx:0, dy:-1, id_user: id_user});
        socket.emit("move", {dx:0, dy:-1});
        var audio = document.getElementById("music");
        audio.play();
    };

    var btn_s = document.getElementById("go_s");
    btn_s.onclick = function(e) {
        console.log("Clicked on button south");
        socket.emit("move", {dx:0, dy:1, id_user: id_user});
        var audio = document.getElementById("music");
        audio.play();
    };

    var btn_w = document.getElementById("go_w");
    btn_w.onclick = function(e) {
        console.log("Clicked on button w");
        socket.emit("move", {dx:-1, dy:0, id_user: id_user});
        var audio = document.getElementById("music");
        audio.play();
    };

    var btn_e = document.getElementById("go_e");
    btn_e.onclick = function(e) {
        console.log("Clicked on button e");
        socket.emit("move", {dx:1, dy:0, id_user: id_user});
        var audio = document.getElementById("music");
        audio.play();
    };


    socket.on("response", function(data){
        console.log(data);
        for( var i=0; i<2; i++){
            var cell_id = "cell " + data[i].i + "-" + data[i].j;
            var span_to_modif = document.getElementById(cell_id);
            span_to_modif.textContent = data[i].content;
        }
    });

    

    

});



