function CancionRandom() {
    let boton = document.getElementById("btn_control");
    let random = Math.floor(Math.random() * canciones.length);
    let reproductor = document.getElementById("reproductor");
    reproductor.src = canciones[random];
    reproductor.play();

    boton.style.display = "block";
    boton.textContent = "Detener música";
}

function ControlReproductor() {
    let reproductor = document.getElementById("reproductor");
    let boton = document.getElementById("btn_control");

    if (!reproductor.paused) {
        reproductor.pause();
        boton.textContent = "Reanudar música";
    } else {
        reproductor.play();
        boton.textContent = "Detener música";
    }
}

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("btn_reproductor").addEventListener("click", CancionRandom);
    document.getElementById("btn_control").addEventListener("click", ControlReproductor);
});
