% rebase('layout.tpl', title="Калькулятор задачи о назначений", year=year)

<div class="hungarian-page">
    <div class="jumbotron">
        <h1>Калькулятор задачи о назначений</h1>
        <p class="lead">Введи размер матрицы и значения затрат</p>
    </div>

    <div class="container">
        <form method="post" action="/hungarian-calc">
            <label for="size">Размер матрицы (n × n):</label>
            <input type="number" id="size" name="size" min="2" max="10" value="4" required>
            <br><br>
            <div id="matrix-container"></div>
            <br>
            <button type="submit" class="btn btn-primary btn-lg">Решить задачу</button>
        </form>

        <div class="example-panel task-container">
            <h3>Пример решения</h3>
            <p>Не хочешь заморачиваться? Загрузить готовый пример и проверить алгоритм!</p>
            <form method="post" action="/hungarian-calc" enctype="multipart/form-data" class="example-form">
                <input type="file" name="example-file" accept=".txt,.json,.csv" class="form-control example-file-input" />
                <button type="submit" class="btn btn-warning example-button">Загрузить пример</button>
            </form>
        </div>
    </div>
</div>

<script>
    function generateMatrix(n) {
        const container = document.getElementById('matrix-container');
        container.innerHTML = ''; // Очистить старую таблицу

        const table = document.createElement('table');
        table.border = "1";
        table.cellPadding = "5";
        table.cellSpacing = "0";

        for(let i = 0; i < n; i++) {
            const tr = document.createElement('tr');
            for(let j = 0; j < n; j++) {
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
            table.appendChild(tr);
        }

        container.appendChild(table);
    }

    document.getElementById('size').addEventListener('input', function() {
        let size = parseInt(this.value);
        if(size >= 2 && size <= 10) {
            generateMatrix(size);
        }
    });

    window.onload = function() {
        const sizeInput = document.getElementById('size');
        generateMatrix(parseInt(sizeInput.value));
    }
</script>