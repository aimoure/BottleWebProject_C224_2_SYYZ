import json
import random
from typing import List
from bottle import route, request, view
from datetime import datetime
from direct_lpp import LinearProgrammingProblem

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

# Маршрут для прямой задачи ЛП
@route('/hungarian-calc', method=['GET','POST'])
@view('direct_lpp_practice') # Единый шаблон и для GET, и для POST
def hungarian_calc():
    # Инициализация базового контекста для шаблона
    ctx = base_context()
    ctx['initial_data_json'] = None
    # При GET-запросе возвращается только базовый контекст, страница отрисовывается пустой формой
    if request.method == 'GET':
        return ctx

    action = request.forms.get('action', 'solve') # Получение типа действия (какая кнопка нажата)

    if action == 'load_example':
        try:
            # Путь к файлу с примерами
            examples_file = 'examples/direct_lpp_examples.json'
            with open(examples_file, 'r', encoding='utf-8-sig') as f:
                examples = json.load(f)
            example = random.choice(examples)

            # Распаковка полей
            objective = example['objective']
            constraints = example['constraints']
            signs = example['signs']
            rhs = example['rhs']

            # Создание задачи
            lp = LinearProgrammingProblem(objective, constraints, signs, rhs)
            # Решение задачи
            result = lp.solve()
            # Сохранение в файл
            lp.save_to_json('results/direct_lpp_results.json')

            # Собираем initial_data для JS
            init_data = {
                "numVars": len(objective),
                "numCons": len(constraints),
                "vars": { f"x_{j}": objective[j] for j in range(len(objective)) },
                "consVars": {
                    f"cons_{i}_{j}": constraints[i][j]
                    for i in range(len(constraints))
                    for j in range(len(objective))
                },
                "consSigns": { f"cons_sign_{i}": signs[i] for i in range(len(signs)) },
                "consRhs": { f"cons_rhs_{i}": rhs[i] for i in range(len(rhs)) }
            }
            # Преобразуем в JSON и кладём в контекст
            ctx['initial_data_json'] = json.dumps(init_data, ensure_ascii=False)

            if result is None: # Если решения нет — в контекст заносится соответствующее сообщение
                ctx['error'] = "Пример загружен, но решения нет."
            else:
                ctx['x_values'] = result['x']
                ctx['objective_value'] = result['objective_value']
                ctx['json_saved'] = True
            return ctx

        except Exception as e:
            ctx['error'] = f"Не удалось загрузить пример: {e}"
            return ctx
    else:
        # Сбор данных из формы
        n_vars = int(request.forms.get('number_of_variables', 2)) # Получение количества переменных из формы
        n_cons = int(request.forms.get('number_of_constraints', 1)) # Получение количества ограничений из формы

        # Сбор списка пустых полей
        missing = []
        # Целевая функция
        for j in range(n_vars):
            if request.forms.get(f'x_{j}', '').strip() == '':
                missing.append(f'x_{j}')
        # Коэффициенты ограничений и правые части
        for i in range(n_cons):
            # Коэффициенты
            for j in range(n_vars):
                if request.forms.get(f'cons_{i}_{j}', '').strip() == '':
                    missing.append(f'cons_{i}_{j}')
            # Правая часть
            if request.forms.get(f'cons_rhs_{i}', '').strip() == '':
                missing.append(f'cons_rhs_{i}')
        if missing:
            # Формировка единый текст ошибки
            ctx['error'] = "Заполните все поля формы."
            return ctx

        # Коэффициенты целевой функции
        objective: List[float] = []
        # Перебираются пустой список для коэффициентов целевой функции
        for j in range(n_vars):
            raw = request.forms.get(f'x_{j}', '').strip() # Получение значения переменной из формы
            try:
                objective.append(float(raw)) # Значение добавляется в список objective
            except ValueError:
                objective.append(0.0) # В случае ошибки преобразования добавление 0.0

        # Проверка на нулевые коэффициенты в целевой функции
        if any(coef == 0 for coef in objective):
            ctx['error'] = "Целевая функция содержит нулевые коэффициенты."
            return ctx

        # Коэффициенты ограничений
        constraints: List[List[float]] = []
        # Перебираются пустой список для коэффициентов ограничений
        for i in range(n_cons):
            row: List[float] = []
            for j in range(n_vars):
                raw = request.forms.get(f'cons_{i}_{j}', '').strip() # Получается значение из формы для соответствующей переменной и ограничения
                try:
                    row.append(float(raw)) # Добавление в текущую строку
                except ValueError:
                    row.append(0.0) # В случае ошибки — добавление 0.0
            # Проверка: если все коэффициенты в строке ограничения нулевые
            if all(coef == 0 for coef in row):
                ctx['error'] = f"Все коэффициенты ограничения №{i+1} равны нулю."
                return ctx
            constraints.append(row) # Строка ограничений добавляется в общий список
    
        # Получение знака ограничения, по умолчанию — '?', добавление в список
        signs: List[str] = []
        for i in range(n_cons):
            signs.append(request.forms.get(f'cons_sign_{i}', '?')) 

        # Получение значения правой части из формы
        rhs: List[float] = []
        for i in range(n_cons):
            raw = request.forms.get(f'cons_rhs_{i}', '').strip()
            try:
                rhs.append(float(raw)) # Добавление в текущую строку
            except ValueError:
                rhs.append(0.0) # В случае ошибки — добавление 0.0

        # Создание и решение задачи
        try:
            # Создаётся экземпляр задачи линейного программирования с собранными данными
            lp = LinearProgrammingProblem(objective, constraints, signs, rhs)
            result = lp.solve() # Поиск решения с помощью функции solve()
        except Exception as e:  # В случае любой ошибки результат ошибки помещается в контекст под ключом 'error'
            ctx['error'] = str(e)
            return ctx

        # Сохраняем в конец JSON-файла
        try:
            lp.save_to_json('results/direct_lpp_results.json')
            ctx['json_saved'] = True
        except Exception as e:
            # Отметка проблемы
            ctx['warning'] = f"Не удалось сохранить JSON: {e}"

        if result is None: # Если решения нет — в контекст заносится соответствующее сообщение
            ctx['error'] = "Нет допустимого решения."
        else:
            ctx['x_values'] = result['x']
            ctx['objective_value'] = result['objective_value']
        return ctx