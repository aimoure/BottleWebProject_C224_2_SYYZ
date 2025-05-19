window.addEventListener('DOMContentLoaded', () => {
    // Получение элементов
    // Количество переменных и ограничений
    const numVarsInput = document.getElementById('number_of_variables');
    const numConsInput = document.getElementById('number_of_constraints');
    // Контейнеры для отрисовки
    const varsContainer = document.getElementById('variables_container');
    const consVarsContainer = document.getElementById('constraints_vars');
    const consSignsContainer = document.getElementById('constraints_signs');
    const consRhsContainer = document.getElementById('constraints_rhs');

    // Общий стиль для всех таблиц
    // Таблицы
    function styleTable(tbl) {
        tbl.style.borderCollapse = 'collapse';
        tbl.style.marginTop = '10px';
        tbl.style.marginBottom = '10px';
    }
    // Ячейки таблицы
    function styleCell(td) {
        td.style.border = '1px solid #333';
        td.style.padding = '0';
        td.style.margin = '0';
        td.style.textAlign = 'center';
        td.style.fontSize = '18px';
    }
    // Input для ввода
    function styleInput(inp) {
        inp.type = 'number';
        inp.style.width = '60px';
        inp.style.height = '30px';
        inp.style.margin = '0';
        inp.style.padding = '0';
        inp.style.border = 'none';
        inp.style.outline = 'none';
        inp.style.borderRadius = '4px';
        inp.style.textAlign = 'center';
        inp.style.fontSize = '18px';
    }
    // Выпадающий список
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

    function saveToStorage() {
        const data = {
            numVars: numVarsInput.value,
            numCons: numConsInput.value,
            vars: {},
            consVars: {},
            consSigns: {},
            consRhs: {}
        };

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

        localStorage.setItem('directLppData', JSON.stringify(data));
    }

    function loadFromStorage() {
        const saved = localStorage.getItem('directLppData');
        if (!saved) {
            redraw(); // Вызов даже если нет сохранённых данных
            return;
        }

        const data = JSON.parse(saved);
        numVarsInput.value = data.numVars;
        numConsInput.value = data.numCons;

        redraw();

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

    // Основная функция перерисовки всех таблиц на странице
    function redraw() {
        // Определение текущего количества переменных и ограничений
        const nVars = parseInt(numVarsInput.value, 10) || 2;
        const nCons = parseInt(numConsInput.value, 10) || 1;

        let oldVarsValues = {};
        varsContainer.querySelectorAll('input').forEach(inp => {
            oldVarsValues[inp.name] = inp.value;
        });
        // Отрисовка таблицы коэффициентов целевой функции
        varsContainer.innerHTML = ''; // Очистка контейнера перед отрисовкой
        const tblObj = document.createElement('table'); // Создание нового элемента <table> для хранения целевой функции
        styleTable(tblObj); // Применение общих стилей таблицы
        // Создание строки заголовка с названиями переменных
        const headerObj = document.createElement('tr');
        for (let j = 0; j < nVars; j++) {
            const th = document.createElement('th'); // Создание ячейки таблицы
            styleCell(th); // Стилизация ячейки
            th.innerHTML = `x${j + 1}`; // Текст ячейки
            headerObj.appendChild(th); // Добавление заполненной ячейки в строку
        }
        tblObj.appendChild(headerObj); // Добавление заполненной строки в таблицу
        const rowObj = document.createElement('tr'); // Создание строки
        // Создание ячеек с input для каждого коэфициента
        for (let j = 0; j < nVars; j++) {
            const td = document.createElement('td'); // Создание ячейки таблицы
            styleCell(td); // Стилизация ячейки
            const inp = document.createElement('input'); // Создание поля ввода
            styleInput(inp); // Стилизация input
            inp.name = `x_${j}`; // Уникальное имя поля
            if (oldVarsValues[inp.name] !== undefined) inp.value = oldVarsValues[inp.name];
            inp.addEventListener('input', saveToStorage); // Сохранение данных
            td.appendChild(inp); // Помещение <input> внутрь ячейки
            rowObj.appendChild(td); // Добавление заполненной ячейки в строку
        }
        tblObj.appendChild(rowObj); // Добавление заполненной строки в таблицу
        varsContainer.appendChild(tblObj); // Вставка таблицы на страницу

        let oldConsVarsValues = {};
        consVarsContainer.querySelectorAll('input').forEach(inp => {
            oldConsVarsValues[inp.name] = inp.value;
        });
        // Ограничения: коэфициенты
        consVarsContainer.innerHTML = ''; // Очистка контейнера перед отрисовкой
        const tblL = document.createElement('table'); // Создание нового элемента <table> для хранения коэфициентов ограничений
        styleTable(tblL); // Применение общих стилей таблицы
        // Создание строки заголовка с названиями коэффициентов
        const headerL = document.createElement('tr');
        for (let j = 0; j < nVars; j++) {
            const th = document.createElement('th'); // Создание ячейки таблицы
            styleCell(th); // Стилизация ячейки
            th.innerHTML = `a<sub>${j + 1}</sub>`; // Текст ячейки
            headerL.appendChild(th); // Добавление заполненной ячейки в строку
        }
        tblL.appendChild(headerL); // Добавление заполненной строки в таблицу
        // Создание ячеек с input для каждого коэфициента
        for (let i = 0; i < nCons; i++) {
            const tr = document.createElement('tr'); // Создание строки
            for (let j = 0; j < nVars; j++) {
                const td = document.createElement('td'); // Создание ячейки таблицы
                styleCell(td); // Стилизация ячейки
                const inp = document.createElement('input'); // Создание поля ввода
                styleInput(inp); // Стилизация input
                inp.name = `cons_${i}_${j}`; // Уникальное имя поля
                if (oldVarsValues[inp.name] !== undefined) inp.value = oldVarsValues[inp.name];
                inp.addEventListener('input', saveToStorage); // Сохранение данных
                td.appendChild(inp); // Помещение <input> внутрь ячейки
                tr.appendChild(td); // Добавление заполненной ячейки в строку
            }
            tblL.appendChild(tr); // Добавление заполненной строки в таблицу
        }
        consVarsContainer.appendChild(tblL); // Вставка таблицы на страницу

        let oldConsSignsValues = {};
        consSignsContainer.querySelectorAll('select').forEach(sel => {
            oldConsSignsValues[sel.name] = sel.value;
        });
        // Ограничения: знак
        consSignsContainer.innerHTML = ''; // Очистка контейнера перед отрисовкой
        const tblS = document.createElement('table'); // Создание нового элемента <table> для хранения знаков
        styleTable(tblS); // Применение общих стилей таблицы
        // Создание строки заголовка
        const headerS = document.createElement('tr');
        const thSign = document.createElement('th'); // Создание ячейки таблицы
        styleCell(thSign); // Стилизация ячейки
        thSign.textContent = 'Знак'; // Текст ячейки
        headerS.appendChild(thSign); // Добавление заполненной ячейки в строку
        tblS.appendChild(headerS); // Добавление заполненной строки в таблицу
        // Создание ячеек с input для каждого знака
        for (let i = 0; i < nCons; i++) {
            const tr = document.createElement('tr'); // Создание строки
            const td = document.createElement('td'); // Создание ячейки таблицы
            styleCell(td); // Стилизация ячейки
            const sel = document.createElement('select'); // Создание поля выпадающего списка
            styleSelect(sel); // Стилизация выпадающего списка
            sel.name = `cons_sign_${i}`; // Уникальное имя поля
            // Добавление опций с символами ≤, = и ≥
            ['≤', '=', '≥'].forEach(sym => {
                const opt = document.createElement('option'); // Для каждого элемента массива создаётся новый элемент <option>
                opt.value = sym; // Значение атрибута value у <option> устанавливается равным текущей строке sym
                opt.textContent = sym; // Текстовое содержимое <option>, отображаемое в выпадающем списке, тоже устанавливается в sym
                sel.appendChild(opt); // Вставка готового <option> внутрь элемента <select> (селектора)
            });
            if (oldVarsValues[inp.name] !== undefined) inp.value = oldVarsValues[inp.name];
            inp.addEventListener('input', saveToStorage); // Сохранение данных
            td.appendChild(sel); // Помещение выпадающего списка внутрь ячейки
            tr.appendChild(td); // Добавление заполненной ячейки в строку
            tblS.appendChild(tr); // Добавление заполненной строки в таблицу
        }
        consSignsContainer.appendChild(tblS); // Вставка таблицы на страницу

        let oldConsRhsValues = {};
        consRhsContainer.querySelectorAll('input').forEach(inp => {
            oldConsRhsValues[inp.name] = inp.value;
        });
        // Ограничения: свободный член
        consRhsContainer.innerHTML = ''; // Очистка контейнера перед отрисовкой
        const tblR = document.createElement('table'); // Создание нового элемента <table> для хранения свободных членов
        styleTable(tblR); // Применение общих стилей таблицы
        // Создание строки заголовка
        const headerR = document.createElement('tr');
        const thR = document.createElement('th'); // Создание ячейки таблицы
        styleCell(thR); // Стилизация ячейки
        thR.textContent = 'b'; // Текст ячейки
        headerR.appendChild(thR); // Добавление заполненной ячейки в строку
        tblR.appendChild(headerR); // Добавление заполненной строки в таблицу
        // Создание ячеек с input для каждого свободного члена
        for (let i = 0; i < nCons; i++) {
            const tr = document.createElement('tr'); // Создание строки
            const td = document.createElement('td'); // Создание ячейки таблицы
            styleCell(td); // Стилизация ячейки
            const inp = document.createElement('input'); // Создание поля ввода
            styleInput(inp); // Стилизация input
            inp.name = `cons_rhs_${i}`; // Уникальное имя поля
            if (oldVarsValues[inp.name] !== undefined) inp.value = oldVarsValues[inp.name];
            inp.addEventListener('input', saveToStorage); // Сохранение данных
            td.appendChild(inp); // Помещение <input> внутрь ячейки
            tr.appendChild(td); // Добавление заполненной ячейки в строку
            tblR.appendChild(tr); // Добавление заполненной строки в таблицу
        }
        consRhsContainer.appendChild(tblR); // Вставка таблицы на страницу

        const nonnegDiv = document.getElementById('nonnegativity_condition');
        let varsList = [];
        for (let i = 0; i < nVars; i++) {
            varsList.push(`x<sub>${i + 1}</sub>`);
        }
        nonnegDiv.innerHTML = varsList.join(', ') + ' ≥ 0';

        saveToStorage(); // Сохранение сразу после отрисовки
    }

    // Навешивание обработчиков на изменение числа переменных и ограничений
    numVarsInput.addEventListener('input', redraw);
    numConsInput.addEventListener('input', redraw);

    // Инициализация
    redraw();

    numVarsInput.addEventListener('input', () => {
        redraw();
    });

    numConsInput.addEventListener('input', () => {
        redraw();
    });

    loadFromStorage();

    const resetBtn = document.getElementById('reset_button');
    resetBtn.addEventListener('click', (e) => {
        e.preventDefault(); // Не отправлять форму

        // Устанавливаем начальные значения переменных
        numVarsInput.value = 2;
        numConsInput.value = 1;

        // Удаляем сохранённые данные
        localStorage.removeItem('dualLppData');

        // Перерисовываем поля
        redraw();

        // Явно очищаем все input'ы и select'ы после перерисовки
        varsContainer.querySelectorAll('input').forEach(input => input.value = '');
        consVarsContainer.querySelectorAll('input').forEach(input => input.value = '');
        consSignsContainer.querySelectorAll('select').forEach(select => select.value = '≤');
        consRhsContainer.querySelectorAll('input').forEach(input => input.value = '');

        // Удалить блок с результатами
        const resultBlock = document.getElementById('results');
        if (resultBlock) {
            resultBlock.innerHTML = '';
        }
    });
});