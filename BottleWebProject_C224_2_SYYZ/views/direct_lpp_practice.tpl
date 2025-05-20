% rebase('layout.tpl', title=title, year=year)
% error = error if 'error' in locals() else None
% x_values = x_values if 'x_values' in locals() else None
% objective_value = objective_value if 'objective_value' in locals() else None
% status = status if 'status' in locals() else None
% initial_data_json = initial_data_json if 'initial_data_json' in locals() else None

<div class="hungarian-page">
    <div class="jumbotron">
        <h1>Калькулятор прямой задачи линейного программирования</h1>
        <p class="lead">Введи размер матрицы и значения затрат</p>
    </div>

    <!-- Основной контейнер -->
    <div class="container">
        <form method="post" action="/hungarian-calc">
            <label>Количество переменных:&emsp;</label>
            <input class="always-visible" type="number" id="number_of_variables" name="number_of_variables" min="2" max="10" value="2" required onkeydown="return false;">
            <br>
            <label>Коэфициенты целевой функции:&emsp;</label>
            <div id="variables_container"></div>
            <br>
            <label>Количество ограничений:&emsp;</label>
            <input class="always-visible" type="number" id="number_of_constraints" name="number_of_constraints" min="1" max="10" value="1" required onkeydown="return false;">
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
            <!-- Добавление условия неотрицательности -->
            <div id="nonnegativity_condition" style="margin-top: 20px; font-size: 18px; font-weight: bold;"></div>
            <br>
            <button type="submit" class="btn btn-primary btn-lg" name="action" value="solve">Решить задачу</button>
            <button type="submit" class="btn btn-secondary btn-lg" style="margin-left: 15px;" id="reset_button">Очистить</button>
            <br>
            <div id="results" style="margin-top:20px;">
              % if error:
                <div class="alert alert-danger">{{error}}</div>
              % elif x_values:
                <h3>Результат решения</h3>
                <p>Оптимальные x: {{', '.join(map(str,x_values))}}</p>
                <p style="margin-bottom: -10px">Значение цели: {{objective_value}}</p>
              % end
            </div>
        </form>

        <!-- Возможность загрузить готовый пример -->
        <div class="example-panel task-container">
            <h3>Пример решения</h3>
            <p>Не хочешь заморачиваться? Загрузить готовый пример и проверить алгоритм!</p>
            <form method="post" action="/hungarian-calc" enctype="multipart/form-data" class="example-form">
                <button style="height: 48px" type="submit" class="btn btn-warning example-button" name="action" value="load_example">Загрузить пример</button>
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

% if initial_data_json:
    
    <script>
    document.addEventListener('DOMContentLoaded', () => {
        const data = JSON.parse('{{!initial_data_json}}');
        localStorage.setItem('directLppData', JSON.stringify(data));
        window.loadFromStorage();
    });
    </script>
% end