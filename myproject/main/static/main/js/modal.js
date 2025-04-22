document.addEventListener("DOMContentLoaded", () => {
    const modal = document.getElementById('confirmModal');
    const modalText = document.getElementById('modalText');
    const confirmBtn = document.getElementById('confirmDelete');
    const cancelBtn = document.getElementById('cancelDelete');

    let deleteUrl = "";

    document.querySelectorAll('.delete-user').forEach(link => {
        link.addEventListener('click', e => {
            e.preventDefault();
            deleteUrl = link.href;
            modalText.textContent = `Вы уверены, что хотите удалить пользователя "${link.dataset.username}"?`;
            modal.style.display = 'block';
        });
    });

    confirmBtn.addEventListener('click', () => {
        window.location.href = deleteUrl;
    });

    cancelBtn.addEventListener('click', () => {
        modal.style.display = 'none';
    });
});
