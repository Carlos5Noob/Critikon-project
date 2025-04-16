document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".form-eliminar").forEach(form => {
        form.addEventListener("submit", e => {
            if (!confirm("¿Estás seguro de que quieres eliminar esta reseña?")) {
                e.preventDefault();
            }
        });
    });
});
