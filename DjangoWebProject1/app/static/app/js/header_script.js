document.querySelector('.more-button').addEventListener('click', function () {
    document.querySelector('.list-container').classList.toggle('active');
});

const openBtn = document.getElementById('openModalBtn');
const closeBtn = document.getElementById('closeModalBtn');
const overlay = document.getElementById('modalOverlay');

openBtn.addEventListener('click', () => {
    overlay.classList.remove('closing');
    overlay.classList.add('active');
    // Очистим старые опции
    const serviceSelect = document.getElementById('service');
    serviceSelect.innerHTML = '<option value="" disabled selected>Выберите услугу</option>';

    // Загрузим новые
    fetch('/api/services/')
        .then(response => response.json())
        .then(data => {
            data.services.forEach(service => {
                const option = document.createElement('option');
                option.value = service.uuid;
                option.textContent = service.name;
                serviceSelect.appendChild(option);
            });
        })
        .catch(error => {
            console.error('Ошибка при загрузке услуг:', error);
        });
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


    document.addEventListener("DOMContentLoaded", function () {
    const serviceSelect = document.getElementById("service");
    const componentSelect = document.getElementById("component");

    serviceSelect.addEventListener("change", function () {
        const serviceUuid = this.value;
    componentSelect.innerHTML = '<option value="">Загрузка...</option>';
    componentSelect.disabled = true;

    if (serviceUuid) {
        fetch(`/get_components/?uuid=${serviceUuid}`)
            .then(response => response.json())
            .then(data => {
                componentSelect.innerHTML = '<option value="">-- Выберите состав --</option>';
                data.components.forEach(comp => {
                    const opt = document.createElement("option");
                    opt.value = comp.uuid;
                    opt.textContent = comp.name;
                    componentSelect.appendChild(opt);
                });
                componentSelect.disabled = false;
            })
            .catch(() => {
                componentSelect.innerHTML = '<option>Ошибка загрузки</option>';
            });
        } else {
        componentSelect.innerHTML = '<option value="">-- Сначала выберите услугу --</option>';
        }
    });
});
