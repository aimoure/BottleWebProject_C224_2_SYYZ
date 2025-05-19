
function generateMatrix(n) {
    // Находим контейнер для таблицы
    const container = document.getElementById('matrix-container');
    // Чистим если там уже была таблица
    container.innerHTML = '';

    // Создаём HTML-таблицу вручную (
    const table = document.createElement('table');
    table.border = "1";             // Внешняя рамка таблицы
    table.cellPadding = "5";        // Отступы внутри ячеек
    table.cellSpacing = "0";        // Расстояние между ячейками (0 = плотно)

    // Генерация первой строки с подписями (пустая ячейка + заголовки столбцов)
    const headerRow = document.createElement('tr');
    const corner = document.createElement('th');
    corner.innerHTML = ''; // верхний левый угол
    headerRow.appendChild(corner);

    // Создаём заголовки столбцов (m1, m2, ..., mn)
    for (let j = 0; j < n; j++) {
        const th = document.createElement('th'); // Заголовочная ячейка
        const input = document.createElement('input'); // Внутри будет input

        input.type = 'text';                    // Текстовое поле — пользователь может переименовать
        input.name = `label-x${j}`;             // Имя поля, для формы (например: label-x0)
        input.value = `m${j + 1}`;              // Значение по умолчанию: m1, m2, m3...

        input.style.width = '60px';
            input.style.padding = '0';
        input.style.border = 'none'; 
        input.style.outline = 'none';
        input.style.textAlign = 'center';
        input.required = true;

        // Кладём input внутрь заголовочной ячейки
        th.appendChild(input);
        headerRow.appendChild(th);
    }

    table.appendChild(headerRow);

    // Генерация остальных строк (с подписями строк слева и ячейками ввода)
    for (let i = 0; i < n; i++) {
        const tr = document.createElement('tr');

        const labelCell = document.createElement('th');
        const labelInput = document.createElement('input');
        labelInput.type = 'text';
        labelInput.name = `label-y${i}`;
        labelInput.value = `w${i + 1}`;
        labelInput.style.width = '60px';
            
        labelInput.style.margin = '0';
        labelInput.style.padding = '0';
        labelInput.style.border = 'none'; 
        labelInput.style.outline = 'none';

        labelInput.style.textAlign = 'center';
        labelInput.required = true;
        labelCell.appendChild(labelInput);
        tr.appendChild(labelCell);

        for (let j = 0; j < n; j++) {
            const td = document.createElement('td');
            const input = document.createElement('input');
            input.type = 'number';
            input.name = `matrix-${i}-${j}`;
            input.value = 0;
            input.min = 0;        // запретить отрицательные числа
            input.max = 1000;     // ограничить сверху
            input.step = 1;       // только целые числа
            input.style.margin = '0';
            input.style.padding = '0';
            input.style.border = 'none'; 
            input.style.outline = 'none';
            input.style.textAlign = 'center';
            input.style.width = '60px';
            input.required = true;
            td.appendChild(input);
            tr.appendChild(td);
        }

        table.appendChild(tr);
    }

    container.appendChild(table);
}

document.getElementById('size').addEventListener('input', function () {
    const size = parseInt(this.value); // Получаем значение из поля ввода
    if (size >= 2 && size <= 10) {
        generateMatrix(size); // Если размер в допустимых пределах, строим таблицу
    }
});

// Строим таблицу с дефолтными размерами
window.onload = function () {
    const sizeInput = document.getElementById('size');
    generateMatrix(parseInt(sizeInput.value));
}


document.getElementById('uploadRandomBtn').addEventListener('click', function () {
    const size = parseInt(document.getElementById('size').value);
    if (isNaN(size) || size < 2 || size > 10) {
        alert('Размер матрицы должен быть от 2 до 10');
        return;
    }

    for (let i = 0; i < size; i++) {
        for (let j = 0; j < size; j++) {
            const input = document.querySelector(`input[name="matrix-${i}-${j}"]`);
            if (input) {
                input.value = Math.floor(Math.random() * 101); // 0-100
            }
        }
    }
});



