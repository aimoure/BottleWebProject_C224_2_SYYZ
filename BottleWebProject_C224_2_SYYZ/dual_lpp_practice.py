from bottle import route, run, template, request, static_file

@route('/static/scripts/<filename>')
def serve_static(filename):
    return static_file(filename, root='static/scripts')

@route('/dual_lpp_practice', method=['GET', 'POST'])
def dual_lpp_practice():
    result_table = None
    num_vars = request.forms.get('num_vars')
    num_cons = request.forms.get('num_cons')

    if request.method == 'POST':
        try:
            num_vars = int(num_vars)
            num_cons = int(num_cons)

            # Получение коэффициентов целевой функции
            c = [float(request.forms.get(f'x_{j}', 0)) for j in range(num_vars)]

            # Получение ограничений
            A = []
            b = []
            signs = []
            for i in range(num_cons):
                row = [float(request.forms.get(f'cons_{i}_{j}', 0)) for j in range(num_vars)]
                A.append(row)
                b.append(float(request.forms.get(f'cons_rhs_{i}', 0)))
                signs.append(request.forms.get(f'cons_sign_{i}', '<='))

            # Здесь можно применить логику симплекс-метода или двойственной задачи
            # Пока просто создадим тестовую таблицу для вывода:
            result_table.append(['Базис', 'Cj', 'x1', 'x2', 'Св.член'])
            result_table.append(['x3', 0, 1, 2, 10])
            result_table.append(['x4', 0, 3, 1, 15])
            result_table.append(['Z', '', '', '', 0])

        except Exception as e:
            result_table = [['Ошибка обработки данных:', str(e)]]

    return template('dual_lpp_practice.tpl',
                    title='Двойственная ЗЛП',
                    year=2025,
                    result_table=result_table,
                    num_vars=num_vars,
                    num_cons=num_cons)
