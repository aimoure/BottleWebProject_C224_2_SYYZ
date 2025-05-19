% rebase('layout.tpl', title=title, year=year)

<div class="hungarian-page">
    <div class="jumbotron">
        <h1>Калькулятор прямой задачи линейного программирования</h1>
        <p class="lead">Введи размер матрицы и значения затрат</p>
    </div>

    <!-- Основной контейнер -->
    <div class="container">
        <form method="post" action="/hungarian-calc">
            <label>Количество переменных:&emsp;</label>
            <input class="always-visible" type="number" id="number_of_variables" min="2" max="10" value="2" required>
            <br>
            <label>Коэфициенты:&emsp;</label>
            <div id="variables_container"></div>
            <br>
            <label>Количество ограничений:&emsp;</label>
            <input class="always-visible" type="number" id="number_of_constraints" min="1" max="10" value="1" required>
            <br>
            <label>Ограничения:&emsp;</label>
            <div id="constraints_wrapper" style="display:flex; gap:20px; align-items:flex-start;">
                <!-- Коэффициенты -->
                <div>
                    <div id="constraints_vars"></div>
                </div>
                <!-- Знак -->
                <div>
                    <div id="constraints_signs"></div>
                </div>
                <!-- Свободный член -->
                <div>
                    <div id="constraints_rhs"></div>
                </div>
            </div>
            <br>
            <button type="submit" class="btn btn-primary btn-lg">Решить задачу</button>
        </form>

        <!-- Возможность загрузить готовый пример -->
        <div class="example-panel task-container">
            <h3>Пример решения</h3>
            <p>Не хочешь заморачиваться? Загрузить готовый пример и проверить алгоритм!</p>
            <form method="post" action="/hungarian-calc" enctype="multipart/form-data" class="example-form">
                <button style="height: 48px" type="submit" class="btn btn-warning example-button">Загрузить пример</button>
            </form>
        </div>
        <!-- Переход к калькулятору двойственной задачи -->
        <div class="example-panel task-container">
            <h3>Двойственная задача</h3>
            <p>Нужно найти и решить двойственную задачу? Можешь перейти здесь.</p>
            <p>
                <a href="/dual_lpp_practice" class="btn btn-warning btn-lg mt-3">Двойственная ЗЛП</a>
            </p>
        </div>
    </div>
</div>


<script src="/static/scripts/dynamic_table.js"></script>