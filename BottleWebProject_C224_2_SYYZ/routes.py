"""
Routes and views for the bottle application.
"""

from bottle import route, view, request, template, redirect
from datetime import datetime
from direct_lpp import LinearProgrammingProblem
from typing import List, Optional
from hungarian_solver import solve_assignment  
import json

# Общая вспомогательная функция: базовые данные для шаблона
def base_context():
    return {
        'title': 'Калькулятор прямой ЗЛП',
        'year': datetime.now().year,
        'error': '',
        'x_values': None,
        'objective_value': None,
        'status': None,
    }

@route('/')
@route('/home')
@view('index')
def home():
    """Renders the home page."""
    return dict(
        year=datetime.now().year
    )

@route('/transport_theory')
@view('transport_theory')
def dual_theory():
    """Renders the transport_theory page."""
    return dict(
        title='The transport programming problem',
        year=datetime.now().year
    )

@route('/transport_practice')
@view('transport_practice')
def dual_theory():
    """Renders the transport_practice page."""
    return dict(
        title='The transport programming problem',
        year=datetime.now().year
    )

@route('/purpose_theory')
@view('purpose_theory')
def direct_lpp_practice():
    """Renders the purpose_theory page."""
    return dict(
        title='The assignment problem',
        year=datetime.now().year
    )

@route('/purpose_practice')
@view('purpose_practice')
def direct_lpp_practice():
    """Renders the purpose_theory page."""
    return dict(
        title='The assignment problem',
        year=datetime.now().year
    )

@route('/direct_lpp_theory')
@view('direct_lpp_theory')
def direct_lpp_theory():
    """Renders the direct_lpp_theory page."""
    return dict(
        title='The direct linear programming program',
        year=datetime.now().year
    )

@route('/direct_lpp_practice')
@view('direct_lpp_practice')
def direct_lpp_practice():
    """Renders the direct_lpp_practice page."""
    return dict(
        title='The direct linear programming program',
        year=datetime.now().year
    )

@route('/dual_lpp_theory')
@view('dual_lpp_theory')
def dual_theory():
    """Renders the dual_theory page."""
    return dict(
        title='The dual linear programming problem',
        year=datetime.now().year
    )

@route('/dual_lpp_practice')
@view('dual_lpp_practice')
def direct_lpp_practice():
    """Renders the direct_lpp_practice page."""
    return dict(
        title='The dual linear programming program',
        year=datetime.now().year
    )

@route('/about')
@view('about')
def about():
    """Renders the about page."""
    return dict(
        title='About',
        year=datetime.now().year
    )

# Маршрут для прямой задачи ЛП
@route('/hungarian-calc', method=['GET','POST'])
@view('direct_lpp_practice') # Единый шаблон и для GET, и для POST
def hungarian_calc():
    ctx = base_context()
    if request.method == 'GET':
        return ctx

    # Сбор данных из формы
    n_vars = int(request.forms.get('number_of_variables', 2))
    objective: List[float] = []
    for j in range(n_vars):
        raw = request.forms.get(f'x_{j}', '').strip()
        try:
            objective.append(float(raw))
        except ValueError:
            objective.append(0.0)

    n_cons = int(request.forms.get('number_of_constraints', 1))
    constraints: List[List[float]] = []
    for i in range(n_cons):
        row: List[float] = []
        for j in range(n_vars):
            raw = request.forms.get(f'cons_{i}_{j}', '').strip()
            try:
                row.append(float(raw))
            except ValueError:
                row.append(0.0)
        constraints.append(row)

    signs: List[str] = []
    for i in range(n_cons):
        signs.append(request.forms.get(f'cons_sign_{i}', '≤'))

    rhs: List[float] = []
    for i in range(n_cons):
        raw = request.forms.get(f'cons_rhs_{i}', '').strip()
        try:
            rhs.append(float(raw))
        except ValueError:
            rhs.append(0.0)

    # Создание и решение задачи
    try:
        lp = LinearProgrammingProblem(
            objective=objective,
            constraints=constraints,
            signs=signs,
            rhs=rhs
        )
        result = lp.solve()
    except Exception as e:
        ctx['error'] = str(e)
        return ctx

    if result is None:
        # Нет допустимого решения
        ctx['error'] = "Нет допустимого решения."
        return ctx

    # Успешный результат – добавление в контекст для шаблона
    ctx.update({
        'x_values': result['x'],
        'objective_value': result['objective_value'],
    })
    return ctx

@route('/purpose_practice', method=['GET', 'POST'])
@view('purpose_practice')
def purpose_practice():
    result = None
    matrix = None
    error = None
    task_labels = []
    worker_labels = []

    if request.method == 'POST':
        try:
            size = int(request.forms.get('size'))
            task_labels = [request.forms.get(f'label-x{j}', f'Task {j+1}') for j in range(size)]
            worker_labels = [request.forms.get(f'label-y{i}', f'Worker {i+1}') for i in range(size)]

            matrix = []
            for i in range(size):
                row = []
                for j in range(size):
                    val = request.forms.get(f'matrix-{i}-{j}')
                    row.append(int(val))
                matrix.append(row)

            result = solve_assignment(matrix)

        except Exception as e:
            error = str(e)

    return dict(
        title="The assignment problem",
        year=datetime.now().year,
        result=result,
        matrix=matrix,
        error=error,
        task_labels=task_labels,
        worker_labels=worker_labels
    )

    # Возврат результата
    return template('direct_lpp_result',
                    x_values=result['x'],
                    objective_value=result['objective_value'],
                    status=result['status'])