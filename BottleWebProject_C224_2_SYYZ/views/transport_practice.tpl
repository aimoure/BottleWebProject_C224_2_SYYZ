% rebase('layout.tpl', title=title, year=year)

<div class="hungarian-page">
    <!-- Заголовок страницы -->
    <div class="jumbotron">
        <h1>Калькулятор транспортной задачи</h1>
        <p class="lead">Введите размеры и заполните матрицу тарифов.</p>
    </div>

    <div class="container">
        <!-- Основная форма: ввод размеров и значений матрицы -->
        <form method="post" action="/transport-calc">
            <div>
                <label for="rows">Количество поставщиков (m):</label>
                <input type="number" id="rows" name="rows" min="1" max="10" value="3" required>
            </div>
            
            <div>
                <label for="cols">Количество потребителей (n):</label>
                <input type="number" id="cols" name="cols" min="1" max="10" value="4" required>
            </div>
            
            <br><br>

            <!-- Контейнер с таблицей матрицы -->
            <div id="matrix-container"></div>

            <br>

            <button type="submit" class="btn btn-primary btn-lg">Решить задачу</button>
            <button type="submit" class="btn btn-secondary btn-lg" style="margin-left: 15px;">Очистить</button>
        </form>

        <!-- Боковая панель справа от матрицы -->
        <div class="example-panel task-container">
            <h3>Пример решения</h3>
            <p>Хочешь протестировать алгоритм? Загрузи один из наших готовых примеров!</p>

            <!-- Форма с кнопкой загрузки примера -->
            <form method="post" action="/transport-calc-example" class="example-form">
                <button style="height: 48px" type="submit" class="btn btn-warning example-button">Загрузить пример</button>
            </form>
        </div>
    </div>
</div>

<script src="/static/scripts/dynamic_table_transport.js"></script>