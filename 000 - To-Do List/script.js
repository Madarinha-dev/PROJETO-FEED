const taskList = document.getElementById('taskList');
const taskInput = document.getElementById('taskInput');


// Função para adicionar tarefa na lista
function addTask() {
    // Variável para pegar o valor de 'taskInput' e guardar no
    // taskText
    const taskText = taskInput.value.trim();
    
    if (taskText != ""){

        const li = document.createElement("li");

        li.innerHTML = `
            <span> ${taskText} </span> <br>
            <button Class="editButton" id="comum" onClick="editTask(this)" > L </button>
            <button Class="deleteButton" onClick="deleteTask(this)" > X </button>
            <button class="colorToggleButton" onClick="toggleColor(this)"> V </button>
        `;
        taskList.appendChild(li);
        taskInput = "";
    }
}


function editTask(button) {
    // "parentElement = pegar o item da lista"
    const li = button.parentElement;
    const span = li.querySelector('span');
    const newText = prompt("Editar tarefa:", span.textContent);
    // span.textContent = pegar o valor (texto) que ta dentro
    // do SPAN;
    
    if (newText !== null && newText.trim() !== "") {
        span.textContent = newText.trim();
    }
}

function deleteTask(button) {
    const li = button.parentElement;
    taskList.removeChild(li);
}

function toggleColor(button) {
    const li = button.parentElement; // Pega o elemento <li> pai do botão
            // Obtém a cor de fundo atual computada pelo navegador
    const currentColor = window.getComputedStyle(li).backgroundColor;

            // Cores que representam azul e vermelho (RGB)
    const blueRGB = 'rgb(23, 23, 147)'; // Cor do Tailwind 'blue-500'
    const redRGB = '#00E084';   // Cor do Tailwind 'red-500'

            // Se a cor de fundo atual for azul, mude para vermelho.
            // Caso contrário, mude para azul.
    if (currentColor === blueRGB) {
        li.style.backgroundColor = redRGB; // Define para vermelho
    } else {
        li.style.backgroundColor = blueRGB; // Define para azul
    }
}
