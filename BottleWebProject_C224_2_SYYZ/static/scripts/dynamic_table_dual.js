window.addEventListener('DOMContentLoaded', () => {
    const numVarsInput = document.getElementById('number_of_variables');
    const numConsInput = document.getElementById('number_of_constraints');
    const varsContainer = document.getElementById('variables_container');
    const consVarsContainer = document.getElementById('constraints_vars');
    const consSignsContainer = document.getElementById('constraints_signs');
    const consRhsContainer = document.getElementById('constraints_rhs');

    function styleTable(tbl) {
        tbl.style.borderCollapse = 'collapse';
        tbl.style.marginTop = '10px';
        tbl.style.marginBottom = '10px';
    }

    function styleCell(td) {
        td.style.border = '1px solid #333';
        td.style.padding = '0';
        td.style.margin = '0';
        td.style.textAlign = 'center';
        td.style.fontSize = '18px';
    }

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

        localStorage.setItem('dualLppData', JSON.stringify(data));
    }

    function loadFromStorage() {
        const saved = localStorage.getItem('dualLppData');
        if (!saved) {
            redraw(); // Вызовем даже если нет сохранённых данных
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

    function redraw() {
        const nVars = parseInt(numVarsInput.value, 10) || 2;
        const nCons = parseInt(numConsInput.value, 10) || 1;

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

        varsContainer.innerHTML = '';
        consVarsContainer.innerHTML = '';
        consSignsContainer.innerHTML = '';
        consRhsContainer.innerHTML = '';

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

        const nonnegDiv = document.getElementById('nonnegativity_condition');
        let varsList = [];
        for (let i = 0; i < nVars; i++) {
            varsList.push(`x<sub>${i + 1}</sub>`);
        }
        nonnegDiv.innerHTML = varsList.join(', ') + ' ≥ 0';

        saveToStorage(); // Сохраняем сразу после отрисовки
    }

    numVarsInput.addEventListener('input', () => {
        redraw();
    });

    numConsInput.addEventListener('input', () => {
        redraw();
    });

    loadFromStorage();

    const resetBtn = document.getElementById('reset_button');
    resetBtn.addEventListener('click', () => {
        numVarsInput.value = 2;
        numConsInput.value = 1;
        redraw();

        varsContainer.querySelectorAll('input').forEach(input => input.value = '');
        consVarsContainer.querySelectorAll('input').forEach(input => input.value = '');
        consSignsContainer.querySelectorAll('select').forEach(select => select.value = '≤');
        consRhsContainer.querySelectorAll('input').forEach(input => input.value = '');

        localStorage.removeItem('dualLppData');

        const solutionSection = document.querySelector('.section');
        if (solutionSection) {
            solutionSection.remove();
        }
    });
});
