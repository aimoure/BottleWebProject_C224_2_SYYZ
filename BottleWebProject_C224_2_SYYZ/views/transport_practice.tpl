% rebase('layout.tpl', title=title, year=year)

<div class="hungarian-page">
    <div class="jumbotron">
        <h1>Калькулятор транспортной задачи</h1>
        <p class="lead">Введите размеры и заполните матрицу тарифов.</p>
    </div>

    <div class="container">
        <form method="post" action="/transport_practice">
            <div>
                <label for="rows">Количество поставщиков (m):</label>
                <input type="number" id="rows" name="rows" min="1" max="10" value="{{rows}}" required>
            </div>
            <div>
                <label for="cols">Количество потребителей (n):</label>
                <input type="number" id="cols" name="cols" min="1" max="10" value="{{cols}}" required>
            </div>
            <!-- Скрытые поля для передачи данных в JavaScript -->
            <input type="hidden" id="cost-matrix-data" value="{{cost_matrix_json}}">
            <input type="hidden" id="supply-data" value="{{supply_json}}">
            <input type="hidden" id="demand-data" value="{{demand_json}}">
            <br><br>
            <div id="matrix-container"></div>
            <br>
            <button type="submit" name="action" value="solve" class="btn btn-primary btn-lg">Решить задачу</button>
            <button type="submit" name="action" value="clear" class="btn btn-secondary btn-lg" style="margin-left: 15px;">Очистить</button>
        </form>

        <div class="example-panel task-container">
            <h3>Пример решения</h3>
            <p>Хочешь протестировать алгоритм? Загрузи один из наших готовых примеров!</p>
            <form method="post" action="/transport_practice_example" class="example-form">
                <button style="height: 48px" type="submit" class="btn btn-warning example-button">Загрузить пример</button>
            </form>
        </div>

        % if error:
        <div class="alert alert-danger" style="margin-top: 20px;">
            {{error}}
        </div>
        % end

        % if result:
        <div class="results" style="margin-top: 20px;">
            <h2>Результаты решения (метод потенциалов)</h2>
            <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse;">
                <tr>
                    <th></th>
                    % for j in range(cols):
                    <th>B<sub>{{j+1}}</sub></th>
                    % end
                </tr>
                % for i in range(rows):
                <tr>
                    <th>A<sub>{{i+1}}</sub></th>
                    % for j in range(cols):
                    <td>{{f"{result[i][j]:.2f}"}}</td>
                    % end
                </tr>
                % end
            </table>
            <p><strong>Общая стоимость:</strong> {{f"{total_cost:.2f}"}}</p>
        </div>
        % end
    </div>
</div>
<script src="/static/scripts/dynamic_table_transport.js"></script>