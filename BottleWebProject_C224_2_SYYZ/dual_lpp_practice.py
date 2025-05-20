from bottle import redirect, route, request, template, static_file
import numpy as np
import os
import json
import datetime
import random

# Исключение при отсутствии допустимого решения
class NoSolutionError(Exception):
    """Исключение для задач без допустимого решения."""
    pass

# Сохранение результатов в JSON-файл
def save_result_to_json(record, filename='input/dual_lpp_results.json'):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
    else:
        data = []
    data.append(record)
    with open(filename, 'w', encoding='utf-8-sig') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Костыль для замены битых символов
corrupted_sign_map = {
    'â\u0089¤': '≤',
    'â\u0089¥': '≥',
    'â¤': '≤',
    'â¥': '≥',
    '<=': '≤',
    '>=': '≥'
}

# Статика
@route('/static/scripts/<filename>')
def serve_static(filename):
    return static_file(filename, root='static/scripts')

# Маршрут для загрузки случайного примера
@route('/dual_lpp_example', method='POST')
def dual_lpp_example():
    example_file = 'output/dual_lpp_examples.json'

    if not os.path.exists(example_file):
        return "Файл с примерами не найден."

    with open(example_file, 'r', encoding='utf-8-sig') as f:
        examples = json.load(f)

    if not examples:
        return "Нет доступных примеров."

    # Выбираем случайный пример из списка и берем поле 'input'
    random_example = random.choice(examples)['input']

    # Сохраняем этот пример в отдельный файл для загрузки в форму
    input_filename = 'input/dual_lpp_last_input.json'
    os.makedirs(os.path.dirname(input_filename), exist_ok=True)
    with open(input_filename, 'w', encoding='utf-8-sig') as f:
        json.dump(random_example, f, ensure_ascii=False, indent=2)

    return redirect('/dual_lpp_practice')

# Основной маршрут
@route('/dual_lpp_practice', method=['GET', 'POST'])
def dual_lpp_practice():
    result_table = []
    steps = []
    answer_vars = {}
    F = None
    primal_obj = ''
    dual_obj = ''
    primal_constraints = []
    dual_constraints = []
    duality_check = ''
    no_solution = False
    error_message = ''
    form_data = {}

    if request.method == 'GET':
        # Попытка загрузить последний пример из файла
        input_filename = 'input/dual_lpp_last_input.json'
        if os.path.exists(input_filename):
            try:
                with open(input_filename, 'r', encoding='utf-8-sig') as f:
                    last_input = json.load(f)

                c = last_input.get('objective_coeffs', [])
                A = last_input.get('constraint_coeffs', [])
                b = last_input.get('rhs_values', [])
                signs = last_input.get('constraint_signs', [])

                num_vars = len(c)
                num_cons = len(A)

                # Решаем задачу сразу
                steps, result_values, W = solve_dual_simplex(c, A, b)
                answer_vars = {k: round(v, 2) for k, v in result_values.items() if k.startswith('y')}
                F = round(-W, 2)
                duality_check = "Все условия двойственности выполняются."

                # Формирование таблицы
                result_table.append(['Базис'] + [f'y{i+1}' for i in range(num_cons)] + ['Св.член'])
                last = steps[-1]['table']
                for row in last[:-1]:
                    result_table.append([row[0]] + [round(x, 2) for x in row[1:]])
                result_table.append(['W'] + [round(x, 2) for x in last[-1][1:]])

                # Формулировки
                x_vars = [f'x{i+1}' for i in range(num_vars)]
                y_vars = [f'y{i+1}' for i in range(num_cons)]
                primal_obj = f"Z = {format_expression(c, x_vars)}"
                primal_constraints = [format_expression(A[i], x_vars, b[i], '≤') for i in range(num_cons)]
                A_dual = np.array(A).T.tolist()
                dual_obj = f"W = {format_expression(b, y_vars)}"
                dual_constraints = [format_expression(A_dual[i], y_vars, c[i], '≥') for i in range(num_vars)]

                form_data = {'x': c, 'cons': A, 'signs': signs, 'rhs': b}

            except Exception as e:
                no_solution = True
                error_message = f"Ошибка загрузки примера: {str(e)}"
                num_vars = 2
                num_cons = 1
        else:
            # Если файла нет — пустая форма
            num_vars = 2
            num_cons = 1

        return template('dual_lpp_practice.tpl',
                        title='Двойственная ЗЛП',
                        year=2025,
                        num_vars=num_vars,
                        num_cons=num_cons,
                        result_table=result_table if result_table else None,
                        dual_steps=steps if steps else None,
                        answer_vars=answer_vars,
                        F=F,
                        duality_check=duality_check,
                        primal_obj=primal_obj,
                        primal_constraints=primal_constraints,
                        dual_obj=dual_obj,
                        dual_constraints=dual_constraints,
                        no_solution=no_solution,
                        error_message=error_message,
                        form_data=form_data)

    # Если POST — берём из формы
    num_vars = int(request.forms.get('num_vars', '2'))
    num_cons = int(request.forms.get('num_cons', '1'))

    try:
        # Целевая функция
        raw_c = [request.forms.get(f'x_{j}', '') for j in range(num_vars)]
        if not any(cell.strip() for cell in raw_c):
            raise Exception("Целевая функция не может быть пустой.")
        c = [float(val or '0') for val in raw_c]
        if all(coef == 0 for coef in c):
            raise Exception("Коэффициенты целевой функции не могут быть все нулями.")

        # Ограничения
        A, b, signs = [], [], []
        for i in range(num_cons):
            row_raw = [request.forms.get(f'cons_{i}_{j}', '') for j in range(num_vars)]
            if not any(cell.strip() for cell in row_raw):
                raise Exception(f"Ограничение {i+1} не может быть пустым.")
            row = [float(val or '0') for val in row_raw]
            if all(val == 0 for val in row):
                raise Exception(f"Ограничение {i+1} не может состоять только из нулей.")
            A.append(row)

            raw_sign = request.forms.get(f'cons_sign_{i}', '≤')
            signs.append(corrupted_sign_map.get(raw_sign, raw_sign))

            b_val = request.forms.get(f'cons_rhs_{i}', '').strip()
            if b_val == '':
                raise Exception(f"Свободный член ограничения №{i+1} не может быть пустым.")
            b.append(float(b_val))

        # Решаем
        steps, result_values, W = solve_dual_simplex(c, A, b)
        answer_vars = {k: round(v, 2) for k, v in result_values.items() if k.startswith('y')}
        F = round(-W, 2)
        duality_check = "Все условия двойственности выполняются."

        # Сохраняем
        record = {
            "timestamp": datetime.datetime.now().isoformat(),
            "input": {
                "objective_coeffs": c,
                "constraint_coeffs": A,
                "rhs_values": b,
                "constraint_signs": signs
            },
            "output": {
                "dual_variables": answer_vars,
                "dual_objective_value": F
            }
        }
        save_result_to_json(record)

        # Таблица
        result_table.append(['Базис'] + [f'y{i+1}' for i in range(num_cons)] + ['Св.член'])
        last = steps[-1]['table']
        for row in last[:-1]:
            result_table.append([row[0]] + [round(x, 2) for x in row[1:]])
        result_table.append(['W'] + [round(x, 2) for x in last[-1][1:]])

        # Формулировки
        x_vars = [f'x{i+1}' for i in range(num_vars)]
        y_vars = [f'y{i+1}' for i in range(num_cons)]
        primal_obj = f"Z = {format_expression(c, x_vars)}"
        primal_constraints = [format_expression(A[i], x_vars, b[i], '≤') for i in range(num_cons)]
        A_dual = np.array(A).T.tolist()
        dual_obj = f"W = {format_expression(b, y_vars)}"
        dual_constraints = [format_expression(A_dual[i], y_vars, c[i], '≥') for i in range(num_vars)]

        form_data = {'x': c, 'cons': A, 'signs': signs, 'rhs': b}

    except Exception as e:
        no_solution = True
        error_message = str(e)

    return template('dual_lpp_practice.tpl',
                    title='Двойственная ЗЛП',
                    year=2025,
                    num_vars=num_vars,
                    num_cons=num_cons,
                    result_table=result_table,
                    dual_steps=steps,
                    answer_vars=answer_vars,
                    F=F,
                    duality_check=duality_check,
                    primal_obj=primal_obj,
                    primal_constraints=primal_constraints,
                    dual_obj=dual_obj,
                    dual_constraints=dual_constraints,
                    no_solution=no_solution,
                    error_message=error_message,
                    form_data=form_data)

