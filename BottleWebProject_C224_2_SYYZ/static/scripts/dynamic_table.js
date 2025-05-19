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
        inp.addEventListener('input', function () {
            const val = this.value;

            // Разрешаем пустую строку, одиночный минус и одиночную точку
            if (val === '' || val === '-' || val === '.') {
                this._lastValid = val;
                return;
            }

            // Проверка до 2 цифр перед точкой и до 2 после
            const re = /^-?\d{1,2}(?:\.\d{0,2})?$/;
            if (!re.test(val)) {
                this.value = this._lastValid;
                return;
            }

            // Проверка на максимальное и минимальное значения
            const num = parseFloat(val);
            if (isNaN(num) || num < minVal || num > maxVal) {
                this.value = this._lastValid;
                return;
            }

            // Сохранение
            this._lastValid = val;
        });
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

    // Сохранение текущего состояния формы в localStorage
    function saveToStorage() {
        // Создание объекта-данных
        const data = {
            numVars: numVarsInput.value,
            numCons: numConsInput.value,
            vars: {},
            consVars: {},
            consSigns: {},
            consRhs: {}
        };

        // Сбор всех коэффициентов целевой функции
        varsContainer.querySelectorAll('input').forEach(input => {
            data.vars[input.name] = input.value;
        });
        // Сбор всех коэффициентов ограничений
        consVarsContainer.querySelectorAll('input').forEach(input => {
            data.consVars[input.name] = input.value;
        });
        // Сбор всех знаков ограничений
        consSignsContainer.querySelectorAll('select').forEach(select => {
            data.consSigns[select.name] = select.value;
        });
        // Сбор всех свободных членов
        consRhsContainer.querySelectorAll('input').forEach(input => {
            data.consRhs[input.name] = input.value;
        });

        localStorage.setItem('directLppData', JSON.stringify(data)); // Сохранение JSON-строки в localStorage
    }

    // Загрузка сохранённых данных и восстановление состояния
    function loadFromStorage() {
        // Чтение из localStorage
        const saved = localStorage.getItem('directLppData');
        // Вызов даже если нет сохранённых данных
        if (!saved) {
            redraw();
            return;
        }

        // Разбор JSON-строки
        const data = JSON.parse(saved);
        numVarsInput.value = data.numVars;
        numConsInput.value = data.numCons;

        redraw();

        // Подстановка сохранённых коэффициентов цели
        for (let [name, value] of Object.entries(data.vars)) { // Проход по парам из объекта data.vars
            const input = document.querySelector(`input[name="${name}"]`); // Поиск на странице input по атрибуту name, равному текущему имени
            if (input) input.value = value; // Если элемент найден, установить его value в сохранённое значение
        }
        // Подстановка сохранённых коэффициентов ограничений
        for (let [name, value] of Object.entries(data.consVars)) { // Проход по парам из объекта data.consVars
            const input = document.querySelector(`input[name="${name}"]`); // Поиск на странице input по атрибуту name, равному текущему имени
            if (input) input.value = value; // Если элемент найден, установить его value в сохранённое значение
        }
        // Подстановка сохранённых знаков ограничений
        for (let [name, value] of Object.entries(data.consSigns)) { // Проход по парам из объекта data.consSigns
            const select = document.querySelector(`select[name="${name}"]`); // Поиск на странице input по атрибуту name, равному текущему имени
            if (select) select.value = value; // Если элемент найден, установить его value в сохранённое значение
        }
        // Подстановка сохранённых свободных членов
        for (let [name, value] of Object.entries(data.consRhs)) { // Проход по парам из объекта data.consRhs
            const input = document.querySelector(`input[name="${name}"]`); // Поиск на странице input по атрибуту name, равному текущему имени
            if (input) input.value = value; // Если элемент найден, установить его value в сохранённое значение
        }
    }

    // Основная функция перерисовки всех таблиц на странице
    function redraw() {
        // Определение текущего количества переменных и ограничений
        const nVars = parseInt(numVarsInput.value, 10) || 2;
        const nCons = parseInt(numConsInput.value, 10) || 1;

        // Создание пустого объекта для хранения предыдущих значений полей целевой функции
        let oldVarsValues = {};
        varsContainer.querySelectorAll('input').forEach(inp => { // Поиск всех input внутри контейнера varsContainer и сбор их текущих значений
            oldVarsValues[inp.name] = inp.value; // Запись значения inp.value в объект под ключом, равным имени поля
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
            if (oldVarsValues[inp.name] !== undefined) inp.value = oldVarsValues[inp.name]; // Если сохранённое значение существует, присвоить его новому input
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
                if (oldConsVarsValues[inp.name] !== undefined) inp.value = oldConsVarsValues[inp.name]; // Если сохранённое значение существует, присвоить его новому input
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
            if (oldConsSignsValues[sel.name] !== undefined) sel.value = oldConsSignsValues[sel.name]; // Если сохранённое значение существует, присвоить его новому input
            sel.addEventListener('change', saveToStorage); // Сохранение данных
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
            if (oldConsRhsValues[inp.name] !== undefined) inp.value = oldConsRhsValues[inp.name]; // Если сохранённое значение существует, присвоить его новому input
            inp.addEventListener('input', saveToStorage); // Сохранение данных
            td.appendChild(inp); // Помещение <input> внутрь ячейки
            tr.appendChild(td); // Добавление заполненной ячейки в строку
            tblR.appendChild(tr); // Добавление заполненной строки в таблицу
        }
        consRhsContainer.appendChild(tblR); // Вставка таблицы на страницу

        // Поиск элемента, куда выводится условие неотрицательности
        const nonnegDiv = document.getElementById('nonnegativity_condition');
        let varsList = [];
        // Формирование списка имён переменных со сниженными индексами
        for (let i = 0; i < nVars; i++) {
            varsList.push(`x<sub>${i + 1}</sub>`); // Добавление строки вида x<sub>i+1</sub> в массив
        }
        nonnegDiv.innerHTML = varsList.join(', ') + ' ≥ 0'; // Объединение элементов массива через запятую и пробел и добавление знака ≥ 0

        // Сохранение текущего состояния всех полей в localStorage
        saveToStorage(); // Сохранение сразу после отрисовки
    }

    // Навешивание события на изменение числа переменных: перерисовка таблиц
    numVarsInput.addEventListener('input', () => { redraw(); });
    numConsInput.addEventListener('input', () => { redraw(); });

    // Загрузка ранее сохранённых данных из localStorage и отрисовка таблиц
    loadFromStorage();

    // Поиск кнопки «Очистка» на странице
    const resetBtn = document.getElementById('reset_button');
    // Навешивание обработчика клика на кнопку «Сброс»
    resetBtn.addEventListener('click', (e) => {
        e.preventDefault(); // Отмена стандартного поведения (отправка формы)

        // Явная очистка всех input и select после перерисовки
        varsContainer.querySelectorAll('input').forEach(input => input.value = '');
        consVarsContainer.querySelectorAll('input').forEach(input => input.value = '');
        consSignsContainer.querySelectorAll('select').forEach(select => select.value = '≤');
        consRhsContainer.querySelectorAll('input').forEach(input => input.value = '');
        saveToStorage();

        // Устанавка начальных значения переменных
        numVarsInput.value = 2;
        numConsInput.value = 1;

        redraw(); // Перерисовка полей

        // Удаление блока с результатами
        const resultBlock = document.getElementById('results');
        if (resultBlock) {
            resultBlock.innerHTML = '';
        }
    });
});