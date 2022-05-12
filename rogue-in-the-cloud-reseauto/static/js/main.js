function pause(secondes){
let now = Date.now(),
      end = now + 1000 * secondes;
  while (now < end) { now = Date.now(); }
};
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
    console.log("coucou")
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
            case 27:
                socket.emit("shot", {id_user : id_user, dx: 0, dy: 1})
                console.log("shot lancé")
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
            console.log(cell_id);

            var span_to_modif = document.getElementById(cell_id);
            span_to_modif.textContent = data[i].content;
        }
        var aff_vie = document.getElementById("vie");
        aff_vie.textContent = data[2].vie
    });
    
    socket.on("ignit_fireball", async function(data){
        console.log("ignition fireball")
        console.log(data);
        var x = data.x
        var y = data.y
        var dx = data.dx
        var dy = data.dy
        var x_max = data.x_max
        var y_max = data.y_max
        var symbole = data.symbole

        x= `${parseInt(x)+parseInt(dx)}`;
            y= `${parseInt(y)+parseInt(dy)}`;

            var cell_id = "cell " + y + "-" + x;
            console.log(cell_id)
            var span_to_modif = document.getElementById(cell_id);
            var anciant_value = span_to_modif;
            console.log(anciant_value)
            span_to_modif.textContent = symbole;
            var restart = true;
        
        while (restart){ //&& (parseInt(x)< parseInt(y_max)-2) && (parseInt(y)< parseInt(x_max)-2)){
            console.log("fireball progressing");
            
            restart = false;
            console.log(restart)


            
            

            x= `${parseInt(x)+parseInt(dx)}`;
            y= `${parseInt(y)+parseInt(dy)}`;



                setInterval(
                () =>{
                var cell_id = "cell " + y + "-" + x;
                console.log(cell_id)
                var span_to_modif = document.getElementById(cell_id);
                console.log(anciant_value)
                span_to_modif.textContent = symbole;
                console.log("replace");
                anciant_value.textContent = '.'
                anciant_value = span_to_modif;
                x= `${parseInt(x)+parseInt(dx)}`;
                y= `${parseInt(y)+parseInt(dy)}`;
                
                console.log(x)


                
            },1000, `${parseInt(x)+parseInt(dx)}`, `${parseInt(y)+parseInt(dy)}`, anciant_value
            );
           
        

            
            };
        
        

        









      

    } )
    socket.on("die", function(){
        console.log("player died");
        window.location = 'http://127.0.0.1:5001/die/';

    }
    )

    

    

});