# Двойственный симплекс-метод
def solve_dual_simplex(c, A, b):
    A = np.array(A, float)
    c = np.array(c, float)
    b = np.array(b, float)
    A_dual, b_dual, c_dual = A.T, c, b
    nV, nC = A_dual.shape[1], A_dual.shape[0]
    var_n = [f"y{i+1}" for i in range(nV)]
    slack = [f"t{i+1}" for i in range(nC)]
    allv = var_n + slack

    Tkl = []
    base = []
    for i in range(nC):
        row = list(-A_dual[i]) + [1 if j == i else 0 for j in range(nC)] + [-b_dual[i]]
        Tkl.append(row)
        base.append(slack[i])
    Tkl.append(list(c_dual) + [0] * nC + [0])

    steps = [{"title": "Начальная таблица", "table": [[base[i]] + Tkl[i] for i in range(nC)] + [["W"] + Tkl[-1]], "explanation": "Начальная симплекс-таблица"}]

    while True:
        last = Tkl
        base_row_vals = [last[i][-1] for i in range(nC)]
        if all(x >= 0 for x in base_row_vals):
            break

        pivot_row = base_row_vals.index(min(base_row_vals))
        pivot_candidates = [(j, last[-1][j] / last[pivot_row][j]) for j in range(nV + nC) if last[pivot_row][j] < 0]
        if not pivot_candidates:
            raise NoSolutionError("Решение не найдено")

        pivot_col = min(pivot_candidates, key=lambda x: x[1])[0]

        pivot = last[pivot_row][pivot_col]
        last[pivot_row] = [x / pivot for x in last[pivot_row]]
        for i in range(nC + 1):
            if i != pivot_row:
                ratio = last[i][pivot_col]
                last[i] = [last[i][j] - ratio * last[pivot_row][j] for j in range(len(last[i]))]

        base[pivot_row] = allv[pivot_col]

        steps.append({"title": f"Шаг {len(steps)}", "table": [[base[i]] + last[i] for i in range(nC)] + [["W"] + last[-1]], "explanation": f"Пивот: строка {pivot_row+1}, столбец {pivot_col+1}"})

    results = {}
    for i, var in enumerate(var_n):
        if var in base:
            idx = base.index(var)
            results[var] = last[idx][-1]
        else:
            results[var] = 0.0

    W = last[-1][-1]
    return steps, results, W

# Форматирование выражения для отображения
def format_expression(coefs, vars, rhs=None, sign=None):
    terms = []
    for a, v in zip(coefs, vars):
        if a == 0:
            continue
        a_str = f"{a:+g}" if terms else f"{a:g}"
        if abs(a) == 1:
            a_str = a_str.replace("1", "")
        terms.append(f"{a_str}{v}")
    expr = " ".join(terms).replace("+ -", "- ")
    if rhs is not None and sign is not None:
        expr += f" {sign} {rhs:g}"
    return expr if expr else "0"

