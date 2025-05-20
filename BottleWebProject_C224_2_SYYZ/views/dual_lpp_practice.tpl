% rebase('layout.tpl', title=title, year=year)

<!-- Определение переменных с безопасной инициализацией -->
% result_table = result_table if 'result_table' in locals() else None
% dual_steps = dual_steps if 'dual_steps' in locals() else None
% num_vars = num_vars if 'num_vars' in locals() else None
% num_cons = num_cons if 'num_cons' in locals() else None
% primal_obj = primal_obj if 'primal_obj' in locals() else None
% dual_obj = dual_obj if 'dual_obj' in locals() else None
% no_solution = no_solution if 'no_solution' in locals() else None
% form_data = form_data if 'form_data' in locals() else None
% answer_vars = answer_vars if 'answer_vars' in locals() and answer_vars is not None else {}

<!--  Подключение JavaScript для динамического управления таблицей -->
<script src="/static/scripts/dynamic_table_dual.js"></script>

<script>
// Если сервер передал нам form_data — зальём его в localStorage ДО того, 
// как dynamic_table_dual.js сделает loadFromStorage()
% if form_data and form_data['x']:
(function(){
    const data = {
        numVars: {{num_vars}},
        numCons: {{num_cons}},
        vars:      {},   // для x_i
        consVars:  {},   // для cons_i_j
        consSigns: {},   // для cons_sign_i
        consRhs:   {}    // для cons_rhs_i
    };

    // 1) Целевая функция
    % for i, val in enumerate(form_data['x']):
    data.vars[`x_{{i}}`] = "{{val}}";
    % end

    // 2) Левые коэффициенты ограничений
    % for i, row in enumerate(form_data['cons']):
        % for j, val in enumerate(row):
    data.consVars[`cons_{{i}}_{{j}}`] = "{{val}}";
        % end
    % end

    // 3) Знаки
    % for i, val in enumerate(form_data['signs']):
    data.consSigns[`cons_sign_{{i}}`] = "{{val}}";
    % end

    // 4) Правые части
    % for i, val in enumerate(form_data['rhs']):
    data.consRhs[`cons_rhs_{{i}}`] = "{{val}}";
    % end

    localStorage.setItem('dualLppData', JSON.stringify(data));
})();
% end
</script>


