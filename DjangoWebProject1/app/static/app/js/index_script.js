
const overlayManual = document.getElementById('manualModal');

document.addEventListener('DOMContentLoaded', function () {


    var listView = document.querySelector('.list-view');
    var gridView = document.querySelector('.grid-view');
    var projectsList = document.querySelector('.project-boxes');






    listView.addEventListener('click', function () {
        gridView.classList.remove('active');
        listView.classList.add('active');
        projectsList.classList.remove('jsGridView');
        projectsList.classList.add('jsListView');
    });

    gridView.addEventListener('click', function () {
        gridView.classList.add('active');
        listView.classList.remove('active');
        projectsList.classList.remove('jsListView');
        projectsList.classList.add('jsGridView');
    });

    document.querySelector('.messages-btn').addEventListener('click', function () {
        document.querySelector('.messages-section').classList.add('show');
    });

    document.querySelector('.messages-close').addEventListener('click', function () {
        document.querySelector('.messages-section').classList.remove('show');
    });
});




function openUserManual(id) {
    console.log(id)
    overlayManual.classList.remove('closing');
    overlayManual.classList.add('active');
    // Очистим старые опции

    fetch(`/get_usermanual/${id}/`)
        .then(response => response.json())
        .then(data => {
            document.getElementById("manualTitle").innerText = data.title;
            document.getElementById("manualContent").innerHTML = data.content;
            document.getElementById("manualModal").style.display = "flex";
        });
}

function closeManual() {
    document.getElementById("manualModal").style.display = "none";
}