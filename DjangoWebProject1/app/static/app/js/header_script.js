document.querySelector('.more-button').addEventListener('click', function () {
    document.querySelector('.list-container').classList.toggle('active');
});

const openBtn = document.getElementById('openModalBtn');
const closeBtn = document.getElementById('closeModalBtn');
const overlay = document.getElementById('modalOverlay');

openBtn.addEventListener('click', () => {
    overlay.classList.remove('closing');
    overlay.classList.add('active');
});

function closeModal() {
    overlay.classList.add('closing');
    overlay.classList.remove('active');

    // Удалим класс 'closing' после завершения анимации
    setTimeout(() => {
        overlay.classList.remove('closing');
    }, 300); // должно совпадать с transition: 0.3s
}

closeBtn.addEventListener('click', closeModal);
overlay.addEventListener('click', (e) => {
    if (e.target === overlay) {
        closeModal();
    }
});