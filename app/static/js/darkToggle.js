document.addEventListener("DOMContentLoaded", function () {
    const toggleButton = document.getElementById("dark-mode-toggle");
    const body = document.body;

    if (localStorage.getItem("theme") === "dark") {
        body.classList.add("dark-mode");
    }

    toggleButton.addEventListener("click", function () {
        body.classList.toggle("dark-mode");
        localStorage.setItem("theme", body.classList.contains("dark-mode") ? "dark" : "light");
    });
});
