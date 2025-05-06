document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".boton-seguir").forEach(boton => {
        boton.addEventListener("click", function () {
            const userId = this.dataset.userId;
            const url = this.dataset.url;

            fetch(url, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCSRFToken(),
                    "X-Requested-With": "XMLHttpRequest"
                }
            })
            .then(response => response.json())
            .then(data => {
                const botones = document.querySelectorAll(`.boton-seguir[data-user-id='${userId}']`);
                botones.forEach(btn => {
                    if (data.seguido) {
                        btn.textContent = "Seguido";
                        btn.classList.remove("btn-secondary");
                        btn.classList.add("btn-success");
                    } else {
                        btn.textContent = "Seguir";
                        btn.classList.remove("btn-success");
                        btn.classList.add("btn-secondary");
                    }
                });
            })
            .catch(error => console.error("Error:", error));
        });
    });
});
