from bottle import route, request, template, static_file
import numpy as np
import os, json, random, datetime

# --- Константы файлов для примеров и результатов ---
EXAMPLES_FILE = 'examples/dual_lpp_examples.json'
RESULTS_FILE  = 'results/dual_lpp_results.json'

# --- Исключение, сигнализирующее об отсутствии допустимого решения ---
class NoSolutionError(Exception):
    pass

# --- Запись структуры record в JSON-файл истории результатов ---
def save_result_to_json(record, filename=RESULTS_FILE):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    data = json.load(open(filename, encoding='utf-8-sig')) if os.path.exists(filename) else []
    data.append(record)
    with open(filename, 'w', encoding='utf-8-sig') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# --- Преобразование числа к строке без ненужной дробной части (4.0 → "4") ---
def format_num(v):
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return str(v)

# --- Построение терма вида "3x1", "-x2" и т.п., пропуская нулевые коэффициенты ---
def format_term(coef, var):
    if coef == 0:
        return ''
    i = int(coef)
    if coef == 1:
        return var
    if coef == -1:
        return f"-{var}"
    return f"{i if coef == i else coef}{var}"

# --- Сборка полного линейного выражения с возможным знаком и правой частью ---
def format_expression(coeffs, vars_list, rhs=None, sign=None):
    terms = [format_term(c, v) for c, v in zip(coeffs, vars_list)]
    expr = ' + '.join(filter(None, terms)).replace('+ -', '- ')
    if sign and rhs is not None:
        r = int(rhs)
        rs = str(r if rhs == r else rhs)
        return f"{expr} {sign} {rs}"
    return expr

# --- Отображение "битых" символов сравнения в корректные знаки ≤ и ≥ ---
_corrupted = {'<=': '≤', '>=': '≥', 'â¤': '≤', 'â¥': '≥'}
def clean_sign(s):
    return _corrupted.get(s, s)

# --- Реализация метода двойственного симплекс-метода ---
def solve_dual_simplex(c, A, b):
    A = np.array(A, float)
    c = np.array(c, float)
    b = np.array(b, float)

    # Формирование двойственной системы
    A_dual, b_dual, c_dual = A.T, c, b
    nV, nC = A_dual.shape[1], A_dual.shape[0]
    var_n = [f"y{i+1}" for i in range(nV)]
    slack = [f"t{i+1}" for i in range(nC)]
    allv  = var_n + slack

    # Инициализация симплекс-таблицы
    T, base = [], []
    for i in range(nC):
        row = list(-A_dual[i]) + [1 if j == i else 0 for j in range(nC)] + [-b_dual[i]]
        T.append(row)
        base.append(slack[i])
    T.append(list(c_dual) + [0] * nC + [0])

    # Сохранение стартового шага
    steps = [{
        "title": "Начальная таблица",
        "table": [[base[i]] + T[i] for i in range(nC)] + [["W"] + T[-1]],
        "explanation": "Начальная симплекс-таблица"
    }]

    # Итеративный процесс двойственного симплекс-метода
    while True:
        rhs = [r[-1] for r in T[:-1]]
        if all(r >= 0 for r in rhs):
            break
        leave = int(np.argmin(rhs))
        row   = T[leave]
        ratios = [(T[-1][j] / abs(row[j]), j) for j in range(len(row) - 1) if row[j] < 0]
        if not ratios:
            raise NoSolutionError("Нет допустимого решения.")
        _, enter = min(ratios)
        piv = row[enter]
        T[leave] = [v / piv for v in row]
        base[leave] = allv[enter]
        for i in range(len(T)):
            if i != leave:
                factor = T[i][enter]
                T[i] = [T[i][j] - factor * T[leave][j] for j in range(len(row))]
        steps.append({
            "title": "Итерация",
            "table": [[base[i]] + T[i] for i in range(nC)] + [["W"] + T[-1]],
            "explanation": f"Ведущий столбец: {allv[enter]}, строка: {base[leave]}"
        })

    # Извлечение решения
    res = {v: 0 for v in allv}
    for i, var in enumerate(base):
        res[var] = T[i][-1]
    return steps, res, T[-1][-1]

# --- Раздача статических JS-файлов ---
@route('/static/scripts/<fn>')
def serve_static(fn):
    return static_file(fn, root='static/scripts')

