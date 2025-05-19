"""
Routes and views for the bottle application.
"""

from bottle import route, view, request, template
from datetime import datetime
from direct_lpp import LinearProgrammingProblem
from typing import List, Optional
from transport_solver import optimize_transportation
import json
import numpy as np


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
def hungarian_calc():
    if request.method == 'GET':
        return template('direct_lpp_practice')

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
        result: Optional[dict] = lp.solve()
    except Exception as e:
        return template('direct_lpp_practice', error=str(e))

    if result is None:
        return template('direct_lpp_practice', error="No feasible solution.")

    # Возврат результата
    return template('direct_lpp_result',
                    x_values=result['x'],
                    objective_value=result['objective_value'],
                    status=result['status'])

@route('/transport_practice', method=['GET', 'POST'])
@view('transport_practice')
def transport_practice():
    """
    Обрабатывается запрос к странице транспортной задачи.
    Поддерживаются GET и POST запросы для отображения формы и обработки данных.
    """
    # Инициализируются переменные по умолчанию
    rows = 3
    cols = 4
    result = None
    total_cost = None
    error = ''
    cost_matrix = None
    supply = None
    demand = None

    if request.method == 'POST':
        action = request.forms.get('action')
        if action == 'clear':
            # При очистке формы возвращаются значения по умолчанию
            return dict(
                title='The transport programming problem',
                year=datetime.now().year,
                rows=rows,
                cols=cols,
                result=None,
                total_cost=None,
                error='',
                cost_matrix_json='null',
                supply_json='null',
                demand_json='null'
            )

        try:
            # Получаются размеры матрицы из формы
            rows = int(request.forms.get('rows', 3))
            cols = int(request.forms.get('cols', 4))
            # Проверяются допустимые размеры
            if rows < 1 or cols < 1 or rows > 10 or cols > 10:
                raise ValueError("Размеры матрицы должны быть от 1 до 10.")

            # Инициализируются массивы для данных формы
            cost_matrix = []
            supply = []
            demand = []

            # Проверяется заполнение матрицы тарифов
            for i in range(rows):
                row = []
                for j in range(cols):
                    value = request.forms.get(f'matrix-{i}-{j}')
                    if value is None or value.strip() == '':
                        raise ValueError("Все поля матрицы тарифов должны быть заполнены числами.")
                    row.append(float(value))
                cost_matrix.append(row)

            # Проверяется заполнение запасов
            for i in range(rows):
                value = request.forms.get(f'supply-{i}')
                if value is None or value.strip() == '':
                    raise ValueError("Все поля запасов должны быть заполнены числами.")
                supply.append(float(value))

            # Проверяется заполнение потребностей
            for j in range(cols):
                value = request.forms.get(f'demand-{j}')
                if value is None or value.strip() == '':
                    raise ValueError("Все поля потребностей должны быть заполнены числами.")
                demand.append(float(value))

            # Проверяется неотрицательность всех значений
            if any(x < 0 for row in cost_matrix for x in row) or any(x < 0 for x in supply) or any(x < 0 for x in demand):
                raise ValueError("Все значения должны быть неотрицательными.")

            # Проверяется равенство суммы запасов и потребностей
            if abs(sum(supply) - sum(demand)) > 1e-10:
                error = "Сумма запасов не равна сумме потребностей."
            else:
                # Выполняется оптимизация транспортной задачи
                result, total_cost = optimize_transportation(
                    np.array(cost_matrix),
                    np.array(supply),
                    np.array(demand)
                )

        except ValueError as e:
            error = f"Ошибка: {str(e)}"
            result = None
            total_cost = None
            # Данные сохраняются даже при ошибке
            if cost_matrix is None:
                cost_matrix = [[0] * cols for _ in range(rows)]
            if supply is None:
                supply = [0] * rows
            if demand is None:
                demand = [0] * cols

    # Преобразуются данные в JSON для передачи в шаблон
    cost_matrix_json = json.dumps(cost_matrix) if cost_matrix else 'null'
    supply_json = json.dumps(supply) if supply else 'null'
    demand_json = json.dumps(demand) if demand else 'null'

    # Возвращается словарь с данными для шаблона
    return dict(
        title='The transport programming problem',
        year=datetime.now().year,
        rows=rows,
        cols=cols,
        result=result,
        total_cost=total_cost,
        error=error,
        cost_matrix_json=cost_matrix_json,
        supply_json=supply_json,
        demand_json=demand_json
    )