document.querySelector('.more-button').addEventListener('click', function () {
    document.querySelector('.list-container').classList.toggle('active');
});

const openBtn = document.getElementById('openModalBtn');
const openBtn2 = document.getElementById('openModal2Btn');
const closeBtn = document.getElementById('closeModalBtn');
const closeBtn2 = document.getElementById('closeModal2Btn');
const overlay = document.getElementById('modalOverlay');
const overlay2 = document.getElementById('modalOverlay2');

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
openBtn2.addEventListener('click', () => {
    overlay2.classList.remove('closing');
    overlay2.classList.add('active');
    // Очистим старые опции
    const serviceSelect = document.getElementById('service');
    serviceSelect.innerHTML = '<option value="" disabled selected>Выберите услугу</option>';
    loadKE(); // Загружаем КЕ

});

function closeModal() {
    overlay.classList.add('closing');
    overlay.classList.remove('active');

    // Удалим класс 'closing' после завершения анимации
    setTimeout(() => {
        overlay.classList.remove('closing');
    }, 300); // должно совпадать с transition: 0.3s
}
function closeModal2() {
    overlay2.classList.add('closing');
    overlay2.classList.remove('active');

    // Удалим класс 'closing' после завершения анимации
    setTimeout(() => {
        overlay2.classList.remove('closing');
    }, 300); // должно совпадать с transition: 0.3s
}

closeBtn.addEventListener('click', closeModal);
closeBtn2.addEventListener('click', closeModal2);

overlay.addEventListener('click', (e) => {
    if (e.target === overlay) {
        closeModal();
    }
});
overlay2.addEventListener('click', (e) => {
    if (e.target === overlay) {
        closeModal();
    }
});


function loadKE() {
    fetch('/get_KE')  // путь должен совпадать с маршрутом Django
        .then(response => response.json())
        .then(data => {
            const tableBody = document.querySelector('#modalOverlay2 tbody');
            tableBody.innerHTML = ''; // очищаем старые строки

            // Строка заголовков
            const headerRow = document.createElement('tr');
            headerRow.innerHTML = `
                <th>Название</th>
                <th>Инв номер</th>
                <th>Класс</th>
            `;
            tableBody.appendChild(headerRow);

            // Добавляем данные
            data.components.forEach(item => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td data-th="Название">${item.NAME}</td>
                    <td data-th="Инв номер">${item.INV}</td>
                    <td data-th="Класс">${item.CLASS}</td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Ошибка загрузки КЕ:', error);
        });
}


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
