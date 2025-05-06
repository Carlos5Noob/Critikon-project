function toggleForm(opinionId) {
            let form = document.getElementById('comentario-form-' + opinionId);
            if (form.style.display === 'none') {
                form.style.display = 'block';
            } else {
                form.style.display = 'none';
            }
}