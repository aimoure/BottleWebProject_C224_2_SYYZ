% rebase('layout.tpl', title="Калькулятор транспортной задачи", year=year)

<div class="hungarian-page">
    <!-- Заголовок страницы -->
    <div class="jumbotron">
        <h1>Калькулятор транспортной задачи</h1>
        <p class="lead">Введите размеры матрицы и значения затрат.</p>
    </div>

    <div class="container">
        <!-- Основная форма: ввод размеров и значений матрицы -->
        <form method="post" action="/transport-calc">
            <label for="rows">Количество поставщиков (m):</label>
            <input type="number" id="rows" name="rows" min="1" max="10" value="3" required>
            
            <label for="cols">Количество потребителей (n):</label>
            <input type="number" id="cols" name="cols" min="1" max="10" value="4" required>
            
            <br><br>

            <!-- Контейнер с таблицей матрицы -->
            <div id="matrix-container"></div>

            <br>

            <button type="submit" class="btn btn-primary btn-lg">Решить задачу</button>
        </form>

        <!-- Боковая панель справа от матрицы -->
        <div class="example-panel task-container">
            <h3>Пример решения</h3>
            <p>Хочешь протестировать алгоритм? Загрузи один из наших готовых примеров!</p>

            <!-- Форма с кнопкой загрузки примера -->
            <form method="post" action="/transport-calc-example" class="example-form">
                <button type="submit" class="btn btn-warning example-button">Загрузить пример</button>
            </form>
        </div>
    </div>
</div>

<!-- Скрипт генерации таблицы -->
<script>
    function generateMatrix(rows, cols) {
        const container = document.getElementById('matrix-container');
        container.innerHTML = ''; // Очищаем старую таблицу

        const table = document.createElement('table');
        table.border = "1";
        table.cellPadding = "5";
        table.cellSpacing = "0";

        // Заголовок таблицы
        const headerRow = document.createElement('tr');
        
        // Пустая ячейка в левом верхнем углу
        const emptyCell = document.createElement('th');
        headerRow.appendChild(emptyCell);

        // Заголовки столбцов (Матрица тарифов, Bij)
        for (let j = 0; j < cols; j++) {
            const th = document.createElement('th');
            th.textContent = `B${j+1}`;
            headerRow.appendChild(th);
        }

        // Заголовок для столбца "Запасы"
        const supplyHeader = document.createElement('th');
        supplyHeader.textContent = 'Запасы, a_i';
        supplyHeader.style.backgroundColor = '#ffe6cc';
        headerRow.appendChild(supplyHeader);

        table.appendChild(headerRow);

        // Строки таблицы
        for (let i = 0; i < rows; i++) {
            const tr = document.createElement('tr');

            // Заголовок строки (Поставщик)
            const rowHeader = document.createElement('th');
            rowHeader.textContent = `A${i+1}`;
            rowHeader.style.backgroundColor = '#ffe6cc';
            tr.appendChild(rowHeader);

            // Ячейки матрицы затрат
            for (let j = 0; j < cols; j++) {
                const td = document.createElement('td');
                const input = document.createElement('input');
                input.type = 'number';
                input.name = `matrix-${i}-${j}`;
                input.value = 0;
                input.required = true;
                input.style.width = '60px';
                td.appendChild(input);
                tr.appendChild(td);
            }

            // Поле для запасов (a_i)
            const supplyCell = document.createElement('td');
            const supplyInput = document.createElement('input');
            supplyInput.type = 'number';
            supplyInput.name = `supply-${i}`;
            supplyInput.value = 0;
            supplyInput.required = true;
            supplyInput.style.width = '60px';
            supplyCell.style.backgroundColor = '#ffe6cc';
            supplyCell.appendChild(supplyInput);
            tr.appendChild(supplyCell);

            table.appendChild(tr);
        }

        // Последняя строка для потребностей (b_j)
        const demandRow = document.createElement('tr');

        // Заголовок "Потребности"
        const demandHeader = document.createElement('th');
        demandHeader.textContent = 'Потребности, b_j';
        demandHeader.style.backgroundColor = '#ffe6cc';
        demandRow.appendChild(demandHeader);

        // Поля для потребностей (b_j)
        for (let j = 0; j < cols; j++) {
            const demandCell = document.createElement('td');
            const demandInput = document.createElement('input');
            demandInput.type = 'number';
            demandInput.name = `demand-${j}`;
            demandInput.value = 0;
            demandInput.required = true;
            demandInput.style.width = '60px';
            demandCell.style.backgroundColor = '#ffe6cc';
            demandCell.appendChild(demandInput);
            demandRow.appendChild(demandCell);
        }

        // Пустая ячейка в последней строке под столбцом запасов
        const emptyDemandCell = document.createElement('td');
        emptyDemandCell.style.backgroundColor = '#ffe6cc';
        demandRow.appendChild(emptyDemandCell);

        table.appendChild(demandRow);

        container.appendChild(table);
    }

    // Генерация матрицы при изменении значений размеров
    function updateMatrix() {
        const rows = parseInt(document.getElementById('rows').value);
        const cols = parseInt(document.getElementById('cols').value);
        if (rows >= 1 && rows <= 10 && cols >= 1 && cols <= 10) {
            generateMatrix(rows, cols);
        }
    }

    document.getElementById('rows').addEventListener('input', updateMatrix);
    document.getElementById('cols').addEventListener('input', updateMatrix);

    // Генерация матрицы при загрузке страницы
    window.onload = function () {
        const rowsInput = document.getElementById('rows');
        const colsInput = document.getElementById('cols');
        generateMatrix(parseInt(rowsInput.value), parseInt(colsInput.value));
    };
</script>