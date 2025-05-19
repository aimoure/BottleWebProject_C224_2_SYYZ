% rebase('layout.tpl', title=title, year=year)

<!-- Подключение MathJax -->
<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>\

<div class="hungarian-page">
    <div class="jumbotron">
        <h1>Прямая задача линейного программирования</h1>
        <p class="lead">
            Суть прямой задачи линейного программирования состоит в том, чтобы максимизировать или минимизировать линейную функцию в условиях, выраженных системой линейных ограничений.
        </p>
        <p>
            <a href="/direct_lpp_practice" class="btn btn-warning btn-lg mt-3">Перейти к калькулятору</a>
        </p>
    </div>

    <!-- Основной контейнер -->
    <div class="container">
        <div class="section">
            <h2>Определение задачи</h2>
            <p class="text">
                Прямая задача линейного программирования (ЗЛП) — задача оптимизации, где нужно максимизировать или минимизировать 
                линейную целевую функцию \(Z = c_1 x_1 + c_2 x_2 + \ldots + c_n x_n\) при условии, что переменные \( x_i \) удовлетворяют системе линейных ограничений:
                \(a_1 x_3 + a_2 x_5 \leq b_1\) и условию неотрицательности \( x_i \geq 0 \).
            </p>
            <p class="text">Цель — найти такие \( x_i \), чтобы \( Z \) была оптимальной.</p>
            <p class="text">Основным методом для решения прямой ЗЛП является симплекс-метод.</p>
        </div>

        <!-- Симплек метод -->
        <section class="section">
            <h2>Симплекс-метод</h2>
            <p class="text">
                Симплекс-метод — это алгоритм решения ЗЛП, который работает следующим образом:
            </p>
            <ol class="list">
                <li class="text">Приведение задачи к стандартной форме, добавляя дополнительные переменные для неравенств.</li>
                <li class="text">Построение начальной симплекс-таблицы, где строки — ограничения, а последняя строка — целевая функция.</li>
                <li class="text">Итеративно:<br>
                    <span class="step-item"><span>Проверка оптимальности (есть ли отрицательные коэффициенты в строке \( Z \)).</span></span>
                    <span class="step-item"><span>Если есть, выбор ведущего столбца (наибольшее по модулю отрицательное число из строки \( Z \)) и строки (минимальное 
                    положительное отношение свободного члена к элементу столбца), пересчет таблицы, вводя новую переменную в базис.</span></span>
                    <span class="indented-text">Все элементы ключевой строки делятся на ключевой элемент, элементы ключевого столбца равны 0.</span></span>
                    <span class="indented-text">Остальные элементы вычисляются по формуле:</span></span>
                    <div class="math" style="text-align: center;">
                        \[
                            a_{ij}' = a_{ij} - \frac{a_{iq} \cdot a_{pj}}{a_{pq}}
                        \]
                    </div>
                    <span class="step-item"><span>Повтор, пока \( Z \) не станет оптимальным.</span></span>
                </li>
                <li class="text">Извлекаем решение: значения \( x_i \) и \( Z \).</li>
            </ol>
        </section>

        <!-- Пример решения -->
        <div class="section">
            <h2>Пример решения</h2>
            <p class="text">Максимизировать:</p>
            <div class="math" style="text-align: center;">
                \[
                    Z = 3x_1 + 2x_2
                \]
            </div>
            <p class="text">Ограничения:</p>
            <div class="math" style="text-align: center;">
                \[
                    2x_1 + x_2 \leq 4
                \]
                \[
                    x_1 + 2x_2 \leq 4
                \]
                \[
                    x_1, x_2 \geq 0
                \]
            </div>
            <h3>Шаг 1: Приведение к стандартной форме</h3>
            <div class="math" style="text-align: center;">
                \[
                    2x_1 + x_2 + s_1 = 4
                \]
                \[
                    x_1 + 2x_2 + s_2 = 4
                \]
                \[
                    Z = 3x_1 + 2x_2
                \]
                \[
                    s_1, s_2 \geq 0
                \]
            </div>
            <h3>Шаг 2: Начальная таблица</h3>
            <!-- Таблица -->
            <table class="custom-table">
                <tr>
                    <th>Базис</th>
                    <th>\( x_1 \)</th>
                    <th>\( x_2 \)</th>
                    <th>\( s_1 \)</th>
                    <th>\( s_2 \)</th>
                    <th>Свободный член</th>
                </tr>
                <tr>
                    <td>\( s_1 \)</td>
                    <td>2</td>
                    <td>1</td>
                    <td>1</td>
                    <td>0</td>
                    <td>4</td>
                </tr>
                <tr>
                    <td>\( s_2 \)</td>
                    <td>1</td>
                    <td>2</td>
                    <td>0</td>
                    <td>1</td>
                    <td>4</td>
                </tr>
                <tr>
                    <td>\( Z \)</td>
                    <td>-3</td>
                    <td>-2</td>
                    <td>0</td>
                    <td>0</td>
                    <td>0</td>
                </tr>
            </table>
            <h3>Шаг 3: Итерации</h3>
            <span class="step-item"><span>Ведущий столбец \( x_1 \) (-3), строка — первая (4/2 = 2)</span></span>
            <span class="step-item"><span>Пересчет таблицы</span></span>
            <!-- Таблица -->
            <table class="custom-table">
                <tr>
                    <th>Базис</th>
                    <th>\( x_1 \)</th>
                    <th>\( x_2 \)</th>
                    <th>\( s_1 \)</th>
                    <th>\( s_2 \)</th>
                    <th>Свободный член</th>
                </tr>
                <tr>
                    <td>\( s_1 \)</td>
                    <td>1</td>
                    <td>0.5</td>
                    <td>0.5</td>
                    <td>0</td>
                    <td>2</td>
                </tr>
                <tr>
                    <td>\( s_2 \)</td>
                    <td>0</td>
                    <td>1.5</td>
                    <td>-0.5</td>
                    <td>1</td>
                    <td>2</td>
                </tr>
                <tr>
                    <td>\( Z \)</td>
                    <td>0</td>
                    <td>-0.5</td>
                    <td>1.5</td>
                    <td>0</td>
                    <td>6</td>
                </tr>
            </table>
            <span class="step-item"><span>Ведущий столбец \( x_2 \) (-0.5), строка — вторая (2/1.5 = 1.33)</span></span>
            <span class="step-item"><span>Итоговая таблица</span></span>
            <!-- Таблица -->
            <table class="custom-table">
                <tr>
                    <th>Базис</th>
                    <th>\( x_1 \)</th>
                    <th>\( x_2 \)</th>
                    <th>\( s_1 \)</th>
                    <th>\( s_2 \)</th>
                    <th>Свободный член</th>
                </tr>
                <tr>
                    <td>\( s_1 \)</td>
                    <td>1</td>
                    <td>0</td>
                    <td>0.67</td>
                    <td>-0.33</td>
                    <td>1.33</td>
                </tr>
                <tr>
                    <td>\( s_2 \)</td>
                    <td>0</td>
                    <td>1</td>
                    <td>-0.33</td>
                    <td>0.67</td>
                    <td>1.33</td>
                </tr>
                <tr>
                    <td>\( Z \)</td>
                    <td>0</td>
                    <td>0</td>
                    <td>1.33</td>
                    <td>0.33</td>
                    <td>6.67</td>
                </tr>
            </table>
            <p class="text">Результат: \( x_1 = 1.33, x_2 = 1.33, Z = 6.67 \).</p>
        </div>
        <hr>
        <!-- Переход к калькулятору -->
        <div class="calc-start-section text-center">
            <h1 class="mb-4">Готовы решить свою задачу?</h1>
            <a href="/direct_lpp_practice" class="btn btn-primary btn-lg">Перейти к калькулятору</a>
        </div>
    </div>
</div>