# --- Обработка POST-запроса для загрузки случайного примера и его решения ---
@route('/dual_lpp_example', method='POST')
def dual_lpp_example():
    if not os.path.exists(EXAMPLES_FILE):
        return "Файл примеров не найден."
    examples = json.load(open(EXAMPLES_FILE, encoding='utf-8-sig'))
    if not examples:
        return "Нет доступных примеров."

    inp = random.choice(examples)['input']
    c, A, b, signs = (
        inp['objective_coeffs'],
        inp['constraint_coeffs'],
        inp['rhs_values'],
        inp['constraint_signs']
    )

    try:
        # Решение задачи
        steps, vals, W = solve_dual_simplex(c, A, b)
        answer_vars   = {k: round(v, 2) for k, v in vals.items() if k.startswith('y')}
        F             = round(-W, 2)
        duality_check = "Все условия двойственности выполняются."
        num_vars, num_cons = len(c), len(A)

        # Формирование таблицы вывода
        result_table = [['Базис'] + [f'y{i+1}' for i in range(num_cons)] + ['Св.член']]
        last = steps[-1]['table']
        for row in last[:-1]:
            result_table.append([row[0]] + [round(x, 2) for x in row[1:]])
        result_table.append(['W'] + [round(x, 2) for x in last[-1][1:]])

        # Составление текстового представления задач
        x_vars = [f'x{i+1}' for i in range(num_vars)]
        y_vars = [f'y{i+1}' for i in range(num_cons)]
        primal_obj        = f"Z = {format_expression(c, x_vars)}"
        primal_constraints= [format_expression(A[i], x_vars, b[i], '≤') for i in range(num_cons)]
        A_dual            = np.array(A).T.tolist()
        dual_obj          = f"W = {format_expression(b, y_vars)}"
        dual_constraints  = [format_expression(A_dual[i], y_vars, c[i], '≥') for i in range(num_vars)]

        # Сохранение результата в историю
        save_result_to_json({
            "timestamp": datetime.datetime.now().isoformat(),
            "input": inp,
            "output": {
                "dual_variables": answer_vars,
                "dual_objective_value": F
            }
        })

        # Подготовка данных для заполнения формы
        form_data = {
            'x':     [format_num(v) for v in c],
            'cons':  [[format_num(v) for v in row] for row in A],
            'signs': signs,
            'rhs':   [format_num(v) for v in b]
        }

        # Рендеринг шаблона с заполненной формой и решением
        return template('dual_lpp_practice.tpl',
                        title='Двойственная ЗЛП', year=2025,
                        num_vars=num_vars, num_cons=num_cons,
                        result_table=result_table, dual_steps=steps,
                        answer_vars=answer_vars, F=F, duality_check=duality_check,
                        primal_obj=primal_obj, primal_constraints=primal_constraints,
                        dual_obj=dual_obj, dual_constraints=dual_constraints,
                        no_solution=False, error_message='',
                        form_data=form_data)

    except Exception as e:
        # Сохранение ошибки и введённых данных в историю
        save_result_to_json({
            "timestamp": datetime.datetime.now().isoformat(),
            "input": {
                "objective_coeffs": inp.get('objective_coeffs', []),
                "constraint_coeffs": inp.get('constraint_coeffs', []),
                "rhs_values": inp.get('rhs_values', []),
                "constraint_signs": inp.get('constraint_signs', [])
            },
            "error": str(e)
        })
        # Подготовка form_data для повторного отображения
        form_data = {
            'x':     [format_num(v) for v in c],
            'cons':  [[format_num(v) for v in row] for row in A],
            'signs': signs,
            'rhs':   [format_num(v) for v in b]
        }
        # Рендеринг шаблона с сообщением об ошибке
        return template('dual_lpp_practice.tpl',
                        title='Двойственная ЗЛП', year=2025,
                        num_vars=len(c), num_cons=len(A),
                        result_table=None, dual_steps=None,
                        answer_vars={}, F=None, duality_check='',
                        primal_obj='', primal_constraints=[],
                        dual_obj='', dual_constraints=[],
                        no_solution=True, error_message=str(e),
                        form_data=form_data)

