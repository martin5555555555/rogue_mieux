function uuidv4() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}


function setCookie(cname, cvalue, exdays) {
  const d = new Date();
  d.setTime(d.getTime() + (exdays*24*60*60*1000));
  let expires = "expires="+ d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

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
    return "undefined_id";
  }

window.addEventListener("DOMContentLoaded", (event) => {
    var socket = io.connect("http://" + document.domain + ":" + location.port );
    console.log("coucou")
 

    var id_user = getCookie("id_user")
    console.log(id_user) 
    if (id_user = "undefined_id"){
      var id_user = uuidv4();
      console.log(id_user + 'djkfk')
      setCookie("id_user", id_user, 7 )
    }
    var partie_en_cours = getCookie("partie_en_cours")
    console.log(partie_en_cours)
    info_game = getCookie("info_game")
    console.log(info_game)
   
    for (btn of document.getElementsByTagName("button") ){
      console.log(btn.id)
      btn.onclick = function(e) {
        console.log("Clicked on button partie existante");
        socket.emit("partie existante", {partie: btn.id});
        console.log(btn.innerHTML)
        window.location =  `http://127.0.0.1:5001/partie/${btn.id}`
    }
  }
    var btn_new = document.getElementById("new");    
    btn_new.onclick = function(e) {
        console.log("Clicked on button new");
        window.location ="http://127.0.0.1:5001/choix_new_partie/ "
    }

});