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
            let value = matrixData && matrixData[i] && matrixData[i][j] !== undefined ? matrixData[i][j] : 0;
            input.value = isNaN(value) ? 0 : value;
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
        let supplyValue = supplyData && supplyData[i] !== undefined ? supplyData[i] : 0;
        supplyInput.value = isNaN(supplyValue) ? 0 : supplyValue;
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
        let demandValue = demandData && demandData[j] !== undefined ? demandData[j] : 0;
        demandInput.value = isNaN(demandValue) ? 0 : demandValue;
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
        const matrixData = [];
        const supplyData = [];
        const demandData = [];

        for (let i = 0; i < rows; i++) {
            matrixData[i] = [];
            for (let j = 0; j < cols; j++) {
                const matrixInput = document.querySelector(`input[name="matrix-${i}-${j}"]`);
                matrixData[i][j] = matrixInput ? parseFloat(matrixInput.value) || 0 : 0;
            }
            const supplyInput = document.querySelector(`input[name="supply-${i}"]`);
            supplyData[i] = supplyInput ? parseFloat(supplyInput.value) || 0 : 0;
        }
        for (let j = 0; j < cols; j++) {
            const demandInput = document.querySelector(`input[name="demand-${j}"]`);
            demandData[j] = demandInput ? parseFloat(demandInput.value) || 0 : 0;
        }

        generateMatrix(rows, cols, matrixData, supplyData, demandData);
    }
}

document.getElementById('rows').addEventListener('input', updateMatrix);
document.getElementById('cols').addEventListener('input', updateMatrix);

document.querySelector('form').addEventListener('submit', function (e) {
    if (e.submitter && e.submitter.value === 'clear') {
        document.getElementById('cost-matrix-data').value = '[]';
        document.getElementById('supply-data').value = '[]';
        document.getElementById('demand-data').value = '[]';
        return;
    }

    const rows = parseInt(document.getElementById('rows').value);
    const cols = parseInt(document.getElementById('cols').value);
    const matrixData = [];
    const supplyData = [];
    const demandData = [];

    for (let i = 0; i < rows; i++) {
        matrixData[i] = [];
        for (let j = 0; j < cols; j++) {
            const matrixInput = document.querySelector(`input[name="matrix-${i}-${j}"]`);
            matrixData[i][j] = matrixInput ? parseFloat(matrixInput.value) || 0 : 0;
        }
        const supplyInput = document.querySelector(`input[name="supply-${i}"]`);
        supplyData[i] = supplyInput ? parseFloat(supplyInput.value) || 0 : 0;
    }
    for (let j = 0; j < cols; j++) {
        const demandInput = document.querySelector(`input[name="demand-${j}"]`);
        demandData[j] = demandInput ? parseFloat(demandInput.value) || 0 : 0;
    }

    document.getElementById('cost-matrix-data').value = JSON.stringify(matrixData);
    document.getElementById('supply-data').value = JSON.stringify(supplyData);
    document.getElementById('demand-data').value = JSON.stringify(demandData);
});

window.onload = function () {
    const rowsInput = document.getElementById('rows');
    const colsInput = document.getElementById('cols');
    const costMatrixJson = document.getElementById('cost-matrix-data').value;
    const supplyJson = document.getElementById('supply-data').value;
    const demandJson = document.getElementById('demand-data').value;

    let matrixData = null, supplyData = null, demandData = null;
    try {
        matrixData = costMatrixJson !== 'null' ? JSON.parse(costMatrixJson) : null;
        supplyData = supplyJson !== 'null' ? JSON.parse(supplyJson) : null;
        demandData = demandJson !== 'null' ? JSON.parse(demandJson) : null;

        const rows = parseInt(rowsInput.value);
        const cols = parseInt(colsInput.value);
        if (matrixData && (matrixData.length !== rows || (matrixData[0] && matrixData[0].length !== cols))) {
            matrixData = null;
        }
        if (supplyData && supplyData.length !== rows) {
            supplyData = null;
        }
        if (demandData && demandData.length !== cols) {
            demandData = null;
        }
    } catch (e) {
        console.error("Ошибка парсинга данных:", e);
        matrixData = null;
        supplyData = null;
        demandData = null;
    }

    generateMatrix(parseInt(rowsInput.value), parseInt(colsInput.value), matrixData, supplyData, demandData);
};