# --- Основной маршрут: отображение формы и её обработка ---
@route('/dual_lpp_practice', method=['GET','POST'])
def dual_lpp_practice():
    if request.method == 'GET':
        # Вывод пустой формы по умолчанию
        return template('dual_lpp_practice.tpl',
                        title='Двойственная ЗЛП', year=2025,
                        num_vars=2, num_cons=1,
                        result_table=None, dual_steps=None,
                        answer_vars={}, F=None, duality_check='',
                        primal_obj='', primal_constraints=[],
                        dual_obj='', dual_constraints=[],
                        no_solution=False, error_message='',
                        form_data={'x':[], 'cons':[], 'signs':[], 'rhs':[]})

    # Сбор данных из формы при POST
    num_vars = int(request.forms.get('num_vars', '2'))
    num_cons = int(request.forms.get('num_cons', '1'))
    raw_c    = [request.forms.get(f'x_{j}', '') for j in range(num_vars)]
    A_raw    = [[request.forms.get(f'cons_{i}_{j}', '') for j in range(num_vars)]
                for i in range(num_cons)]
    signs    = [clean_sign(request.forms.get(f'cons_sign_{i}', '≤')) for i in range(num_cons)]
    raw_b    = [request.forms.get(f'cons_rhs_{i}', '') for i in range(num_cons)]

    try:
        # Проверка непустоты целевой функции
        if not any(cell.strip() for cell in raw_c):
            raise Exception("Целевая функция не может быть пустой.")
        # Преобразование строк к float
        c = [float(v.replace(',', '.')) for v in raw_c]
        # Проверка того, что не все коэффициенты нулевые
        if all(coef == 0 for coef in c):
            raise Exception("Коэффициенты функции не могут быть все нулями.")
        # Проверка непустоты ограничений
        for i, row in enumerate(A_raw):
            if not any(cell.strip() for cell in row):
                raise Exception(f"Ограничение {i+1} пустое.")
        A = [[float(v.replace(',', '.')) for v in row] for row in A_raw]
        b = [float(v.replace(',', '.')) for v in raw_b]

        # Подготовка form_data для повторного вывода
        form_data = {
            'x':     [format_num(v) for v in c],
            'cons':  [[format_num(v) for v in row] for row in A],
            'signs': signs,
            'rhs':   [format_num(v) for v in b]
        }

        # Решение задачи
        steps, vals, W = solve_dual_simplex(c, A, b)
        answer_vars   = {k: round(v,2) for k, v in vals.items() if k.startswith('y')}
        F             = round(-W,2)
        duality_check = "Все условия двойственности выполняются."

        # Формирование таблицы результатов
        result_table = [['Базис'] + [f'y{i+1}' for i in range(num_cons)] + ['Св.член']]
        last = steps[-1]['table']
        for row in last[:-1]:
            result_table.append([row[0]] + [round(x,2) for x in row[1:]])
        result_table.append(['W'] + [round(x,2) for x in last[-1][1:]])

        # Построение текстовых представлений
        x_vars = [f'x{i+1}' for i in range(num_vars)]
        y_vars = [f'y{i+1}' for i in range(num_cons)]
        primal_obj = f"Z = {format_expression(c, x_vars)}"
        primal_constraints = [format_expression(A[i], x_vars, b[i], '≤') for i in range(num_cons)]
        A_dual = np.array(A).T.tolist()
        dual_obj = f"W = {format_expression(b, y_vars)}"
        dual_constraints = [format_expression(A_dual[i], y_vars, c[i], '≥') for i in range(num_vars)]

        # Сохранение результата решения
        save_result_to_json({
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
        })

        # Рендеринг шаблона с результатом
        return template('dual_lpp_practice.tpl',
                        title='Двойственная ЗЛП', year=2025,
                        num_vars=num_vars, num_cons=num_cons,
                        result_table=result_table, dual_steps=steps,
                        answer_vars=answer_vars, F=F, duality_check=duality_check,
                        primal_obj=primal_obj, primal_constraints=primal_constraints,
                        dual_obj=dual_obj, dual_constraints=dual_constraints,
                        no_solution=False, error_message='',
                        form_data=form_data)

    except Exception as e:
        # Сохранение ошибки и введённых данных в историю
        save_result_to_json({
            "timestamp": datetime.datetime.now().isoformat(),
            "input": {
                "objective_coeffs": raw_c,
                "constraint_coeffs": A_raw,
                "rhs_values": raw_b,
                "constraint_signs": signs
            },
            "error": str(e)
        })
        # Отображение ошибки с возвратом введённых данных
        form_data = {
            'x':     raw_c,
            'cons':  A_raw,
            'signs': signs,
            'rhs':   raw_b
        }
        return template('dual_lpp_practice.tpl',
                        title='Двойственная ЗЛП', year=2025,
                        num_vars=num_vars, num_cons=num_cons,
                        result_table=None, dual_steps=None,
                        answer_vars={}, F=None, duality_check='',
                        primal_obj='', primal_constraints=[],
                        dual_obj='', dual_constraints=[],
                        no_solution=True, error_message=str(e),
                        form_data=form_data)
