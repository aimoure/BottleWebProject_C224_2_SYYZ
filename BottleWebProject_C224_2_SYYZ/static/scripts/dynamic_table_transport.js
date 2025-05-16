// Функция для генерации таблицы транспортной задачи
// Принимаются параметры: rows (количество строк, т.е. поставщиков) и cols (количество столбцов, т.е. потребителей)
function generateMatrix(rows, cols) {
    // Находится контейнер с id="matrix-container", куда помещается таблица
    const container = document.getElementById('matrix-container');
    // Очищается содержимое контейнера для удаления предыдущей таблицы, если она была
    container.innerHTML = '';

    // Создается элемент таблицы <table>
    const table = document.createElement('table');
    // Устанавливаются атрибуты таблицы: граница, внутренние отступы, расстояние между ячейками
    table.border = "1";
    table.cellPadding = "5";
    table.cellSpacing = "0";

    // Создается строка заголовка таблицы
    const headerRow = document.createElement('tr');

    // Создается пустая ячейка в левом верхнем углу таблицы
    const emptyCell = document.createElement('th');
    // Добавляется пустая ячейка в строку заголовка
    headerRow.appendChild(emptyCell);

    // Генерируются заголовки столбцов (B1, B2, ..., Bn) для потребителей
    for (let j = 0; j < cols; j++) {
        // Создается ячейка заголовка столбца
        const th = document.createElement('th');
        // Устанавливается текст ячейки с нижним индексом (например, B₁, B₂)
        th.innerHTML = `B<sub>${j + 1}</sub>`;
        // Добавляется ячейка в строку заголовка
        headerRow.appendChild(th);
    }

    // Создается заголовок для столбца "Запасы"
    const supplyHeader = document.createElement('th');
    // Устанавливается текст "Запасы, a_i" с нижним индексом
    supplyHeader.innerHTML = 'Запасы, a<sub>i</sub>';
    // Добавляется заголовок столбца в строку
    headerRow.appendChild(supplyHeader);

    // Добавляется строка заголовка в таблицу
    table.appendChild(headerRow);

    // Генерируются строки таблицы для каждого поставщика (A1, A2, ..., Am)
    for (let i = 0; i < rows; i++) {
        // Создается новая строка таблицы
        const tr = document.createElement('tr');

        // Создается заголовок строки (например, A₁, A₂, ...)
        const rowHeader = document.createElement('th');
        // Устанавливается текст заголовка строки с нижним индексом
        rowHeader.innerHTML = `A<sub>${i + 1}</sub>`;
        // Добавляется заголовок в строку
        tr.appendChild(rowHeader);

        // Генерируются ячейки матрицы затрат (Cij) для текущей строки
        for (let j = 0; j < cols; j++) {
            // Создается ячейка для ввода значения затрат
            const td = document.createElement('td');
            // Создается поле ввода
            const input = document.createElement('input');
            // Устанавливается тип поля ввода как число
            input.type = 'number';
            // Задается имя поля ввода в формате matrix-i-j для обработки формы
            input.name = `matrix-${i}-${j}`;
            // Устанавливается начальное значение поля (0)
            input.value = 0;
            // Поле делается обязательным для заполнения
            input.required = true;
            // Устанавливается ширина поля ввода (60px)
            input.style.width = '60px';
            // Убираются отступы и границы поля ввода
            input.style.margin = '0';
            input.style.padding = '0';
            input.style.border = 'none';
            input.style.outline = 'none';
            // Добавляется поле ввода в ячейку
            td.appendChild(input);
            // Добавляется ячейка в строку
            tr.appendChild(td);
        }

        // Создается ячейка для ввода запасов (a_i)
        const supplyCell = document.createElement('td');
        // Создается поле ввода для запасов
        const supplyInput = document.createElement('input');
        // Устанавливается тип поля ввода как число
        supplyInput.type = 'number';
        // Задается имя поля ввода для обработки формы
        supplyInput.name = `supply-${i}`;
        // Устанавливается начальное значение поля (0)
        supplyInput.value = 0;
        // Поле делается обязательным для заполнения
        supplyInput.required = true;
        // Устанавливается ширина поля ввода (60px)
        supplyInput.style.width = '60px';
        // Убираются отступы и границы поля ввода
        supplyInput.style.margin = '0';
        supplyInput.style.padding = '0';
        supplyInput.style.border = 'none';
        supplyInput.style.outline = 'none';
        // Добавляется поле ввода в ячейку
        supplyCell.appendChild(supplyInput);
        // Добавляется ячейка в строку
        tr.appendChild(supplyCell);

        // Добавляется строка в таблицу
        table.appendChild(tr);
    }

    // Создается последняя строка для потребностей (b_j)
    const demandRow = document.createElement('tr');

    // Создается заголовок строки "Потребности"
    const demandHeader = document.createElement('th');
    // Устанавливается текст "Потребности, b_j" с нижним индексом
    demandHeader.innerHTML = 'Потребности, b<sub>j</sub>';
    // Добавляется заголовок в строку
    demandRow.appendChild(demandHeader);

    // Генерируются поля для потребностей (b_j)
    for (let j = 0; j < cols; j++) {
        // Создается ячейка для ввода потребности
        const demandCell = document.createElement('td');
        // Создается поле ввода для потребности
        const demandInput = document.createElement('input');
        // Устанавливается тип поля ввода как число
        demandInput.type = 'number';
        // Задается имя поля ввода для обработки формы
        demandInput.name = `demand-${j}`;
        // Устанавливается начальное значение поля (0)
        demandInput.value = 0;
        // Поле делается обязательным для заполнения
        demandInput.required = true;
        // Устанавливается ширина поля ввода (60px)
        demandInput.style.width = '60px';
        // Убираются отступы и границы поля ввода
        demandInput.style.margin = '0';
        demandInput.style.padding = '0';
        demandInput.style.border = 'none';
        demandInput.style.outline = 'none';
        // Добавляется поле ввода в ячейку
        demandCell.appendChild(demandInput);
        // Добавляется ячейка в строку
        demandRow.appendChild(demandCell);
    }

    // Создается пустая ячейка в последней строке под столбцом запасов
    const emptyDemandCell = document.createElement('td');
    // Добавляется пустая ячейка в строку
    demandRow.appendChild(emptyDemandCell);

    // Добавляется строка потребностей в таблицу
    table.appendChild(demandRow);

    // Добавляется таблица в контейнер
    container.appendChild(table);
}

// Функция для обновления таблицы при изменении размеров
function updateMatrix() {
    // Получаются значения количества строк и столбцов из полей ввода
    const rows = parseInt(document.getElementById('rows').value);
    const cols = parseInt(document.getElementById('cols').value);
    // Проверяется, что значения находятся в допустимом диапазоне (от 1 до 10)
    if (rows >= 1 && rows <= 10 && cols >= 1 && cols <= 10) {
        // Генерируется новая таблица с обновленными размерами
        generateMatrix(rows, cols);
    }
}

// Добавляется обработчик события на изменение значения поля количества строк
document.getElementById('rows').addEventListener('input', updateMatrix);
// Добавляется обработчик события на изменение значения поля количества столбцов
document.getElementById('cols').addEventListener('input', updateMatrix);

// Выполняется генерация таблицы при загрузке страницы
window.onload = function () {
    // Получаются элементы полей ввода
    const rowsInput = document.getElementById('rows');
    const colsInput = document.getElementById('cols');
    // Генерируется таблица с начальными значениями размеров
    generateMatrix(parseInt(rowsInput.value), parseInt(colsInput.value));
};