from bottle import route, view, request, template, redirect
from datetime import datetime
from typing import List, Optional
from hungarian_solver import solve_assignment  
from transport_solver import optimize_transportation
import json
import random
import os
import numpy as np

@route('/transport_practice', method=['GET', 'POST'])
@view('transport_practice')
def transport_practice():
    """
    Обрабатывается запрос к странице транспортной задачи.
    Поддерживаются GET и POST запросы для отображения формы и обработки данных.
    После успешного решения записываются данные в transport_results.json.
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

    # Обработка GET-запроса с параметрами от примера
    if request.method == 'GET':
        try:
            rows = int(request.query.get('rows', 3))
            cols = int(request.query.get('cols', 4))
            cost_matrix_json = request.query.get('cost_matrix_json', 'null')
            supply_json = request.query.get('supply_json', 'null')
            demand_json = request.query.get('demand_json', 'null')
            
            if cost_matrix_json != 'null':
                cost_matrix = json.loads(cost_matrix_json)
            if supply_json != 'null':
                supply = json.loads(supply_json)
            if demand_json != 'null':
                demand = json.loads(demand_json)
            error = request.query.get('error', '')
        except (ValueError, json.JSONDecodeError) as e:
            error = f"Ошибка загрузки примера: {str(e)}"
            rows = 3
            cols = 4

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
            rows = request.forms.get('rows')
            cols = request.forms.get('cols')
            if not rows or not cols:
                raise ValueError("Укажите количество поставщиков и потребителей.")
            rows = int(rows)
            cols = int(cols)
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
                    try:
                        val = float(value)
                        if val < 0:
                            raise ValueError("Значения матрицы тарифов должны быть неотрицательными.")
                        row.append(val)
                    except (ValueError, TypeError):
                        raise ValueError(f"Некорректное значение в матрице тарифов на позиции ({i+1}, {j+1}).")
                cost_matrix.append(row)

            # Проверяется заполнение запасов
            for i in range(rows):
                value = request.forms.get(f'supply-{i}')
                if value is None or value.strip() == '':
                    raise ValueError("Все поля запасов должны быть заполнены числами.")
                try:
                    val = float(value)
                    if val < 0:
                        raise ValueError("Значения запасов должны быть неотрицательными.")
                    supply.append(val)
                except (ValueError, TypeError):
                    raise ValueError(f"Некорректное значение в запасах на позиции {i+1}.")

            # Проверяется заполнение потребностей
            for j in range(cols):
                value = request.forms.get(f'demand-{j}')
                if value is None or value.strip() == '':
                    raise ValueError("Все поля потребностей должны быть заполнены числами.")
                try:
                    val = float(value)
                    if val < 0:
                        raise ValueError("Значения потребностей должны быть неотрицательными.")
                    demand.append(val)
                except (ValueError, TypeError):
                    raise ValueError(f"Некорректное значение в потребностях на позиции {j+1}.")

            # Проверяется, что не все запасы или потребности равны нулю
            if all(s == 0 for s in supply) or all(d == 0 for d in demand):
                raise ValueError("Запасы и потребности не могут быть одновременно равны нулю.")

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
                # После успешного решения записываются данные в файл
                if result is not None and total_cost is not None:
                    # Формируется запись
                    record = {
                        "timestamp": datetime.now().isoformat(),
                        "input_data": {
                            "rows": rows,
                            "cols": cols,
                            "cost_matrix": cost_matrix,
                            "supply": supply,
                            "demand": demand
                        },
                        "result": result,
                        "total_cost": total_cost
                    }
                    
                    # Путь к файлу transport_results.json
                    results_file = os.path.join('results', 'transport_results.json')
                    
                    # Чтение текущих данных или создание пустого списка
                    try:
                        if os.path.exists(results_file):
                            with open(results_file, 'r', encoding='utf-8') as f:
                                results = json.load(f)
                        else:
                            results = []
                    except (json.JSONDecodeError, IOError):
                        results = []
                    
                    # Добавление новой записи
                    results.append(record)
                    
                    # Запись обновленного списка в файл
                    try:
                        with open(results_file, 'w', encoding='utf-8') as f:
                            json.dump(results, f, ensure_ascii=False, indent=4)
                    except IOError as e:
                        error = f"Ошибка записи результатов в файл: {str(e)}"

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

@route('/transport_practice_example', method='POST')
def transport_practice_example():
    """
    Обрабатывается запрос на загрузку случайного примера из transport_output.json.
    Выбирается случайный пример и перенаправляется на страницу транспортной задачи с данными.
    """
    # Путь к файлу с примерами (в папке output)
    examples_file = os.path.join('examples', 'transport_example.json')
    
    try:
        # Чтение файла JSON
        with open(examples_file, 'r', encoding='utf-8') as f:
            examples = json.load(f)
        
        # Проверка, что файл не пустой
        if not examples:
            return redirect('/transport_practice?error=Файл с примерами пуст.')
        
        # Выбор случайного примера
        example = random.choice(examples)
        
        # Подготовка данных для перенаправления
        rows = example['rows']
        cols = example['cols']
        cost_matrix = example['cost_matrix']
        supply = example['supply']
        demand = example['demand']
        
        # Преобразование в JSON для передачи через параметры запроса
        cost_matrix_json = json.dumps(cost_matrix)
        supply_json = json.dumps(supply)
        demand_json = json.dumps(demand)
        
        # Перенаправление на страницу с данными примера
        return redirect(f'/transport_practice?rows={rows}&cols={cols}&cost_matrix_json={cost_matrix_json}&supply_json={supply_json}&demand_json={demand_json}')
    
    except FileNotFoundError:
        return redirect('/transport_practice?error=Файл transport_output.json не найден в папке output.')
    except json.JSONDecodeError:
        return redirect('/transport_practice?error=Ошибка декодирования JSON в файле transport_output.json.')
    except KeyError as e:
        return redirect(f'/transport_practice?error=Неверная структура файла transport_output.json (отсутствует ключ {e}).')
