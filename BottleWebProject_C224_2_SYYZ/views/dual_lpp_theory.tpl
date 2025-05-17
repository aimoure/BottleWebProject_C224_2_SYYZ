% rebase('layout.tpl', title=title, year=year)

<!-- Подключение MathJax -->
<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>

<div class="hungarian-page">

    <div class="jumbotron">
        <h1>Двойственная задача линейного программирования</h1>
        <p class="lead">
            Суть двойственной задачи линейного программирования состоит в том, чтобы для исходной (прямой) задачи составить связанную с ней двойственную задачу.
        </p>
        <p>
            <a href="/dual_lpp_practice" class="btn btn-warning btn-lg mt-3">Перейти к калькулятору</a>
        </p>
    </div>

    <div class="container">

        <section class="section">
            <h2>Что такое двойственная задача?</h2>
            <p>
                Двойственная задача линейного программирования (ЗЛП) формируется на основе прямой задачи. 
                Она позволяет получить альтернативное решение, а также оценить чувствительность исходной задачи и интерпретировать значения двойственных переменных (теневых цен).
            </p>

            <h3>Формально, если прямая задача имеет вид:</h3>
            <p>Максимизировать</p>
            <div class="math" style="text-align: center;">
                \[
                    Z = c_1 x_1 + c_2 x_2 + \ldots + c_n x_n
                \]
            </div>

            <p>при условиях:</p>
            <div class="math" style="text-align: center;">
                \[
                    a_{1}x_{1} + a_{2}x_{2} + \ldots + a_{n}x_{n} \leq b_{i}
                \]
            </div>

            <h3>То двойственная задача будет:</h3>
            <p>Минимизировать</p>
            <div class="math" style="text-align: center;">
                \[
                    W = b_1 y_1 + b_2 y_2 + \ldots + b_m y_m
                \]
            </div>

            <p>при условиях:</p>
            <div class="math" style="text-align: center;">
                \[
                    a_{1}y_{1} + a_{2}y_{2} + \ldots + a_{m}y_{m} \geq c_{j}
                \]
            </div>

            <div class="math" style="text-align: center;">
                где \( y_i \geq 0 \).
            </div>
        </section>

        <section class="section">
            <h2>Симплекс-метод</h2>
            <p>
                Двойственная задача решается с использованием классического симплекс-метода, который работает следующим образом:
            </p>
            <ol>
                <li>
                    <p>Преобразование к стандартной форме. Все неравенства вида \( \geq \) приводятся к уравнениям путём введения дополнительных переменных.</p>
                </li>
                <li>
                    <p>Составление начальной симплекс-таблицы. Формируется начальная таблица, где строки — ограничения, а последняя строка — целевая функция.</p>
                </li>
                <li>
                    <p>Итерации симплекс-метода:</p>
                    <ul>
                        <li class="step-item">Проверить оптимальность текущего решения (отрицательные коэффициенты в последней строке таблицы).</li>
                        <li class="step-item">Если решение не оптимально, выбрать разрешающий столбец (наиболее отрицательный коэффициент).</li>
                        <li class="step-item">Затем выбрать разрешающую строку (минимальное положительное отношение правой части к элементу столбца).</li>
                        <li class="step-item">Пересчитать таблицу.</li>
                    </ul>
                    <div class="math" style="text-align: center;">
                        \[
                            a'_{ij} = a_{ij} - \frac{a_{iq} \cdot a_{pj}}{a_{pq}}
                        \]
                    </div>
                    <div class="math" style="text-align: center;">
                        где \( p \) — разрешающая строка, \( q \) — разрешающий столбец.
                    </div>
                </li>
                <li>
                    <p>Извлекаем решение: значения \( y_i \) и \( W \).</p>
                </li>
            </ol>
        </section>


        <div class="section">
            <h2>Пример решения</h2>
            <p class="text">Исходная прямая задача — максимизировать:</p>
            <div class="math" style="text-align: center;">
                \[
                    Z = 3x_1 + 2x_2
                \]
            </div>
            <p>при условиях:</p>
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
            <p>Для задачи максимизации с ограничениями вида \( \leq \), двойственная будет задачей минимизации с ограничениями вида \( \geq \). 
            Переменные двойственной задачи — \(y_1, y_2\) — будут связаны с ограничениями прямой задачи.</p>
            <p class="text">Составим двойственную задачу — минимизировать:</p>
            <div class="math" style="text-align: center;">
                \[
                    W = 4y_1 + 4y_2
                \]
            </div>
            <p>при условиях:</p>
            <div class="math" style="text-align: center;">
                \[
                    2y_1 + y_2 \geq 3
                \]
                 \[
                    y_1 + 2y_2 \geq 2
                \]
                 \[
                    y_1, y_2 \geq 0
                \]
            </div>
        </div>

       <div class="section">
            <h3>Итоговая двойственная задача:</h3>
            <p class="text">Минимизировать:</p>
            <div class="math" style="text-align: center;">
                \[
                    W = 4y_{1} + 4y_{2}
                \]
            </div>
            <p class="text">при условиях:</p>
            <div class="math" style="text-align: center;">
                \[
                    2y_{1} + 1y_{2} \geq 3
                \]
                \[
                    1y_{1} + 2y_{2} \geq 2
                \]
                \[
                    y_{1}, y_{2} \geq 0
                \]
            </div>

            <!-- Шаг 1: стандартная форма -->
            <p class="text">Шаг 1: Приведение к стандартной форме (умножаем неравенства на −1 и вводим \(t_1\), \(t_2\)):</p>
            <div class="math" style="text-align: center;">
                \[
                    -2y_{1} - 1y_{2} + t_{1} = -3
                \]
                \[
                    -1y_{1} - 2y_{2} + t_{2} = -2
                \]
                \[
                    W = 4y_{1} + 4y_{2}
                \]
            </div>
            <div class="math" style="text-align: center;">
                \[
                    t_{1}, t_{2} \geq 0
                \]
            </div>

            <!-- Шаг 2: начальная симплекс‑таблица -->
            <p class="text">Шаг 2: Начальная таблица</p>
            <table class="custom-table">
                <tr>
                    <th>Базис</th><th>\(y_{1}\)</th><th>\(y_{2}\)</th><th>\(t_{1}\)</th><th>\(t_{2}\)</th><th>Свободный член</th>
                </tr>
                <tr>
                    <td>\(t_{1}\)</td><td>-2</td><td>-1</td><td>1</td><td>0</td><td>-3</td>
                </tr>
                <tr>
                    <td>\(t_{2}\)</td><td>-1</td><td>-2</td><td>0</td><td>1</td><td>-2</td>
                </tr>
                <tr>
                    <td>\(W\)</td><td>4</td><td>4</td><td>0</td><td>0</td><td>0</td>
                </tr>
            </table>

            <!-- Шаг 3: первая итерация -->
            <p class="text">Шаг 3: Итерация 1</p>
            <span class="step-item"><span>Ведущий столбец \(y_{1}\) (–4), ведущая строка \(t_{1}\) (–3/–2 = 1.5).</span></span><br>
            <span class="step-item"><span>Делим первую строку на –2, затем зануляем \(y_{1}\) в остальных строках.</span></span>
            <table class="custom-table">
                <tr>
                    <th>Базис</th><th>\(y_{1}\)</th><th>\(y_{2}\)</th><th>\(t_{1}\)</th><th>\(t_{2}\)</th><th>Свободный член</th>
                </tr>
                <tr>
                    <td>\(y_{1}\)</td><td>1</td><td>0.5</td><td>-0.5</td><td>0</td><td>1.5</td>
                </tr>
                <tr>
                    <td>\(t_{2}\)</td><td>0</td><td>-1.5</td><td>-0.5</td><td>1</td><td>-0.5</td>
                </tr>
                <tr>
                    <td>\(W\)</td><td>0</td><td>-2</td><td>2</td><td>0</td><td>6</td>
                </tr>
            </table>

            <!-- Шаг 4: вторая итерация -->
            <p class="text">Шаг 4: Итерация 2</p>
            <span class="step-item"><span>Ведущий столбец \(y_{2}\) (–2), ведущая строка \(t_{2}\) (–0.5/–1.5 ≈ 0.33).</span></span><br>
            <span class="step-item"><span>Делим вторую строку на –1.5, затем зануляем \(y_{2}\) в остальных строках.</span></span>
            <table class="custom-table">
                <tr>
                    <th>Базис</th><th>\(y_{1}\)</th><th>\(y_{2}\)</th><th>\(t_{1}\)</th><th>\(t_{2}\)</th><th>Свободный член</th>
                </tr>
                <tr>
                    <td>\(y_{1}\)</td><td>1</td><td>0</td><td>-0.67</td><td>0.33</td><td>1.33</td>
                </tr>
                <tr>
                    <td>\(y_{2}\)</td><td>0</td><td>1</td><td>0.33</td><td>-0.67</td><td>0.33</td>
                </tr>
                <tr>
                    <td>\(W\)</td><td>0</td><td>0</td><td>2.67</td><td>-1.33</td><td>6.67</td>
                </tr>
            </table>

            <!-- Итоговый результат -->
            <p class="text">Результат: \(y_{1} = 1.33\), \(y_{2} = 0.33\), \(W = 6.67\).</p>
            <p class="text">Проверим двойственность: \(Z = W = 6.67\).</p>
            <p class="text">Все условия двойственности выполняются.</p>
        </div>

        <hr>
        <div class="calc-start-section text-center">
            <h1 class="mb-4">Готовы решить свою задачу?</h1>
            <a href="/dual_lpp_practice" class="btn btn-primary btn-lg">Перейти к калькулятору</a>
        </div>
    </div>
</div>
