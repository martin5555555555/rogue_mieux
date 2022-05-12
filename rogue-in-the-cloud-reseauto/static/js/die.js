

window.addEventListener("DOMContentLoaded", (event) => {
    var restart = document.getElementById('restart');
    
    restart.onclick = function(e) {
        console.log('restart')

        window.location = 'http://127.0.0.1:5001/'
    }


         
        
    })