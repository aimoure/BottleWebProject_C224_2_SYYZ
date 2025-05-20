import numpy as np

def northwest_corner_method(cost_matrix, supply, demand):
    """
    Выполняется построение начального базисного плана методом северо-западного угла.
    
    Аргументы:
        cost_matrix: Матрица тарифов (стоимостей перевозок).
        supply: Массив запасов поставщиков.
        demand: Массив потребностей потребителей.
    
    Возвращается:
        plan: Матрица начального базисного плана перевозок.
    """
    # Копируются входные массивы для предотвращения изменения исходных данных
    supply = supply.copy()
    demand = demand.copy()
    # Определяются размеры матрицы: количество поставщиков и потребителей
    rows, cols = len(supply), len(demand)
    # Создается матрица плана, заполненная нулями
    plan = np.zeros((rows, cols))
    # Устанавливаются начальные индексы для перебора
    i = j = 0
    # Выполняется цикл, пока не обработаны все поставщики или потребители
    while i < rows and j < cols:
        # Пропускаются нулевые запасы или потребности
        while i < rows and supply[i] == 0:
            i += 1
        while j < cols and demand[j] == 0:
            j += 1
        if i >= rows or j >= cols:
            break
        # Находится минимальное значение между запасом и потребностью
        amount = min(supply[i], demand[j])
        # Значение записывается в план
        plan[i, j] = amount
        # Уменьшаются запас и потребность на использованное количество
        supply[i] -= amount
        demand[j] -= amount
        # Если запас исчерпан, индекс поставщика увеличивается
        if supply[i] == 0:
            i += 1
        # Если потребность удовлетворена, индекс потребителя увеличивается
        elif demand[j] == 0:
            j += 1
    return plan

def get_basis(plan):
    """
    Определяются базисные клетки плана (ненулевые значения).
    При необходимости добавляются дополнительные клетки для достижения требуемого числа базисных переменных.
    
    Аргументы:
        plan: Матрица плана перевозок.
    
    Возвращается:
        basis: Список кортежей (i, j) — координаты базисных клеток.
    """
    # Формируется список ненулевых клеток плана
    basis = [(i, j) for i in range(plan.shape[0]) for j in range(plan.shape[1]) if plan[i, j] > 0]
    # Проверяется, достаточно ли базисных клеток (m + n - 1)
    while len(basis) < plan.shape[0] + plan.shape[1] - 1:
        # Добавляется первая подходящая небазисная клетка
        for i in range(plan.shape[0]):
            for j in range(plan.shape[1]):
                if (i, j) not in basis and plan[i, j] >= 0:  # Учитываем нули как допустимые
                    basis.append((i, j))
                    return basis
    return basis

def calculate_potentials(cost_matrix, basis):
    """
    Вычисляются потенциалы u и v для базисных клеток методом потенциалов.
    
    Аргументы:
        cost_matrix: Матрица тарифов.
        basis: Список базисных клеток (i, j).
    
    Возвращается:
        u: Список потенциалов поставщиков.
        v: Список потенциалов потребителей.
    """
    # Инициализируются списки потенциалов значениями None
    u = [None] * cost_matrix.shape[0]
    v = [None] * cost_matrix.shape[1]
    # Устанавливается начальное значение u[0] = 0 для решения системы уравнений
    u[0] = 0
    # Выполняется цикл для вычисления всех потенциалов
    for _ in range(cost_matrix.shape[0] + cost_matrix.shape[1] - 1):  # Увеличен лимит для надежности
        for i, j in basis:
            if u[i] is not None and v[j] is None:
                v[j] = cost_matrix[i, j] - u[i]
            elif u[i] is None and v[j] is not None:
                u[i] = cost_matrix[i, j] - v[j]
    # Если остались None, заполняются нулями для нулевых строк/столбцов
    for i in range(len(u)):
        if u[i] is None:
            u[i] = 0
    for j in range(len(v)):
        if v[j] is None:
            v[j] = 0
    return u, v

