(function() {
    // 🔒 Bloqueia F12, Ctrl+Shift+I, Ctrl+Shift+J e Ctrl+U
    document.addEventListener("keydown", function(event) {
        if (
            event.key === "F12" ||
            (event.ctrlKey && event.shiftKey && (event.key === "I" || event.key === "J")) ||
            (event.ctrlKey && event.key === "U")
        ) {
            event.preventDefault();
        }
    });

    // 🔍 Detecta o DevTools aberto usando `debugger`
    function detectDevTools() {
        const start = performance.now();
        debugger; // Se o DevTools estiver aberto, há um delay aqui
        const end = performance.now();
        if (end - start > 100) { 
            window.location.href = "https://google.com"; // Redireciona
        }
    }

    // 🔍 Detecta se o console está aberto
    function detectConsole() {
        let devtools = false;
        const element = new Image();
        Object.defineProperty(element, 'id', {
            get: function() {
                devtools = true;
                window.location.href = "https://google.com"; // Redireciona
            }
        });
        console.log('%c', element);
    }

    // 🔄 Verifica DevTools e Console a cada 1s
    setInterval(() => {
        detectDevTools();
        detectConsole();
    }, 100);

    // 📏 Detecta mudanças suspeitas no tamanho da janela
    window.addEventListener('resize', function() {
        if (window.outerWidth - window.innerWidth > 160) {
            window.location.href = "https://google.com";
        }
    });

})();
