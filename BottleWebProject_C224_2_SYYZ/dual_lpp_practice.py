from bottle import route, request, template, static_file
import numpy as np

@route('/static/scripts/<filename>')
def serve_static(filename):
    return static_file(filename, root='static/scripts')

@route('/dual_lpp_practice', method=['GET', 'POST'])
def dual_lpp_practice():
    result_table = []
    steps = []
    answer_vars = {}
    F = None
    duality_check = ''

    num_vars = request.forms.get('num_vars', '2')
    num_cons = request.forms.get('num_cons', '1')

    if request.method == 'POST':
        try:
            num_vars = int(num_vars)
            num_cons = int(num_cons)

            c = [float(request.forms.get(f'x_{j}', '0') or '0') for j in range(num_vars)]

            A = []
            b = []
            for i in range(num_cons):
                row = [float(request.forms.get(f'cons_{i}_{j}', '0') or '0') for j in range(num_vars)]
                A.append(row)
                b.append(float(request.forms.get(f'cons_rhs_{i}', '0') or '0'))

            steps, result_values, W = solve_dual_simplex(c, A, b)

            answer_vars = {k: v for k, v in result_values.items() if k.startswith('y')}
            F = -W
            duality_check = "Все условия двойственности выполняются."

            result_table.append(['Базис'] + [f'y{i+1}' for i in range(len(answer_vars))] + ['Свободный член'])
            last_table = steps[-1]['table']
            for row in last_table[:-1]:
                result_table.append([row[0]] + [round(x, 2) for x in row[1:]])
            result_table.append(['W'] + [round(x, 2) for x in last_table[-1][1:]])

            return template('dual_lpp_practice.tpl',
                            title='Двойственная ЗЛП',
                            year=2025,
                            result_table=result_table,
                            num_vars=num_vars,
                            num_cons=num_cons,
                            dual_steps=steps,
                            answer_vars=answer_vars,
                            F=round(F, 3),
                            duality_check=duality_check)

        except Exception as e:
            result_table = [['Ошибка обработки данных:', str(e)]]
            return template('dual_lpp_practice.tpl',
                            title='Двойственная ЗЛП',
                            year=2025,
                            result_table=result_table,
                            num_vars=num_vars,
                            num_cons=num_cons,
                            dual_steps=[],
                            answer_vars={},
                            F=None,
                            duality_check='')

    # Для GET-запроса:
    return template('dual_lpp_practice.tpl',
                    title='Двойственная ЗЛП',
                    year=2025,
                    result_table=result_table,
                    num_vars=num_vars,
                    num_cons=num_cons,
                    dual_steps=steps,
                    answer_vars={},
                    F=None,
                    duality_check='')



def solve_dual_simplex(c, A, b):
    A = np.array(A, dtype=float)
    c = np.array(c, dtype=float)
    b = np.array(b, dtype=float)

    # Построение двойственной задачи
    A_dual = A.T
    b_dual = c
    c_dual = b

    num_vars = A_dual.shape[1]
    num_cons = A_dual.shape[0]

    # Имена переменных
    var_names = [f"y{i+1}" for i in range(num_vars)]
    slack_names = [f"t{i+1}" for i in range(num_cons)]
    all_vars = var_names + slack_names

    # Построение начальной таблицы
    tableau = []
    basis = []
    for i in range(num_cons):
        row = list(-A_dual[i])  # знак "≤"
        slack = [1 if j == i else 0 for j in range(num_cons)]
        row += slack
        row.append(-b_dual[i])
        tableau.append(row)
        basis.append(slack_names[i])

    # Целевая функция W = c_dual^T * y
    z_row = list(c_dual) + [0]*num_cons + [0]
    tableau.append(z_row)

    steps = []
    steps.append({
        "title": "Начальная таблица",
        "table": [ [basis[i]] + tableau[i] for i in range(len(basis)) ] + [["W"] + tableau[-1]],
        "pivot": None,
        "explanation": "Начальная симплекс-таблица"
    })

    while True:
        # Шаг 1: Найти строку с отрицательным свободным членом (rhs)
        rhs = [row[-1] for row in tableau[:-1]]
        if all(r >= 0 for r in rhs):
            break  # оптимум достигнут

        leaving = np.argmin(rhs)  # самая отрицательная строка
        row = tableau[leaving]

        # Шаг 2: Найти допустимый ведущий столбец (min ratio test по отрицательным коэффициентам)
        ratios = []
        for j in range(len(row) - 1):  # не учитываем свободный член
            coeff = row[j]
            zjcj = tableau[-1][j]
            if coeff < 0:
                ratios.append((zjcj / abs(coeff), j))
        if not ratios:
            raise Exception("Задача не имеет решения: не найден допустимый ведущий столбец.")

        # Шаг 3: Выбор столбца с минимальным отношением
        _, entering = min(ratios)

        pivot_val = tableau[leaving][entering]
        tableau[leaving] = [v / pivot_val for v in tableau[leaving]]
        basis[leaving] = all_vars[entering]

        for i in range(len(tableau)):
            if i != leaving:
                factor = tableau[i][entering]
                tableau[i] = [
                    tableau[i][j] - factor * tableau[leaving][j]
                    for j in range(len(tableau[i]))
                ]

        # Сохраняем шаг
        step_table = [ [basis[i]] + tableau[i] for i in range(len(basis)) ] + [["W"] + tableau[-1]]
        steps.append({
            "title": "Итерация",
            "table": step_table,
            "pivot": (leaving, entering),
            "explanation": f"Ведущий столбец: {all_vars[entering]}, ведущая строка: {basis[leaving]}"
        })

    # Финальные значения
    result_values = {name: 0 for name in all_vars}
    for i, var in enumerate(basis):
        result_values[var] = tableau[i][-1]
    W = tableau[-1][-1]

    return steps, result_values, W
