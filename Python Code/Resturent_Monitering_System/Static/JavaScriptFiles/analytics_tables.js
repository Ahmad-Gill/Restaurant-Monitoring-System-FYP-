document.addEventListener('DOMContentLoaded', function() {
    const dishesData = {
        labels: ['Image', 'Dish', 'Orders', 'Date'],
        data: [
            [staticUrl + 'images/pizza.jpg', 'Pizza', 300, 'Oct 4, 2024'],
            [staticUrl + 'images/burger.jfif', 'Burger', 250, 'Oct 4, 2024'],
            [staticUrl + 'images/pasta.jfif', 'Pasta', 200, 'Oct 4, 2024'],
            [staticUrl + 'images/salad.jfif', 'Salad', 150, 'Oct 4, 2024'],
            [staticUrl + 'images/steak.jfif', 'Steak', 100, 'Oct 4, 2024']
        ]
    };

    const CustomerData = {
        labels: ['Day', 'Customers', 'Date'],
        data: [
            ['Monday', 5000, 'Oct 1, 2024'],
            ['Tuesday', 5500, 'Oct 2, 2024'],
            ['Wednesday', 6000, 'Oct 3, 2024'],
            ['Thursday', 5800, 'Oct 4, 2024'],
            ['Friday', 7000, 'Oct 5, 2024'],
            ['Saturday', 8000, 'Oct 6, 2024'],
            ['Sunday', 7500, 'Oct 7, 2024']
        ]
    };

    const peakHoursData = {
        labels: ['Time', 'Customers', 'Date'],
        data: [
            ['11am', 20, 'Oct 4, 2024'],
            ['12pm', 40, 'Oct 4, 2024'],
            ['1pm', 60, 'Oct 4, 2024'],
            ['2pm', 50, 'Oct 4, 2024'],
            ['3pm', 30, 'Oct 4, 2024'],
            ['4pm', 35, 'Oct 4, 2024'],
            ['5pm', 45, 'Oct 4, 2024'],
            ['6pm', 70, 'Oct 4, 2024'],
            ['7pm', 80, 'Oct 4, 2024'],
            ['8pm', 60, 'Oct 4, 2024']
        ]
    };

    const satisfactionData = {
        labels: ['Rating', 'Percentage (%)', 'Date'],
        data: [
            ['Excellent', 60, 'Oct 4, 2024'],
            ['Good', 20, 'Oct 4, 2024'],
            ['Fair', 10, 'Oct 4, 2024'],
            ['Poor', 10, 'Oct 4, 2024']
        ]
    };

    function createTable(tableId, data) {
        const table = document.getElementById(tableId);
        let html = '<tr>';
        for (let label of data.labels) {
            html += `<th>${label}</th>`;
        }
        html += '</tr>';
        for (let row of data.data) {
            html += '<tr>';
            for (let i = 0; i < row.length; i++) {
                if (tableId === 'dishesTable' && i === 0) {
                    html += `<td><img src="${row[i]}" alt="${row[i+1]}"></td>`;
                } else {
                    html += `<td>${row[i]}</td>`;
                }
            }
            html += '</tr>';
        }
        table.innerHTML = html;
    }

    createTable('dishesTable', dishesData);
    createTable('countTable', CustomerData);
    createTable('peakHoursTable', peakHoursData);
    createTable('satisfactionTable', satisfactionData);
});
