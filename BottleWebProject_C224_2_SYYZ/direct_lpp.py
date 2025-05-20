from dataclasses import dataclass, field
from typing import List, Optional
import numpy as np
from scipy.optimize import linprog
import json
from datetime import datetime
from json import JSONDecodeError

@dataclass
class LinearProgrammingProblem:
    objective: List[float] = field(default_factory=list) # Коэффициенты целевой функции (массив чисел)
    constraints: List[List[float]] = field(default_factory=list) # Коэффициенты ограничений (двумерный массив)
    signs: List[str] = field(default_factory=list)  # Знаки ограничений: каждый элемент — одна из строк '?', '=', '?'
    rhs: List[float] = field(default_factory=list) # Свободные члены ограничений (массив чисел)

    corrupted_sign_map = {
        'â\u0089¤': '≤',
        'â\u0089¥': '≥'
        }

    # Инициализация
    def __post_init__(self):
        # Простая валидация на согласованность размеров
        n_vars = len(self.objective)
        n_cons = len(self.rhs)
        try:
            self.objective = [float(x) for x in self.objective]
            self.rhs = [float(x) for x in self.rhs]
            self.constraints = [[float(x) for x in row] for row in self.constraints]
        except (ValueError, TypeError) as e:
            raise ValueError("Все коэффициенты и свободные члены должны быть числовыми") from e
        if len(self.constraints) != n_cons:
            raise ValueError(f"Ожидалось {n_cons} строк в constraints, получено {len(self.constraints)}")
        if len(self.signs) != n_cons:
            raise ValueError(f"Ожидалось {n_cons} знаков, получено {len(self.signs)}")
        for i, row in enumerate(self.constraints):
            if len(row) != n_vars:
                raise ValueError(f"В ограничении {i} ожидается {n_vars} коэффициентов, получено {len(row)}")

    # Добавление нового ограничения
    def add_constraint(self, coeffs: List[float], sign: str, b: float):
        if len(coeffs) != len(self.objective):
            raise ValueError("Длина coeffs должна совпадать с количеством переменных")
        if sign not in ('≤', '=', '≥'):
            raise ValueError("Sign должен быть одним из '≤', '=', '≥'")
        self.constraints.append(coeffs)
        self.signs.append(sign)
        self.rhs.append(b)

    def __repr__(self):
        return (
            f"LinearProgrammingProblem(objective={self.objective}, optimize={self.optimize!r},\n"
            f"                         constraints={self.constraints},\n"
            f"                         signs={self.signs}, rhs={self.rhs})"
        )

    def solve(self) -> Optional[dict]:
        # Подготовка коэффициентов для linprog
        c = -np.array(self.objective, dtype=float)

        # A_ub и b_ub — для всех ограничений вида ai x ≤ bi
        # A_eq и b_eq — для всех ограничений вида ai x = bi
        A_ub, b_ub, A_eq, b_eq = [], [], [], []
        # Разбираем каждое ограничение в нужный массив
        for row, sign, b in zip(self.constraints, self.signs, self.rhs):
            if sign == '≤':
                A_ub.append(row)
                b_ub.append(b)
            # ax >= b  <=>  -ax <= -b
            elif sign == '≥':
                A_ub.append([-a for a in row])
                b_ub.append(-b)
             # sign == '='
            else:
                A_eq.append(row)
                b_eq.append(b)

        # Преобразуем в numpy-массивы или None
        A_ub = np.array(A_ub, dtype=float) if A_ub else None
        b_ub = np.array(b_ub, dtype=float) if b_ub else None
        A_eq = np.array(A_eq, dtype=float) if A_eq else None
        b_eq = np.array(b_eq, dtype=float) if b_eq else None

        # Сам вызов linprog
        res = linprog(c,
                      A_ub=A_ub, b_ub=b_ub,
                      A_eq=A_eq, b_eq=b_eq,
                      method='highs')
        if not res.success:
            # Нет решения или не найдено
            return None

        # Собираем ответ
        x = [round(val, 2) for val in res.x.tolist()]
        value = round(-res.fun, 2)

        return {
            'x': x, # Список значений переменных
            'objective_value': value, # Значение функции
        }
    
    def save_to_json(self, filepath: str) -> None:
        # Костыль для восстановления корректных символов знаков
        corrupted_sign_map = {
            'â\u0089¤': '≤',
            'â\u0089¥': '≥'
        }
        clean_signs = [corrupted_sign_map.get(s, s) for s in self.signs]

        new_entry = {
            "input": {
                "x": self.objective,
                "coefficients_of_constraints": self.constraints,
                "signs": clean_signs,
                "b": self.rhs
            },
            "output": self._make_output_block()
        }

        # Чтение существующих данных
        try:
            with open(filepath, 'r', encoding='utf-8-sig') as f:
                data = json.load(f)
                # Если файл содержит не список — обёрнем его в список
                if not isinstance(data, list):
                    data = [data]
        except (FileNotFoundError, JSONDecodeError):
            data = []

        # Добавление новой записи
        data.append(new_entry)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    # Вспомогательный метод, собирающий блок output
    def _make_output_block(self) -> dict:
        try:
            result = self.solve()
            if result is None:
                return {
                    "time": datetime.now().isoformat(),
                    "x": [],
                    "Z": None,
                    "error": "Нет допустимого решения"
                }
            else:
                return {
                    "time": datetime.now().isoformat(),
                    "x": result["x"],
                    "Z": result["objective_value"],
                    "error": None
                }
        except Exception as e:
            return {
                "time": datetime.now().isoformat(),
                "x": [],
                "Z": None,
                "error": str(e)
            }