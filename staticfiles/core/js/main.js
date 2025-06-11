function alertSonidoError(message) {
    console.log("Función alertSonidoError llamada");

    // Selecciona el elemento donde se mostrará el mensaje de error
    const errorSection = document.getElementById('error-section');
    
    // Comprueba si el elemento existe
    if (!errorSection) {
        console.error("No se encontró el elemento con id 'error-section'");
        return;
    }

    // Limpia cualquier mensaje de error anterior
    errorSection.innerHTML = '';

    // Crea un nuevo div para el mensaje de error
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert';
    alertDiv.textContent = message;

    // Añade el mensaje de error a la sección específica
    errorSection.appendChild(alertDiv);

    // Reproduce el sonido de alerta
    const audio = new Audio(audioURL_error);
    audio.play().then(() => {
        console.log("Sonido de alerta reproducido");
    }).catch((error) => {
        console.error("Error al reproducir el sonido de alerta:", error);
    });

    // Elimina el mensaje de error después de 3 segundos
    setTimeout(() => {
        errorSection.removeChild(alertDiv);
    }, 3000);
}

function showPopup(message) {
    console.log("Función showPopup llamada");

    // Selecciona la ventana emergente
    const popup = document.getElementById('popup');
    
    // Muestra el mensaje de error
    popup.textContent = message;

    // Reproduce el sonido de alerta, variable global audioURL_error proviene del template html que llama a la funcion

    const audio = new Audio(audioURL_error);
    audio.play();

    // Muestra la ventana emergente
    popup.style.display = 'block';

    // Oculta la ventana emergente después de 3 segundos
    setTimeout(() => {
        popup.style.display = 'none';
    }, 3000);
}

function alertSonidoError2(message) { 
    const alertDiv = document.createElement('error_section'); 

    // Comprueba si el elemento existe 
    if (!errorSection) { 
        console.error("No se encontró el elemento con id 'error-section'"); 
        return;
    }

    // Limpia cualquier mensaje de error anterior 
    errorSection.innerHTML = ''

    // Crea un nuevo div para el mensaje de error 
    //const alertDiv = document.createElement('div');

    alertDiv.className = 'alert'; 
    alertDiv.textContent = message; 
    document.body.appendChild(alertDiv); 
    const audio = new Audio("{% static 'core/sounds/beep-warning-6387.mp3' %}"); 
    audio.play().then(() => { 
        console.log("Sonido de alerta reproducido"); 
    }).catch((error) => { 
        console.error("Error al reproducir el sonido de alerta:", error); 
    }); 
    
    setTimeout(() => { document.body.removeChild(alertDiv); }, 3000);
}

function alertSonidoOk() { 
    const audio = new Audio(audioURL_ok); 
    audio.play(); 
}
