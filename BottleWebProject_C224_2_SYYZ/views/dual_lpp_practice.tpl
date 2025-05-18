% rebase('layout.tpl', title=title, year=year)
% result_table = result_table if 'result_table' in locals() else None
% dual_steps = dual_steps if 'dual_steps' in locals() else None
% answer_vars = answer_vars if 'answer_vars' in locals() and answer_vars is not None else {}

<script src="/static/scripts/dynamic_table_dual.js"></script>

<div class="hungarian-page">
    <div class="jumbotron">
        <h1>Калькулятор двойственной задачи линейного программирования</h1>
        <p class="lead">Введи размер матрицы и значения затрат</p>
    </div>

    <div class="container">
        <form method="post" action="/dual_lpp_practice">
            <label>Количество переменных:&emsp;</label>
            <input class="always-visible" type="number" id="number_of_variables" name="num_vars" min="2" max="10" value="2" required>
            <br>
            <label>Коэфициенты:&emsp;</label>
            <div id="variables_container"></div>
            <br>
            <label>Количество ограничений:&emsp;</label>
            <input class="always-visible" type="number" id="number_of_constraints" name="num_cons" min="1" max="10" value="1" required>
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

            <!-- Добавляем условие неотрицательности -->
            <div id="nonnegativity_condition" style="margin-top: 20px; font-size: 18px; font-weight: bold;"></div>

            <br>
            <button type="submit" class="btn btn-primary btn-lg">Решить задачу</button>
            <button type="submit" id="reset_button" class="btn btn-secondary btn-lg" style="margin-left: 15px;">Очистить</button>
        </form>

        % if answer_vars:
            <h3>Ответ:</h3>
            <p>
                % for var, val in answer_vars.items():
                    {{var}} = {{round(val, 2)}}&emsp;
                % end
            </p>
            <p>Значение целевой функции: W = {{F}}</p>
        % endif

        % if dual_steps:
            <div class="section">
                <h3>Решение двойственной задачи:</h3>
                % for step in dual_steps:
                    <h4>{{step['title']}}</h4>
                    <p>{{step['explanation']}}</p>
                    <table class="custom-table">
                        <tr>
                            <th>Базис</th>
                            % for i in range(len(step['table'][0])-2):
                                <th>y{{i+1}}</th>
                            % end
                            <th>Свободный член</th>
                        </tr>
                        % for row in step['table']:
                            <tr>
                                % for cell in row:
                                    <td>{{round(cell, 2) if isinstance(cell, float) else cell}}</td>
                                % end
                            </tr>
                        % end
                    </table>
                % end
            </div>
        % end

        % if answer_vars:
            <h3>Результат:</h3>
            <p>
                % for var, val in answer_vars.items():
                    {{var}} = {{round(val, 2)}}&emsp;
                % end
            </p>
            <p>Значение целевой функции: W = {{F}}</p>
            <h4>Проверим двойственность:</h4>
            <p><b>{{duality_check}}</b></p>
        % end

        
        <!-- Возможность загрузить готовый пример -->
        <div class="example-panel task-container">
            <h3>Пример решения</h3>
            <p>Не хочешь заморачиваться? Загрузить готовый пример и проверить алгоритм!</p>
            <form method="post" action="/hungarian-calc" enctype="multipart/form-data" class="example-form">
                <button style="height: 48px" type="submit" class="btn btn-warning example-button">Загрузить пример</button>
            </form>
        </div>
    </div>
</div>


