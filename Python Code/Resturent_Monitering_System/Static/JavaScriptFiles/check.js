document.addEventListener('DOMContentLoaded', function() {
    const tables = [
        { image: staticUrl + 'images/table1.jfif', location: 'Main Hall', date: 'Oct 4, 2024', time: '12:30 PM' },
        { image: staticUrl + 'images/table2.jfif', location: 'Patio', date: 'Oct 4, 2024', time: '1:15 PM' }
    ];
    const chefs = [
        { image: staticUrl + 'images/chef.jfif', station: 'Grill', date: 'Oct 4, 2024', time: '12:00 PM' }
    ];
    const waiters = [
        { image: staticUrl + 'images/waiter 1.jfif', section: 'Main Hall', date: 'Oct 4, 2024', time: '12:45 PM' },
        { image: staticUrl + 'images/waiter 2.jfif', section: 'Patio', date: 'Oct 4, 2024', time: '1:00 PM' }
    ];

    function populateTables() {
        // Populate Dirty Tables
        const dirtyTablesBody = document.querySelector('#dirty-tables tbody');
        tables.forEach(table => {
            dirtyTablesBody.innerHTML += `
                <tr>
                    <td><img src="${table.image}" alt="Table" class="table-image"></td>
                    <td>${table.location}</td>
                    <td>${table.date}</td>
                    <td>${table.time}</td>
                </tr>
            `;
        });

        // Populate Non-Compliant Chefs
        const nonCompliantChefsBody = document.querySelector('#non-compliant-chefs tbody');
        chefs.forEach(chef => {
            nonCompliantChefsBody.innerHTML += `
                <tr>
                    <td><img src="${chef.image}" alt="Chef" class="table-image"></td>
                    <td>${chef.station}</td>
                    <td>${chef.date}</td>
                    <td>${chef.time}</td>
                </tr>
            `;
        });

        // Populate Non-Compliant Waiters
        const nonCompliantWaitersBody = document.querySelector('#non-compliant-waiters tbody');
        waiters.forEach(waiter => {
            nonCompliantWaitersBody.innerHTML += `
                <tr>
                    <td><img src="${waiter.image}" alt="Waiter" class="table-image"></td>
                    <td>${waiter.section}</td>
                    <td>${waiter.date}</td>
                    <td>${waiter.time}</td>
                </tr>
            `;
        });
    }

    // Populate tables with hardcoded data
    populateTables();
});