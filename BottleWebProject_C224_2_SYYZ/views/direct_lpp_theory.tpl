% rebase('layout.tpl', title=title, year=year)

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

    <div class="container">
        <div class="section">
            <h2>Определение задачи</h2>
            <p class="text">
                Прямая задача линейного программирования (ЗЛП) — задача оптимизации, где нужно максимизировать или минимизировать линейную целевую функцию 
                <span class="center">Z = c<sub>1</sub>x<sub>1</sub> + c<sub>2</sub>x<sub>2</sub> + … + c<sub>n</sub>x<sub>n</sub></span>
                при условии, что переменные x<sub>i</sub> удовлетворяют системе линейных ограничений, например, a<sub>1</sub>x<sub>3</sub> + a<sub>2</sub>x<sub>5</sub> ≤ b<sub>1</sub> и условию неотрицательности x<sub>i</sub> ≥ 0.
            </p>
            <p class="text">Цель — найти такие x<sub>i</sub>, чтобы Z была оптимальной.</p>
            <p class="text">Основным методом для решения прямой ЗЛП является симплекс метод.</p>
        </div>

        <section class="section">
            <h2>Симплекс-метод</h2>
            <p class="text">
                Симплекс-метод — это алгоритм решения ЗЛП, который работает следующим образом:
            </p>
            <ol class="list">
                <li class="text">Приведение задачи к стандартной форме, добавляя дополнительные переменные для неравенств.</li>
                <li class="text">Построение начальной симплекс-таблицы, где строки — ограничения, а последняя строка — целевая функция.</li>
                <li class="text">Итеративно:<br>
                    <span class="step-item"><span>Проверка оптимальности (есть ли отрицательные коэффициенты в строке Z).</span></span>
                    <span class="step-item"><span>Если есть, выбор ведущего столбца (наибольшее по модулю отрицательное число из столбца Z) и строки (минимальное положительное отношение свободного члена к элементу столбца), пересчет таблицы, вводя новую переменную в базис.</span></span>
                    <span class="indented-text">Все элементы ключевой строки делятся на ключевой элемент, элементы ключевого столбца равны 0.</span>
                    <span class="indented-text">Остальные элементы вычисляются по формуле:</span>
                    <span class="formula">a<sub>ij</sub>' = a<sub>ij</sub> - (a<sub>iq</sub> * a<sub>pj</sub>) / a<sub>pq</sub>,</span>
                    <span class="formula">где p – ключевая строка, q – ключевой столбец</span>
                    <span class="step-item"><span>Повтор, пока Z не станет оптимальным.</span></span>
                </li>
                <li class="text">Извлекаем решение: значения x<sub>i</sub> и Z.</li>
            </ol>
        </section>

        <div class="section">
            <h2>Пример решения</h2>
            <p class="text">Максимизировать:</p>
            <p class="formula">Z = 3x<sub>1</sub> + 2x<sub>2</sub></p>
            <p class="text">Ограничения:</p>
            <p class="formula">2x<sub>1</sub> + x<sub>2</sub> ≤ 4</p>
            <p class="formula">x<sub>1</sub> + 2x<sub>2</sub> ≤ 4</p>
            <p class="formula">x<sub>1</sub>, x<sub>2</sub> ≥ 0</p>
            <h3>Шаг 1: Приведение к стандартной форме</h3>
            <p class="formula">2x<sub>1</sub> + x<sub>2</sub> + s<sub>1</sub> = 4</p>
            <p class="formula">x<sub>1</sub> + 2x<sub>2</sub> + s<sub>2</sub> = 4</p>
            <p class="formula">Z = 3x<sub>1</sub> + 2x<sub>2</sub></p>
            <p class="formula">где s<sub>1</sub>, s<sub>2</sub> ≥ 0</p>
            <h3>Шаг 2: Начальная таблица</h3>
            <table class="custom-table">
                <tr>
                    <th>Базис</th>
                    <th>x<sub>1</sub></th>
                    <th>x<sub>2</sub></th>
                    <th>s<sub>1</sub></th>
                    <th>s<sub>2</sub></th>
                    <th>Свободный член</th>
                </tr>
                <tr>
                    <td>s<sub>1</sub></td>
                    <td>2</td>
                    <td>1</td>
                    <td>1</td>
                    <td>0</td>
                    <td>4</td>
                </tr>
                <tr>
                    <td>s<sub>2</sub></td>
                    <td>1</td>
                    <td>2</td>
                    <td>0</td>
                    <td>1</td>
                    <td>4</td>
                </tr>
                <tr>
                    <td>Z</td>
                    <td>-3</td>
                    <td>-2</td>
                    <td>0</td>
                    <td>0</td>
                    <td>0</td>
                </tr>
            </table>
            <h3>Шаг 3: Итерации</h3> 
            <span class="step-item"><span>Ведущий столбец x<sub>1</sub> (-3), строка — первая (4/2 = 2)</span></span>
            <span class="step-item"><span>Пересчет таблицы</span></span>
            <table class="custom-table">
                <tr>
                    <th>Базис</th>
                    <th>x<sub>1</sub></th>
                    <th>x<sub>2</sub></th>
                    <th>s<sub>1</sub></th>
                    <th>s<sub>2</sub></th>
                    <th>Свободный член</th>
                </tr>
                <tr>
                    <td>s<sub>1</sub></td>
                    <td>1</td>
                    <td>0.5</td>
                    <td>0.5</td>
                    <td>0</td>
                    <td>2</td>
                </tr>
                <tr>
                    <td>s<sub>2</sub></td>
                    <td>0</td>
                    <td>1.5</td>
                    <td>-0.5</td>
                    <td>1</td>
                    <td>2</td>
                </tr>
                <tr>
                    <td>Z</td>
                    <td>0</td>
                    <td>-0.5</td>
                    <td>1.5</td>
                    <td>0</td>
                    <td>6</td>
                </tr>
            </table>
            <span class="step-item"><span>Ведущий столбец x<sub>2</sub> (-0.5), строка — вторая (2/1.5 = 1.33)</span></span>
            <span class="step-item"><span>Итоговая таблица</span></span>
            <table class="custom-table">
                <tr>
                    <th>Базис</th>
                    <th>x<sub>1</sub></th>
                    <th>x<sub>2</sub></th>
                    <th>s<sub>1</sub></th>
                    <th>s<sub>2</sub></th>
                    <th>Свободный член</th>
                </tr>
                <tr>
                    <td>s<sub>1</sub></td>
                    <td>1</td>
                    <td>0</td>
                    <td>0.67</td>
                    <td>-0.33</td>
                    <td>1.33</td>
                </tr>
                <tr>
                    <td>s<sub>2</sub></td>
                    <td>0</td>
                    <td>1</td>
                    <td>-0.33</td>
                    <td>0.67</td>
                    <td>1.33</td>
                </tr>
                <tr>
                    <td>Z</td>
                    <td>0</td>
                    <td>0</td>
                    <td>1.33</td>
                    <td>0.33</td>
                    <td>6.67</td>
                </tr>
            </table>
            <span class="text"><span>Результат: x<sub>1</sub> = 1.33, x<sub>2</sub> = 1.33, Z = 6.67.</span></span>
        </div>

        <hr>
        <div class="calc-start-section text-center">
            <h1 class="mb-4">Готовы решить свою задачу?</h1>
            <a href="/direct_lpp_practice" class="btn btn-primary btn-lg">Перейти к калькулятору</a>
        </div>
    </div>
</div>