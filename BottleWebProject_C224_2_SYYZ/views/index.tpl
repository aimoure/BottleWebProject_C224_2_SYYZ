% rebase('layout.tpl', title='Home Page', year=year)

<div class="hungarian-page">
    <div class="jumbotron">
        <h1>DualSolve</h1>
        <p class="lead">DualSolve — образовательный сайт, посвященный изучению и решению задач линейного программирования: транспортной задачи, задачи о назначениях, прямой и двойственной ЗЛП. Доступное и структурированное освоение методов оптимизации для студентов и специалистов.</p>
    </div>

    <div class="container">
        <!-- Верхний ряд: два контейнера -->
        <div class="row">
            <!-- Транспортная задача -->
            <div class="col-md-6 task-container" style="margin-bottom: 40px;">
                <div class="task-card">
                    <div>
                        <h3>Транспортная задача</h3>
                        <p>Минимизирует затраты на перевозки ресурсов от поставщиков к потребителям. Решается методами северо-западного угла или потенциалов.</p>
                    </div>
                    <p><a class="btn" href="/transportation-problem">Перейти к решению</a></p>
                </div>
            </div>

            <!-- Задача о назначениях -->
            <div class="col-md-6 task-container" style="margin-bottom: 40px;">
                <div class="task-card">
                    <div>
                        <h3>Задача о назначениях</h3>
                        <p>Оптимально распределяет задания между исполнителями, минимизируя затраты. Решается венгерским алгоритмом.</p>
                    </div>
                    <p><a class="btn" href="/assignment-problem">Перейти к решению</a></p>
                </div>
            </div>
        </div>

        <!-- Нижний ряд: два контейнера -->
        <div class="row">
            <!-- Прямая ЗЛП -->
            <div class="col-md-6 task-container" style="margin-bottom: 40px;">
                <div class="task-card">
                    <div>
                        <h3>Прямая задача линейного программирования (ЗЛП)</h3>
                        <p>Оптимизирует целевую функцию при линейных ограничениях. Решается симплекс-методом.</p>
                    </div>
                    <p><a class="btn" href="/primal-zlp">Перейти к решению</a></p>
                </div>
            </div>

            <!-- Двойственная ЗЛП -->
            <div class="col-md-6 task-container" style="margin-bottom: 40px;">
                <div class="task-card">
                    <div>
                        <h3>Двойственная задача линейного программирования</h3>
                        <p>Анализирует ресурсы и их ценность, дополняя прямую задачу. Оценивает чувствительность решения.</p>
                    </div>
                    <p><a class="btn" href="/dual-zlp">Перейти к решению</a></p>
                </div>
            </div>
        </div>
    </div>
</div>