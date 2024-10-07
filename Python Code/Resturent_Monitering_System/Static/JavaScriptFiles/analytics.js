document.addEventListener('DOMContentLoaded', function() {
    const chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false,
                labels: {
                    color: '#ffffff'
                }
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                ticks: {
                    font: {
                        size: 10
                    },
                    color: '#ffffff'
                }
            },
            x: {
                ticks: {
                    font: {
                        size: 10
                    },
                    color: '#ffffff'
                }
            }
        }
    };

    new Chart(document.getElementById('dishesChart'), {
        type: 'bar',
        data: {
            labels: ['Pizza', 'Burger', 'Pasta', 'Salad', 'Steak'],
            datasets: [{
                label: 'Orders',
                data: [3000, 250, 200, 150, 100],
                backgroundColor: 'rgba(91, 75, 138, 0.7)',
                borderColor: 'rgba(91, 75, 138, 1)',
                borderWidth: 1
            }]
        },
        options: chartOptions
    });

    new Chart(document.getElementById('CustomerChart'), {
        type: 'line',
        data: {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            datasets: [{
                label: 'Customers',
                data: [5000, 5500, 6000, 5800, 7000, 8000, 7500],
                borderColor: 'rgba(91, 75, 138, 1)',
                tension: 0.1
            }]
        },
        options: chartOptions
    });

    new Chart(document.getElementById('peakHoursChart'), {
        type: 'bar',
        data: {
            labels: ['11am', '12pm', '1pm', '2pm', '3pm', '4pm', '5pm', '6pm', '7pm', '8pm','9pm','10pm','11pm'],
            datasets: [{
                label: 'Customers',
                data: [20, 40, 60, 50, 30, 35, 45, 70, 80, 60, 20, 30, 30],
                backgroundColor: 'rgba(91, 75, 138, 0.7)',
                borderColor: 'rgba(91, 75, 138, 1)',
                borderWidth: 1
            }]
        },
        options: chartOptions
    });

    new Chart(document.getElementById('satisfactionChart'), {
        type: 'pie',
        data: {
            labels: ['Excellent', 'Good', 'Fair', 'Poor'],
            datasets: [{
                label: 'Satisfaction',
                data: [60, 20, 10, 10],
                backgroundColor: [
                    'rgba(91, 75, 138, 0.7)',
                    'rgba(255, 99, 132, 0.7)',
                    'rgba(54, 162, 235, 0.7)',
                    'rgba(255, 206, 86, 0.7)'
                ],
                borderColor: [
                    'rgba(91, 75, 138, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'right',
                    labels: {
                        font: {
                            size: 12
                        },
                        color: '#ffffff'
                    }
                }
            },
            scales: {
                x: { display: false },
                y: { display: false }
            }
        }
    });
});