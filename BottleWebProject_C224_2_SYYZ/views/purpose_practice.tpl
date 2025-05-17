% rebase('layout.tpl', title="Калькулятор задачи о назначений", year=year)

<div class="hungarian-page">
    <!-- Заголовок страницы -->
    <div class="jumbotron">
        <h1>Калькулятор задачи о назначениях</h1>
        <p class="lead">Введите размер матрицы и значения затрат.</p>
    </div>

    <div class="container">
        <!-- Основная форма: ввод размера и значений матрицы -->
        <form method="post" action="/hungarian-calc">
            <label for="size">Размер матрицы (n × n):&emsp;</label>
            <input class="always-visible" type="number" id="size" name="size" min="2" max="10" value="4" required>
            
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
            <form method="post" action="/hungarian-calc-example" class="example-form">
                <button style="height: 48px" type="submit" class="btn btn-warning example-button">Загрузить пример</button>
            </form>
        </div>
    </div>
</div>

<script src="/static/scripts/dynamic_table_purpose.js"></script>