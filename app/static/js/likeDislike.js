document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".like-btn").forEach(button => {
        button.addEventListener("click", function () {
            const opinionId = this.dataset.opinionId;
            const likeUrl = this.dataset.likeUrl;

            fetch(likeUrl, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCSRFToken(),
                    "X-Requested-With": "XMLHttpRequest"
                }
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById(`likes-count-${opinionId}`).textContent = data.likes;
                document.getElementById(`dislikes-count-${opinionId}`).textContent = data.dislikes;
            })
            .catch(error => console.error("Error:", error));
        });
    });

    document.querySelectorAll(".dislike-btn").forEach(button => {
        button.addEventListener("click", function () {
            const opinionId = this.dataset.opinionId;
            const dislikeUrl = this.dataset.dislikeUrl;

            fetch(dislikeUrl, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCSRFToken(),
                    "X-Requested-With": "XMLHttpRequest"
                }
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById(`likes-count-${opinionId}`).textContent = data.likes;
                document.getElementById(`dislikes-count-${opinionId}`).textContent = data.dislikes;
            })
            .catch(error => console.error("Error:", error));
        });
    });
});
