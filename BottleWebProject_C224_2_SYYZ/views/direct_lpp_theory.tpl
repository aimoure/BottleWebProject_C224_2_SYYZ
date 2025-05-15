% rebase('layout.tpl', title=title, year=year)

<div class="jumbotron">
	<h1>Прямая задача линейного программирования</h1>
	<p class="lead">
        Суть прямой задачи линейного программирования состоит в том, чтобы максимизировать или минимизировать линейную функцию в условиях, выраженных системой линейных ограничений.
    </p>
</div>

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
        <li class="text">&emsp;Приведение задачи к стандартной форме, добавляя дополнительные переменные для неравенств.</li>
        <li class="text">&emsp;Построение начальной симплекс-таблицы, где строки — ограничения, а последняя строка — целевая функция.</li>
        <li class="text">&emsp;Итеративно:<br>
            <span class="step-item"><span>Проверка оптимальности (есть ли отрицательные коэффициенты в строке Z).</span></span>
            <span class="step-item"><span>Если есть, выбор ведущего столбца (наибольшее по модулю отрицательное число из столбца Z) и строки (минимальное положительное отношение свободного члена к элементу столбца), пересчет таблицы, вводя новую переменную в базис.</span></span>
            <span class="indented-text">Все элементы ключевой строки делятся на ключевой элемент, элементы ключевого столбца равны 0.</span>
            <span class="indented-text">Остальные элементы вычисляются по формуле:</span>
            <span class="formula">a<sub>ij</sub>' = a<sub>ij</sub> - (a<sub>iq</sub> * a<sub>pj</sub>) / a<sub>pq</sub>,</span>
            <span class="formula">где p – ключевая строка, q – ключевой столбец</span>
            <span class="step-item"><span>Повтор, пока Z не станет оптимальным.</span></span>
        </li>
        <li class="text">&emsp;Извлекаем решение: значения x<sub>i</sub> и Z.</li>
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
    <p class="text">Шаг 1: Приведение к стандартной форме:</p>
    <p class="formula">2x<sub>1</sub> + x<sub>2</sub> + s<sub>1</sub> = 4</p>
    <p class="formula">x<sub>1</sub> + 2x<sub>2</sub> + s<sub>2</sub> = 4</p>
    <p class="formula">Z = 3x<sub>1</sub> + 2x<sub>2</sub></p>
    <p class="formula">где s<sub>1</sub>, s<sub>2</sub> ≥ 0</p>
</div>