def find_cycle(basis, start):
    """
    Выполняется поиск замкнутого цикла в базисе, начиная с указанной клетки.
    
    Аргументы:
        basis: Список базисных клеток (i, j).
        start: Начальная клетка (i, j) для поиска цикла.
    
    Возвращается:
        path: Список клеток, образующих замкнутый цикл, или None, если цикл не найден.
    """
    from collections import defaultdict, deque

    # Создается граф смежности для базисных клеток
    graph = defaultdict(list)
    for i, j in basis:
        for ii, jj in basis:
            if (i == ii or j == jj) and (i, j) != (ii, jj):
                graph[(i, j)].append((ii, jj))

    def dfs(path, visited):
        """
        Выполняется поиск цикла с помощью поиска в глубину.
        
        Аргументы:
            path: Текущий путь (список клеток).
            visited: Множество посещенных клеток.
        
        Возвращается:
            path: Замкнутый цикл или None, если цикл не найден.
        """
        node = path[-1]
        for neighbor in graph[node]:
            # Проверяется, образует ли сосед замкнутый цикл
            if neighbor == path[0] and len(path) >= 4 and len(path) % 2 == 0:
                return path
            # Если сосед не посещен, продолжается поиск
            if neighbor not in visited:
                result = dfs(path + [neighbor], visited | {neighbor})
                if result:
                    return result
        return None

    # Если цикл не найден, возвращается None с предупреждением
    cycle = dfs([start], {start})
    if not cycle:
        print("Предупреждение: Цикл не найден, возможно, данные не позволяют оптимизировать план.")
    return cycle

def optimize_transportation(cost_matrix, supply, demand):
    """
    Оптимизируется транспортная задача методом потенциалов.
    
    Аргументы:
        cost_matrix: Матрица тарифов.
        supply: Массив запасов поставщиков.
        demand: Массив потребностей потребителей.
    
    Возвращается:
        plan: Оптимизированный план перевозок (список).
        total_cost: Общая стоимость перевозок.
    """
    # Получается начальный базисный план
    plan = northwest_corner_method(cost_matrix, supply, demand)
    while True:
        # Определяются базисные клетки
        basis = get_basis(plan)
        # Вычисляются потенциалы
        u, v = calculate_potentials(cost_matrix, basis)

        # Создается матрица дельт для небазисных клеток
        deltas = np.full(cost_matrix.shape, None)
        for i in range(cost_matrix.shape[0]):
            for j in range(cost_matrix.shape[1]):
                if (i, j) not in basis:
                    # Проверяется, что u[i] и v[j] определены
                    if u[i] is not None and v[j] is not None:
                        deltas[i, j] = cost_matrix[i, j] - u[i] - v[j]

        # Находится минимальная дельта
        min_delta = np.min([x for x in deltas.flatten() if x is not None])
        # Если минимальная дельта неотрицательна, оптимизация завершена
        if min_delta >= 0 or min_delta is None:  # Добавлена проверка на None
            break

        # Находится клетка с минимальной дельтой
        i, j = np.argwhere(deltas == min_delta)[0]
        # Строится цикл, включающий новую клетку
        cycle = find_cycle(basis + [(i, j)], (i, j))
        if not cycle:
            print("Предупреждение: Не удалось построить цикл, план остается начальным.")
            break

        # Находится минимальное значение в цикле для корректировки плана
        min_val = float('inf')
        for k in range(1, len(cycle), 2):
            ci, cj = cycle[k]
            if plan[ci, cj] < min_val:
                min_val = plan[ci, cj]

        # Корректируется план по циклу
        for k, (ci, cj) in enumerate(cycle):
            if k % 2 == 0:
                plan[ci, cj] += min_val
            else:
                plan[ci, cj] -= min_val

        # Устраняются малые значения для численной стабильности
        plan = np.where(plan < 1e-10, 0, plan)

    # Вычисляется общая стоимость
    total_cost = np.sum(plan * cost_matrix)
    return plan.tolist(), total_cost