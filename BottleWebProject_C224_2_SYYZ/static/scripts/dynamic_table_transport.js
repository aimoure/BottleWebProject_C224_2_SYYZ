function generateMatrix(rows, cols, matrixData = null, supplyData = null, demandData = null) {
    const container = document.getElementById('matrix-container');
    container.innerHTML = '';

    const table = document.createElement('table');
    table.border = "1";
    table.cellPadding = "5";
    table.cellSpacing = "0";
    table.style.borderCollapse = "collapse";

    const headerRow = document.createElement('tr');
    const emptyCell = document.createElement('th');
    headerRow.appendChild(emptyCell);

    for (let j = 0; j < cols; j++) {
        const th = document.createElement('th');
        th.innerHTML = `B<sub>${j + 1}</sub>`;
        headerRow.appendChild(th);
    }

    const supplyHeader = document.createElement('th');
    supplyHeader.innerHTML = 'Запасы, a<sub>i</sub>';
    headerRow.appendChild(supplyHeader);
    table.appendChild(headerRow);

    for (let i = 0; i < rows; i++) {
        const tr = document.createElement('tr');
        const rowHeader = document.createElement('th');
        rowHeader.innerHTML = `A<sub>${i + 1}</sub>`;
        tr.appendChild(rowHeader);

        for (let j = 0; j < cols; j++) {
            const td = document.createElement('td');
            const input = document.createElement('input');
            input.type = 'number';
            input.name = `matrix-${i}-${j}`;
            input.value = matrixData && matrixData[i] && matrixData[i][j] !== undefined ? matrixData[i][j] : 0;
            input.min = 0;
            input.required = true;
            input.style.width = '60px';
            input.style.margin = '0';
            input.style.padding = '0';
            input.style.border = 'none';
            input.style.outline = 'none';
            td.appendChild(input);
            tr.appendChild(td);
        }

        const supplyCell = document.createElement('td');
        const supplyInput = document.createElement('input');
        supplyInput.type = 'number';
        supplyInput.name = `supply-${i}`;
        supplyInput.value = supplyData && supplyData[i] !== undefined ? supplyData[i] : 0;
        supplyInput.min = 0;
        supplyInput.required = true;
        supplyInput.style.width = '60px';
        supplyInput.style.margin = '0';
        supplyInput.style.padding = '0';
        supplyInput.style.border = 'none';
        supplyInput.style.outline = 'none';
        supplyCell.appendChild(supplyInput);
        tr.appendChild(supplyCell);
        table.appendChild(tr);
    }

    const demandRow = document.createElement('tr');
    const demandHeader = document.createElement('th');
    demandHeader.innerHTML = 'Потребности, b<sub>j</sub>';
    demandRow.appendChild(demandHeader);

    for (let j = 0; j < cols; j++) {
        const demandCell = document.createElement('td');
        const demandInput = document.createElement('input');
        demandInput.type = 'number';
        demandInput.name = `demand-${j}`;
        demandInput.value = demandData && demandData[j] !== undefined ? demandData[j] : 0;
        demandInput.min = 0;
        demandInput.required = true;
        demandInput.style.width = '60px';
        demandInput.style.margin = '0';
        demandInput.style.padding = '0';
        demandInput.style.border = 'none';
        demandInput.style.outline = 'none';
        demandCell.appendChild(demandInput);
        demandRow.appendChild(demandCell);
    }

    const emptyDemandCell = document.createElement('td');
    demandRow.appendChild(emptyDemandCell);
    table.appendChild(demandRow);
    container.appendChild(table);
}

function updateMatrix() {
    const rows = parseInt(document.getElementById('rows').value);
    const cols = parseInt(document.getElementById('cols').value);
    if (rows >= 1 && rows <= 10 && cols >= 1 && cols <= 10) {
        // Сохраняем текущие данные формы
        const form = document.querySelector('form');
        const formData = new FormData(form);
        const matrixData = [];
        const supplyData = [];
        const demandData = [];

        for (let i = 0; i < rows; i++) {
            matrixData[i] = [];
            for (let j = 0; j < cols; j++) {
                matrixData[i][j] = parseFloat(formData.get(`matrix-${i}-${j}`)) || 0;
            }
            supplyData[i] = parseFloat(formData.get(`supply-${i}`)) || 0;
        }
        for (let j = 0; j < cols; j++) {
            demandData[j] = parseFloat(formData.get(`demand-${j}`)) || 0;
        }

        generateMatrix(rows, cols, matrixData, supplyData, demandData);
    }
}

document.getElementById('rows').addEventListener('input', updateMatrix);
document.getElementById('cols').addEventListener('input', updateMatrix);

window.onload = function () {
    const rowsInput = document.getElementById('rows');
    const colsInput = document.getElementById('cols');
    // Получаем данные из шаблона
    const costMatrixJson = document.getElementById('cost-matrix-data').value;
    const supplyJson = document.getElementById('supply-data').value;
    const demandJson = document.getElementById('demand-data').value;

    const matrixData = costMatrixJson !== 'null' ? JSON.parse(costMatrixJson) : null;
    const supplyData = supplyJson !== 'null' ? JSON.parse(supplyJson) : null;
    const demandData = demandJson !== 'null' ? JSON.parse(demandJson) : null;

    generateMatrix(
        parseInt(rowsInput.value),
        parseInt(colsInput.value),
        matrixData,
        supplyData,
        demandData
    );
};