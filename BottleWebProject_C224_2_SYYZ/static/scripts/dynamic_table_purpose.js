
function generateMatrix(n) {
    const container = document.getElementById('matrix-container');
    container.innerHTML = '';

    const table = document.createElement('table');
    table.border = "1";
    table.cellPadding = "5";
    table.cellSpacing = "0";

    // Генерация первой строки с подписями (пустая ячейка + заголовки столбцов)
    const headerRow = document.createElement('tr');
    const corner = document.createElement('th');
    corner.innerHTML = ''; // верхний левый угол
    headerRow.appendChild(corner);

    for (let j = 0; j < n; j++) {
        const th = document.createElement('th');
        const input = document.createElement('input');
        input.type = 'text';
        input.name = `label-x${j}`;
        input.value = `m${j + 1}`;
        input.style.width = '60px';
            input.style.padding = '0';
        input.style.border = 'none'; 
        input.style.outline = 'none';
        input.style.textAlign = 'center';
        input.required = true;
        th.appendChild(input);
        headerRow.appendChild(th);
    }

    table.appendChild(headerRow);

    // Генерация остальных строк (с подписями строк слева и ячейками ввода)
    for (let i = 0; i < n; i++) {
        const tr = document.createElement('tr');

        const labelCell = document.createElement('th');
        const labelInput = document.createElement('input');
        labelInput.type = 'text';
        labelInput.name = `label-y${i}`;
        labelInput.value = `w${i + 1}`;
        labelInput.style.width = '60px';
            
        labelInput.style.margin = '0';
        labelInput.style.padding = '0';
        labelInput.style.border = 'none'; 
        labelInput.style.outline = 'none';

        labelInput.style.textAlign = 'center';
        labelInput.required = true;
        labelCell.appendChild(labelInput);
        tr.appendChild(labelCell);

        for (let j = 0; j < n; j++) {
            const td = document.createElement('td');
            const input = document.createElement('input');
            input.type = 'number';
            input.name = `matrix-${i}-${j}`;
            input.value = 0;
            input.style.margin = '0';
            input.style.padding = '0';
            input.style.border = 'none'; 
            input.style.outline = 'none';
            input.style.textAlign = 'center';
            input.style.width = '60px';
            input.required = true;
            td.appendChild(input);
            tr.appendChild(td);
        }

        table.appendChild(tr);
    }

    container.appendChild(table);
}

document.getElementById('size').addEventListener('input', function () {
    const size = parseInt(this.value);
    if (size >= 2 && size <= 10) {
        generateMatrix(size);
    }
});

window.onload = function () {
    const sizeInput = document.getElementById('size');
    generateMatrix(parseInt(sizeInput.value));
}