<div class="hungarian-page">
    <div class="jumbotron">
        <h1>Калькулятор двойственной задачи линейного программирования</h1>
        <p class="lead">Введите коэффициенты задачи и получите решение двойственной задачи</p>
    </div>

    <div class="container">
        <!-- Форма для ввода данных задачи -->
        <form method="post" action="/dual_lpp_practice">
            <label>Количество переменных:</label>
            <input type="number" id="number_of_variables" name="num_vars" min="2" max="10" step="1" value="{{num_vars or 2}}" required onkeydown="return false;">
            <br>

            <label>Коэффициенты целевой функции:</label>
            <div id="variables_container">
                % if num_vars:
                    % for i in range(num_vars):
                        <input type="number" step="any" name="x_{{i}}" size="5"
                               value="{{form_data['x'][i] if i < len(form_data['x']) else ''}}">
                    % end
                % end
            </div>
            <br>

            <label>Количество ограничений:</label>
            <input type="number" id="number_of_constraints" name="num_cons" min="1" max="10" value="{{num_cons or 1}}" required onkeydown="return false;">
            <br>

            <label>Ограничения:&emsp;</label>
            <!-- Контейнеры для ограничений: коэффициенты, знаки, свободные члены -->
            <div id="constraints_wrapper" style="display:flex; gap:20px; align-items:flex-start;">
                <div>
                    <div id="constraints_vars">
                    % if num_vars:
                        % for i in range(num_cons):
                            <div>
                                % for j in range(num_vars):
                                    <input type="number" step="any" name="cons_{{i}}_{{j}}" size="5"
                                           value="{{form_data['cons'][i][j] if i < len(form_data['cons']) and j < len(form_data['cons'][i]) else ''}}">
                                % end
                            </div>
                        % end
                    % end
                    </div>
                </div>
                <div>
                    <div id="constraints_signs">
                    % if num_cons:
                        % for i in range(num_cons):
                            <select name="cons_sign_{{i}}">
                                <option value="≤" {{'selected' if (form_data['signs'][i] if i < len(form_data['signs']) else '') == '≤' else ''}}>≤</option>
                                <option value="≥" {{'selected' if (form_data['signs'][i] if i < len(form_data['signs']) else '') == '≥' else ''}}>≥</option>
                                <option value="=" {{'selected' if (form_data['signs'][i] if i < len(form_data['signs']) else '') == '=' else ''}}>=</option>
                            </select>
                        % end
                    % end
                    </div>
                </div>
                <div>
                    <div id="constraints_rhs">
                    % if num_cons:
                        % for i in range(num_cons):
                            <input type="number" step="any" name="cons_rhs_{{i}}" size="5"
                                   value="{{form_data['rhs'][i] if i < len(form_data['rhs']) else ''}}">
                        % end
                    % end
                    </div>
                </div>
            </div>

            <!-- Автоматическое добавление условий неотрицательности -->
            <div id="nonnegativity_condition" style="margin-top: 20px; font-size: 18px; font-weight: bold;"></div>
            <br>

            <!-- Кнопки отправки и очистки формы -->
            <button type="submit" class="btn btn-primary btn-lg">Решить задачу</button>
            <button type="button" id="reset_button" class="btn btn-secondary btn-lg" style="margin-left: 15px;">Очистить</button>
        </form>

        <!-- Отображение результатов решения задачи -->
        <div id="results">
            <br>

            % if no_solution:
                <!-- Сообщение об ошибке при отсутствии решения -->
                <div class="alert alert-danger" role="alert">
                    {{error_message}}
                </div>
            % else:
                % if primal_obj and dual_obj:
                    <!-- Вывод исходной и двойственной задач -->
                    <div class="section">
                        <h3>Исходная задача:</h3>
                        <p><b>Целевая функция:</b> {{primal_obj}}</p>
                        <p><b>Ограничения:</b></p>
                        <ul>
                            % for cons in primal_constraints:
                                <li>{{cons}}</li>
                            % end
                            <li>x1, x2 ≥ 0</li>
                        </ul>

                        <h3>Двойственная задача:</h3>
                        <p><b>Целевая функция:</b> {{dual_obj}}</p>
                        <p><b>Ограничения:</b></p>
                        <ul>
                            % for cons in dual_constraints:
                                <li>{{cons}}</li>
                            % end
                            <li>y1, y2 ≥ 0</li>
                        </ul>
                    </div>
                % end

                % if answer_vars:
                    <!-- Отображение найденного оптимального решения -->
                    <h3>Ответ:</h3>
                    <p>
                        % for var, val in answer_vars.items():
                            {{var}} = {{round(val, 2)}}&emsp;
                        % end
                        W = {{round(F, 2)}}
                    </p>
                % end

                % if dual_steps:
                    <!-- Пошаговое решение двойственной задачи -->
                    <div class="section">
                        <h3>Решение двойственной задачи:</h3>
                        % for step in dual_steps:
                            <h4>{{step['title']}}</h4>
                            <p>{{step['explanation']}}</p>
                            <table class="custom-table">
                                <tr>
                                    <th>Базис</th>
                                    % for i in range(len(step['table'][0]) - 2):
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
                    <!-- Проверка равенства значений целевых функций -->
                    <h4>Проверка двойственности:</h4>
                    <p><b>{{duality_check}} Z = W = {{round(F, 2)}}</b></p>
                % end
            % end
        </div>

        <!-- Панель загрузки готового примера -->
        <div class="example-panel task-container">
            <h3>Пример решения</h3>
            <p>Не хочешь заморачиваться? Загрузить готовый пример и проверить алгоритм!</p>
            <form method="post" action="/dual_lpp_example" class="example-form">
              <button type="submit" class="btn btn-warning example-button">
                Загрузить пример
              </button>
            </form>
        </div>
    </div>
</div>
