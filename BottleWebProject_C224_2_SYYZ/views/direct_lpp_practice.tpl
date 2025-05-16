% rebase('layout.tpl', title=title, year=year)

<div class="hungarian-page">
    <div class="jumbotron">
        <h1>Калькулятор прямой задачи линейного программирования</h1>
        <p class="lead">Введи размер матрицы и значения затрат</p>
    </div>

    <div class="container">
        <form method="post" action="/hungarian-calc">
            <label for="size">Количество переменных:&emsp;</label>
            <input style="text-align: center; border-radius: 10px;" type="number" id="number_of_variable" name="size" min="2" max="10" value="2" required>
            <br>
            <div id="variable_container"></div>
            <br>
            <button type="submit" class="btn btn-primary btn-lg">Решить задачу</button>
        </form>

        <div class="example-panel task-container">
            <h3>Пример решения</h3>
            <p>Не хочешь заморачиваться? Загрузить готовый пример и проверить алгоритм!</p>
            <form method="post" action="/hungarian-calc" enctype="multipart/form-data" class="example-form">
                <button type="submit" class="btn btn-warning example-button">Загрузить пример</button>
            </form>
        </div>
        <div class="example-panel task-container">
            <h3>Двойственная задача</h3>
            <p>Нужно найти двойственную задачу? Можешь перейти здесь.</p>
            <p>
                <a href="/dual_lpp_practice" class="btn btn-warning btn-lg mt-3">Двойственная ЗЛП</a>
            </p>
        </div>
    </div>
</div>