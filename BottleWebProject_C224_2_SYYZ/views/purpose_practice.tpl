% rebase('layout.tpl', title="Калькулятор задачи о назначениях", year=year)

<div class="hungarian-page">
    <!-- Заголовок страницы -->
    <div class="jumbotron bg-warning text-dark">
        <h1>Калькулятор задачи о назначениях</h1>
        <p class="lead">Введите размер матрицы и значения затрат.</p>
    </div>

    <div class="container">
        <!-- Основная форма: ввод размера и значений матрицы -->
        <form method="post" action="/purpose_practice">
            <label for="size">Размер матрицы (n × n):&emsp;</label>
            <input class="always-visible" type="number" id="size" name="size" min="2" max="10" value="4" required>
            
            <br><br>
            <div class="form-check form-switch mb-3">
                <input class="form-check-input" type="checkbox" id="maximize" name="maximize">
                <label class="form-check-label" for="maximize">Решать задачу на максимум</label>
            </div>
            <!-- Контейнер с таблицей матрицы -->
            <div id="matrix-container"></div>

            <br>

            <button type="submit" class="btn btn-primary btn-lg">Решить задачу</button>
        </form>

        <div class="example-panel task-container p-3 mb-4 border rounded bg-light">
            <h3>Пример решения</h3>
            <p>Хочешь протестировать алгоритм? Сгенерируй рандомные значения!</p>

            <button type="button" id="uploadRandomBtn" class="btn btn-warning btn-lg">Сгенерировать</button>
        </div>

        % if result:
        <hr>
        <div class="result-container p-4 mb-5 border rounded shadow-sm bg-white">
            <h2 class="text-center mb-4" style="color: #f56c42;">Результат задачи о назначениях</h2>
            <p class="fs-5"><strong>Итоговая стоимость:</strong> <span class="badge bg-danger fs-6">{{result['total_cost']}}</span></p>
            <table class="table table-striped table-bordered mt-3">
                <thead class="table-warning">
                    <tr>
                        <th>Рабочий</th>
                        <th>Назначенная задача</th>
                    </tr>
                </thead>
                <tbody>
                % for worker, task in enumerate(result['assignment']):
                    <tr>
                        <td>{{worker_labels[worker]}}</td>
                        <td>{{task_labels[task]}}</td>
                    </tr>
                % end
                </tbody>
            </table>
        </div>
        % end

        % if error:
        <div class="alert alert-danger" role="alert">
            <strong>Ошибка:</strong> {{error}}
        </div>
        % end
    </div>
</div>

<script src="/static/scripts/dynamic_table_purpose.js"></script>
