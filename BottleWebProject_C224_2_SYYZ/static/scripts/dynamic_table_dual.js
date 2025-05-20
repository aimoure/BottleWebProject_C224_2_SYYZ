window.addEventListener('DOMContentLoaded', () => {
    // Получение основных DOM-элементов
    const numVarsInput = document.getElementById('number_of_variables');
    const numConsInput = document.getElementById('number_of_constraints');
    const varsContainer = document.getElementById('variables_container');
    const consVarsContainer = document.getElementById('constraints_vars');
    const consSignsContainer = document.getElementById('constraints_signs');
    const consRhsContainer = document.getElementById('constraints_rhs');

    // Применение стилей к таблице
    function styleTable(tbl) {
        tbl.style.borderCollapse = 'collapse';
        tbl.style.marginTop = '10px';
        tbl.style.marginBottom = '10px';
    }

    // Применение стилей к ячейке таблицы
    function styleCell(td) {
        td.style.border = '1px solid #333';
        td.style.padding = '0';
        td.style.margin = '0';
        td.style.textAlign = 'center';
        td.style.fontSize = '18px';
    }

    // Применение стилей и ограничений к числовому полю ввода
    function styleInput(inp, minVal = -99, maxVal = 99) {
        inp.type = 'number';
        inp.style.width = '72px';
        inp.style.height = '30px';
        inp.style.margin = '0';
        inp.style.padding = '0';
        inp.style.border = 'none';
        inp.style.outline = 'none';
        inp.style.borderRadius = '4px';
        inp.style.textAlign = 'center';
        inp.style.fontSize = '18px';
        inp.step = '0.01';
        inp.setAttribute('min', String(minVal));
        inp.setAttribute('max', String(maxVal));
        inp._lastValid = '';

        // Проверка значения при вводе
        inp.addEventListener('input', function () {
            const val = this.value;

            // Разрешается пустая строка, одиночный минус и точка
            if (val === '' || val === '-' || val === '.') {
                this._lastValid = val;
                return;
            }

            // Проверка на формат: до 2 цифр до и после точки
            const re = /^-?\d{1,2}(?:\.\d{0,2})?$/;
            if (!re.test(val)) {
                this.value = this._lastValid;
                return;
            }

            // Проверка на диапазон значений
            const num = parseFloat(val);
            if (isNaN(num) || num < minVal || num > maxVal) {
                this.value = this._lastValid;
                return;
            }

            // Сохранение допустимого значения
            this._lastValid = val;
        });
    }

    // Применение стилей к выпадающему списку
    function styleSelect(sel) {
        sel.style.width = '60px';
        sel.style.height = '30px';
        sel.style.margin = '0';
        sel.style.padding = '0';
        sel.style.border = 'none';
        sel.style.outline = 'none';
        sel.style.borderRadius = '4px';
        sel.style.textAlign = 'center';
        sel.style.fontSize = '18px';
        sel.style.whiteSpace = 'nowrap';
    }

    // Сохранение текущих данных в localStorage
    function saveToStorage() {
        const data = {
            numVars: numVarsInput.value,
            numCons: numConsInput.value,
            vars: {},
            consVars: {},
            consSigns: {},
            consRhs: {}
        };

        // Сбор значений переменных и ограничений
        varsContainer.querySelectorAll('input').forEach(input => {
            data.vars[input.name] = input.value;
        });
        consVarsContainer.querySelectorAll('input').forEach(input => {
            data.consVars[input.name] = input.value;
        });
        consSignsContainer.querySelectorAll('select').forEach(select => {
            data.consSigns[select.name] = select.value;
        });
        consRhsContainer.querySelectorAll('input').forEach(input => {
            data.consRhs[input.name] = input.value;
        });

        localStorage.setItem('dualLppData', JSON.stringify(data));
    }

    // Загрузка данных из localStorage (если они существуют)
    function loadFromStorage() {
        const saved = localStorage.getItem('dualLppData');
        if (!saved) {
            redraw(); // Выполнение перерисовки, даже если данные отсутствуют
            return;
        }

        const data = JSON.parse(saved);
        numVarsInput.value = data.numVars;
        numConsInput.value = data.numCons;

        redraw();

        // Восстановление значений в полях
        for (let [name, value] of Object.entries(data.vars)) {
            const input = document.querySelector(`input[name="${name}"]`);
            if (input) input.value = value;
        }
        for (let [name, value] of Object.entries(data.consVars)) {
            const input = document.querySelector(`input[name="${name}"]`);
            if (input) input.value = value;
        }
        for (let [name, value] of Object.entries(data.consSigns)) {
            const select = document.querySelector(`select[name="${name}"]`);
            if (select) select.value = value;
        }
        for (let [name, value] of Object.entries(data.consRhs)) {
            const input = document.querySelector(`input[name="${name}"]`);
            if (input) input.value = value;
        }
    }

    // Перерисовка таблиц и полей в зависимости от количества переменных и ограничений
    function redraw() {
        const nVars = parseInt(numVarsInput.value, 10) || 2;
        const nCons = parseInt(numConsInput.value, 10) || 1;

        // Сохранение старых значений перед очисткой
        let oldVarsValues = {};
        varsContainer.querySelectorAll('input').forEach(inp => {
            oldVarsValues[inp.name] = inp.value;
        });

        let oldConsVarsValues = {};
        consVarsContainer.querySelectorAll('input').forEach(inp => {
            oldConsVarsValues[inp.name] = inp.value;
        });

        let oldConsSignsValues = {};
        consSignsContainer.querySelectorAll('select').forEach(sel => {
            oldConsSignsValues[sel.name] = sel.value;
        });

        let oldConsRhsValues = {};
        consRhsContainer.querySelectorAll('input').forEach(inp => {
            oldConsRhsValues[inp.name] = inp.value;
        });

        // Очистка контейнеров перед генерацией новых элементов
        varsContainer.innerHTML = '';
        consVarsContainer.innerHTML = '';
        consSignsContainer.innerHTML = '';
        consRhsContainer.innerHTML = '';

        // Создание строки ввода коэффициентов целевой функции
        const tblObj = document.createElement('table');
        styleTable(tblObj);
        const headerObj = document.createElement('tr');
        for (let j = 0; j < nVars; j++) {
            const th = document.createElement('th');
            styleCell(th);
            th.innerHTML = `x<sub>${j + 1}</sub>`;
            headerObj.appendChild(th);
        }
        tblObj.appendChild(headerObj);
        const rowObj = document.createElement('tr');
        for (let j = 0; j < nVars; j++) {
            const td = document.createElement('td');
            styleCell(td);
            const inp = document.createElement('input');
            styleInput(inp);
            inp.name = `x_${j}`;
            if (oldVarsValues[inp.name] !== undefined) inp.value = oldVarsValues[inp.name];
            inp.addEventListener('input', saveToStorage);
            td.appendChild(inp);
            rowObj.appendChild(td);
        }
        tblObj.appendChild(rowObj);
        varsContainer.appendChild(tblObj);

        // Создание таблицы коэффициентов ограничений
        const tblL = document.createElement('table');
        styleTable(tblL);
        const headerL = document.createElement('tr');
        for (let j = 0; j < nVars; j++) {
            const th = document.createElement('th');
            styleCell(th);
            th.innerHTML = `a<sub>${j + 1}</sub>`;
            headerL.appendChild(th);
        }
        tblL.appendChild(headerL);
        for (let i = 0; i < nCons; i++) {
            const tr = document.createElement('tr');
            for (let j = 0; j < nVars; j++) {
                const td = document.createElement('td');
                styleCell(td);
                const inp = document.createElement('input');
                styleInput(inp);
                inp.name = `cons_${i}_${j}`;
                if (oldConsVarsValues[inp.name] !== undefined) inp.value = oldConsVarsValues[inp.name];
                inp.addEventListener('input', saveToStorage);
                td.appendChild(inp);
                tr.appendChild(td);
            }
            tblL.appendChild(tr);
        }
        consVarsContainer.appendChild(tblL);

        // Создание таблицы выбора знаков ограничений
        const tblS = document.createElement('table');
        styleTable(tblS);
        const headerS = document.createElement('tr');
        const thSign = document.createElement('th');
        styleCell(thSign);
        thSign.textContent = 'Знак';
        headerS.appendChild(thSign);
        tblS.appendChild(headerS);
        for (let i = 0; i < nCons; i++) {
            const tr = document.createElement('tr');
            const td = document.createElement('td');
            styleCell(td);
            const sel = document.createElement('select');
            styleSelect(sel);
            sel.name = `cons_sign_${i}`;
            ['≤', '=', '≥'].forEach(sym => {
                const opt = document.createElement('option');
                opt.value = sym;
                opt.textContent = sym;
                sel.appendChild(opt);
            });
            if (oldConsSignsValues[sel.name] !== undefined) sel.value = oldConsSignsValues[sel.name];
            sel.addEventListener('change', saveToStorage);
            td.appendChild(sel);
            tr.appendChild(td);
            tblS.appendChild(tr);
        }
        consSignsContainer.appendChild(tblS);

        // Создание таблицы правых частей ограничений
        const tblR = document.createElement('table');
        styleTable(tblR);
        const headerR = document.createElement('tr');
        const thR = document.createElement('th');
        styleCell(thR);
        thR.textContent = 'b';
        headerR.appendChild(thR);
        tblR.appendChild(headerR);
        for (let i = 0; i < nCons; i++) {
            const tr = document.createElement('tr');
            const td = document.createElement('td');
            styleCell(td);
            const inp = document.createElement('input');
            styleInput(inp);
            inp.name = `cons_rhs_${i}`;
            if (oldConsRhsValues[inp.name] !== undefined) inp.value = oldConsRhsValues[inp.name];
            inp.addEventListener('input', saveToStorage);
            td.appendChild(inp);
            tr.appendChild(td);
            tblR.appendChild(tr);
        }
        consRhsContainer.appendChild(tblR);

        // Обновление условия неотрицательности
        const nonnegDiv = document.getElementById('nonnegativity_condition');
        let varsList = [];
        for (let i = 0; i < nVars; i++) {
            varsList.push(`x<sub>${i + 1}</sub>`);
        }
        nonnegDiv.innerHTML = varsList.join(', ') + ' ≥ 0';

        saveToStorage(); // Сохранение после обновления интерфейса
    }

    // Обработка изменения количества переменных и ограничений
    numVarsInput.addEventListener('input', () => {
        redraw();
    });
    numConsInput.addEventListener('input', () => {
        redraw();
    });

    // Инициализация интерфейса из сохранённых данных
    loadFromStorage();

    // Обработка сброса формы
    const resetBtn = document.getElementById('reset_button');
    resetBtn.addEventListener('click', (e) => {
        e.preventDefault(); // Предотвращение отправки формы

        // Очистка всех полей ввода и восстановление значений по умолчанию
        varsContainer.querySelectorAll('input').forEach(input => input.value = '');
        consVarsContainer.querySelectorAll('input').forEach(input => input.value = '');
        consSignsContainer.querySelectorAll('select').forEach(select => select.value = '≤');
        consRhsContainer.querySelectorAll('input').forEach(input => input.value = '');
        saveToStorage();

        numVarsInput.value = 2;
        numConsInput.value = 1;

        redraw(); // Обновление интерфейса

        // Очистка блока с результатами, если он существует
        const resultBlock = document.getElementById('results');
        if (resultBlock) {
            resultBlock.innerHTML = '';
        }
    });
});
