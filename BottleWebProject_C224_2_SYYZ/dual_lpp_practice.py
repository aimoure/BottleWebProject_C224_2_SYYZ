from bottle import route, request, template, static_file
import numpy as np

class NoSolutionError(Exception):
    """Исключение для нерешаемой задачи."""
    pass

@route('/static/scripts/<filename>')
def serve_static(filename):
    return static_file(filename, root='static/scripts')

@route('/dual_lpp_practice', method=['GET', 'POST'])
def dual_lpp_practice():
    # общие переменные
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

    num_vars = request.forms.get('num_vars', '2')
    num_cons = request.forms.get('num_cons', '1')

    if request.method == 'POST':
        try:
            num_vars = int(num_vars)
            num_cons = int(num_cons)

            # считываем коэффициенты цели
            c = [float(request.forms.get(f'x_{j}', '0') or '0') for j in range(num_vars)]
            # считываем матрицу ограничений
            A = []
            b = []
            for i in range(num_cons):
                row = [float(request.forms.get(f'cons_{i}_{j}', '0') or '0') for j in range(num_vars)]
                A.append(row)
                b.append(float(request.forms.get(f'cons_rhs_{i}', '0') or '0'))

            # решаем двойственным симплексом
            steps, result_values, W = solve_dual_simplex(c, A, b)

            # разбираем решение
            answer_vars = {k: v for k, v in result_values.items() if k.startswith('y')}
            F = -W
            duality_check = "Все условия двойственности выполняются."

            # форматируем вывод таблицы
            result_table.append(['Базис'] + [f'y{i+1}' for i in range(len(answer_vars))] + ['Св.член'])
            last_table = steps[-1]['table']
            for row in last_table[:-1]:
                result_table.append([row[0]] + [round(x, 2) for x in row[1:]])
            result_table.append(['W'] + [round(x, 2) for x in last_table[-1][1:]])

            # формируем текстовые задачи
            x_vars = [f'x{i+1}' for i in range(num_vars)]
            y_vars = [f'y{i+1}' for i in range(num_cons)]
            primal_obj = f"Z = {format_expression(c, x_vars)}"
            primal_constraints = [format_expression(A[i], x_vars, b[i], '≤') for i in range(num_cons)]
            A_dual = np.array(A).T.tolist()
            dual_obj = f"W = {format_expression(b, y_vars)}"
            dual_constraints = [format_expression(A_dual[i], y_vars, c[i], '≥') for i in range(num_vars)]

        except NoSolutionError as ne:
            no_solution = True
            error_message = str(ne)
        except Exception as e:
            no_solution = True
            error_message = f"Ошибка: {e}"

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
                    error_message=error_message)


def solve_dual_simplex(c, A, b):
    A = np.array(A, dtype=float)
    c = np.array(c, dtype=float)
    b = np.array(b, dtype=float)

    A_dual = A.T
    b_dual = c
    c_dual = b

    num_vars = A_dual.shape[1]
    num_cons = A_dual.shape[0]

    var_names = [f"y{i+1}" for i in range(num_vars)]
    slack_names = [f"t{i+1}" for i in range(num_cons)]
    all_vars = var_names + slack_names

    tableau = []
    basis = []
    for i in range(num_cons):
        row = list(-A_dual[i])
        slack = [1 if j == i else 0 for j in range(num_cons)]
        row += slack
        row.append(-b_dual[i])
        tableau.append(row)
        basis.append(slack_names[i])

    z_row = list(c_dual) + [0]*num_cons + [0]
    tableau.append(z_row)

    steps = [{
        "title": "Начальная таблица",
        "table": [[basis[i]] + tableau[i] for i in range(num_cons)] + [["W"] + tableau[-1]],
        "explanation": "Начальная симплекс-таблица"
    }]

    while True:
        rhs = [row[-1] for row in tableau[:-1]]
        if all(r >= 0 for r in rhs):
            break

        leaving = int(np.argmin(rhs))
        row = tableau[leaving]

        ratios = []
        for j in range(len(row)-1):
            coeff = row[j]
            zjcj = tableau[-1][j]
            if coeff < 0:
                ratios.append((zjcj / abs(coeff), j))
        if not ratios:
            raise NoSolutionError("Задача не имеет допустимого решения.")

        _, entering = min(ratios)
        pivot = tableau[leaving][entering]
        tableau[leaving] = [v / pivot for v in tableau[leaving]]
        basis[leaving] = all_vars[entering]

        for i in range(len(tableau)):
            if i != leaving:
                factor = tableau[i][entering]
                tableau[i] = [
                    tableau[i][j] - factor * tableau[leaving][j]
                    for j in range(len(tableau[i]))
                ]

        steps.append({
            "title": "Итерация",
            "table": [[basis[i]] + tableau[i] for i in range(num_cons)] + [["W"] + tableau[-1]],
            "explanation": f"Ведущий столбец: {all_vars[entering]}, ведущая строка: {basis[leaving]}"
        })

    result_values = {name: 0 for name in all_vars}
    for i, var in enumerate(basis):
        result_values[var] = tableau[i][-1]
    W = tableau[-1][-1]

    return steps, result_values, W


def format_term(coef, var):
    if coef == 0: return ''
    coef_int = int(coef)
    if coef == 1: return var
    if coef == -1: return f"-{var}"
    return f"{coef_int if coef==coef_int else coef}{var}"

def format_expression(coeffs, vars_list, rhs=None, sign=None):
    terms = [format_term(c, v) for c, v in zip(coeffs, vars_list)]
    expr = ' + '.join(filter(None, terms)).replace('+ -', '- ')
    if sign and rhs is not None:
        rhs_int = int(rhs)
        rhs_str = str(rhs_int if rhs==rhs_int else rhs)
        return f"{expr} {sign} {rhs_str}"
    return expr
