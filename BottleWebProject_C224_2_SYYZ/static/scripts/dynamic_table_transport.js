// Создается таблица матрицы с заданным количеством строк и столбцов, поддерживается ввод данных для затрат, запасов и потребностей
function generateMatrix(rows, cols, matrixData = null, supplyData = null, demandData = null) {
    const container = document.getElementById('matrix-container');
    container.innerHTML = ''; // Очищается содержимое контейнера перед созданием новой таблицы

    const table = document.createElement('table');
    table.border = "1";
    table.cellPadding = "5";
    table.cellSpacing = "0";
    table.style.borderCollapse = "collapse"; // Устанавливаются стили для таблицы

    // Создается заголовочная строка с метками для столбцов и ячейкой для заголовка запасов
    const headerRow = document.createElement('tr');
    const emptyCell = document.createElement('th');
    headerRow.appendChild(emptyCell);

    for (let j = 0; j < cols; j++) {
        const th = document.createElement('th');
        th.innerHTML = `B<sub>${j + 1}</sub>`; // Метки для столбцов B1, B2, ...
        headerRow.appendChild(th);
    }

    const supplyHeader = document.createElement('th');
    supplyHeader.innerHTML = 'Запасы, a<sub>i</sub>'; // Заголовок для столбца запасов
    headerRow.appendChild(supplyHeader);
    table.appendChild(headerRow);

    // Создаются строки таблицы с ячейками для ввода затрат и запасов
    for (let i = 0; i < rows; i++) {
        const tr = document.createElement('tr');
        const rowHeader = document.createElement('th');
        rowHeader.innerHTML = `A<sub>${i + 1}</sub>`; // Метки для строк A1, A2, ...
        tr.appendChild(rowHeader);

        for (let j = 0; j < cols; j++) {
            const td = document.createElement('td');
            const input = document.createElement('input');
            input.type = 'number';
            input.name = `matrix-${i}-${j}`; // Уникальное имя для ячейки матрицы
            input.value = matrixData && matrixData[i] && matrixData[i][j] !== undefined ? matrixData[i][j] : 0; // Устанавливается значение из matrixData или 0
            input.min = 0;
            input.required = true;
            input.style.width = '60px';
            input.style.margin = '0';
            input.style.padding = '0';
            input.style.border = 'none';
            input.style.outline = 'none'; // Стили для поля ввода
            td.appendChild(input);
            tr.appendChild(td);
        }

        const supplyCell = document.createElement('td');
        const supplyInput = document.createElement('input');
        supplyInput.type = 'number';
        supplyInput.name = `supply-${i}`; // Уникальное имя для ячейки запаса
        supplyInput.value = supplyData && supplyData[i] !== undefined ? supplyData[i] : 0; // Устанавливается значение из supplyData или 0
        supplyInput.min = 0;
        supplyInput.required = true;
        supplyInput.style.width = '60px';
        supplyInput.style.margin = '0';
        supplyInput.style.padding = '0';
        supplyInput.style.border = 'none';
        supplyInput.style.outline = 'none'; // Стили для поля ввода
        supplyCell.appendChild(supplyInput);
        tr.appendChild(supplyCell);
        table.appendChild(tr);
    }

    // Создается строка для ввода потребностей
    const demandRow = document.createElement('tr');
    const demandHeader = document.createElement('th');
    demandHeader.innerHTML = 'Потребности, b<sub>j</sub>'; // Заголовок для строки потребностей
    demandRow.appendChild(demandHeader);

    for (let j = 0; j < cols; j++) {
        const demandCell = document.createElement('td');
        const demandInput = document.createElement('input');
        demandInput.type = 'number';
        demandInput.name = `demand-${j}`; // Уникальное имя для ячейки потребности
        demandInput.value = demandData && demandData[j] !== undefined ? demandData[j] : 0; // Устанавливается значение из demandData или 0
        demandInput.min = 0;
        demandInput.required = true;
        demandInput.style.width = '60px';
        demandInput.style.margin = '0';
        demandInput.style.padding = '0';
        demandInput.style.border = 'none';
        demandInput.style.outline = 'none'; // Стили для поля ввода
        demandCell.appendChild(demandInput);
        demandRow.appendChild(demandCell);
    }

    const emptyDemandCell = document.createElement('td');
    demandRow.appendChild(emptyDemandCell);
    table.appendChild(demandRow);
    container.appendChild(table); // Добавляется таблица в контейнер
}

// Обновляется матрица при изменении количества строк или столбцов
function updateMatrix() {
    const rows = parseInt(document.getElementById('rows').value);
    const cols = parseInt(document.getElementById('cols').value);
    if (rows >= 1 && rows <= 10 && cols >= 1 && cols <= 10) { // Проверяется допустимость размеров матрицы
        // Сохраняются текущие данные формы
        const form = document.querySelector('form');
        const formData = new FormData(form);
        const matrixData = [];
        const supplyData = [];
        const demandData = [];

        for (let i = 0; i < rows; i++) {
            matrixData[i] = [];
            for (let j = 0; j < cols; j++) {
                matrixData[i][j] = parseFloat(formData.get(`matrix-${i}-${j}`)) || 0; // Собираются данные матрицы
            }
            supplyData[i] = parseFloat(formData.get(`supply-${i}`)) || 0; // Собираются данные запасов
        }
        for (let j = 0; j < cols; j++) {
            demandData[j] = parseFloat(formData.get(`demand-${j}`)) || 0; // Собираются данные потребностей
        }

        generateMatrix(rows, cols, matrixData, supplyData, demandData); // Перегенерируется матрица с сохраненными данными
    }
}

// Добавляются обработчики событий для полей ввода количества строк и столбцов
document.getElementById('rows').addEventListener('input', updateMatrix);
document.getElementById('cols').addEventListener('input', updateMatrix);

// Инициализируется матрица при загрузке страницы
window.onload = function () {
    const rowsInput = document.getElementById('rows');
    const colsInput = document.getElementById('cols');
    // Получаются данные из шаблона
    const costMatrixJson = document.getElementById('cost-matrix-data').value;
    const supplyJson = document.getElementById('supply-data').value;
    const demandJson = document.getElementById('demand-data').value;

    const matrixData = costMatrixJson !== 'null' ? JSON.parse(costMatrixJson) : null; // Парсятся данные матрицы затрат
    const supplyData = supplyJson !== 'null' ? JSON.parse(supplyJson) : null; // Парсятся данные запасов
    const demandData = demandJson !== 'null' ? JSON.parse(demandJson) : null; // Парсятся данные потребностей

    generateMatrix(
        parseInt(rowsInput.value),
        parseInt(colsInput.value),
        matrixData,
        supplyData,
        demandData
    ); // Генерируется начальная матрица
};