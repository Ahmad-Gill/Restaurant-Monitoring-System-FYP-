const tables = [
    { id: 'T001', location: 'Main Hall' },
    { id: 'T002', location: 'Patio' },
    { id: 'T003', location: 'Bar Area' },
    { id: 'T004', location: 'Private Room' },
    { id: 'T005', location: 'Window Side' }
];
const chefs = [
    { id: 'C001', name: 'Abbas', station: 'Grill' },
    { id: 'C002', name: 'Kazim', station: 'Salad' },
    { id: 'C003', name: 'Munir', station: 'Pastry' }
];
const waiters = [
    { id: 'W001', name: 'Ahmad', section: 'Main Hall' },
    { id: 'W002', name: 'Hassan', section: 'Patio' },
    { id: 'W003', name: 'Sohaib', section: 'Bar Area' },
    { id: 'W004', name: 'Mohsin', section: 'Private Room' }
];

let simulationInterval;
let violations = { tables: {}, chefs: {}, waiters: {} };

function startSimulation() {
    simulationInterval = setInterval(simulateViolation, 3000);
    document.getElementById('startButton').disabled = true;
    document.getElementById('stopButton').disabled = false;
}

function stopSimulation() {
    clearInterval(simulationInterval);
    document.getElementById('startButton').disabled = false;
    document.getElementById('stopButton').disabled = true;
}

function simulateViolation() {
    const violationType = Math.floor(Math.random() * 3);
    let violation = '';

    switch(violationType) {
        case 0:
            violation = simulateTableViolation();
            break;
        case 1:
            violation = simulateChefViolation();
            break;
        case 2:
            violation = simulateWaiterViolation();
            break;
    }

    if (violation) {
        logViolation(violation);
        updateDashboard();
    }
}

function simulateTableViolation() {
    const table = tables[Math.floor(Math.random() * tables.length)];
    if (Math.random() < 0.3) {
        violations.tables[table.id] = (violations.tables[table.id] || 0) + 1;
        return `Table ${table.id} (${table.location}) is dirty`;
    }
    return '';
}

function simulateChefViolation() {
    const chef = chefs[Math.floor(Math.random() * chefs.length)];
    if (Math.random() < 0.2) {
        violations.chefs[chef.id] = (violations.chefs[chef.id] || 0) + 1;
        return `Chef ${chef.id} (${chef.name}, ${chef.station} station) is not wearing an apron`;
    } else if (Math.random() < 0.2) {
        violations.chefs[chef.id] = (violations.chefs[chef.id] || 0) + 1;
        return `Chef ${chef.id} (${chef.name}, ${chef.station} station) is not wearing a head cap`;
    }
    return '';
}

function simulateWaiterViolation() {
    const waiter = waiters[Math.floor(Math.random() * waiters.length)];
    if (Math.random() < 0.2) {
        violations.waiters[waiter.id] = (violations.waiters[waiter.id] || 0) + 1;
        return `Waiter ${waiter.id} (${waiter.name}, ${waiter.section}) is not wearing proper uniform`;
    } else if (Math.random() < 0.2) {
        violations.waiters[waiter.id] = (violations.waiters[waiter.id] || 0) + 1;
        return `Waiter ${waiter.id} (${waiter.name}, ${waiter.section}) is not wearing a name tag`;
    }
    return '';
}

function logViolation(violation) {
    const logElement = document.getElementById('violation-log');
    const violationElement = document.createElement('div');
    violationElement.className = 'violation';
    violationElement.innerHTML = `${new Date().toLocaleTimeString()}: <span class="culprit-info">${violation}</span>`;
    logElement.insertBefore(violationElement, logElement.firstChild);
}

function updateDashboard() {
    const tableStatus = document.getElementById('table-status');
    const chefStatus = document.getElementById('chef-status');
    const waiterStatus = document.getElementById('waiter-status');

    const dirtyTables = Object.keys(violations.tables).length;
    const nonCompliantChefs = Object.keys(violations.chefs).length;
    const nonCompliantWaiters = Object.keys(violations.waiters).length;

    tableStatus.textContent = dirtyTables > 0 ? `${dirtyTables} table(s) need attention` : 'All tables clean';
    chefStatus.textContent = nonCompliantChefs > 0 ? `${nonCompliantChefs} chef(s) non-compliant` : 'All chefs compliant';
    waiterStatus.textContent = nonCompliantWaiters > 0 ? `${nonCompliantWaiters} waiter(s) non-compliant` : 'All waiters compliant';
}