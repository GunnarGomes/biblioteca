

var pass = document.querySelector('#password')

setInterval(function (){
    if (pass.type == 'password') {
        document.getElementById('password').style.display = 'block'
        console.log('ok')
    }else {
        document.getElementById('password').style.display = 'none'
        pass.type = 'password'
    }
},10)

addEventListener('contextmenu', function (ev){
    ev.preventDefault()
})

(function() {
    function detectDevTools() {
        const start = performance.now();
        debugger; // O DevTools irá pausar aqui se estiver aberto
        const end = performance.now();
        if (end - start > 100) { 
            window.location.href = "https://google.com"; // Redireciona para outra página
        }
    }

    setInterval(detectDevTools, 1000); // Verifica a cada segundo
})();