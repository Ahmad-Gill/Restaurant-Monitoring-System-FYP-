if (typeof waitingTimeData !== 'undefined' && waitingTimeData.length > 0 &&
    typeof total_waiting_time_data !== 'undefined' && total_waiting_time_data.length > 0) {

    // Labels and data for the first chart
    const labels = waitingTimeData.map(item => item.table_number);
    const waitingTimes = waitingTimeData.map(item => item.waiting_time);

    // Labels and data for the second chart
    const labels_2 = total_waiting_time_data.map(item => item.date);
    const waitingTimesDate = total_waiting_time_data.map(item => item.total_waiting_time);

    // Common chart options for both charts
    const commonOptions = {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Waiting Time (Minutes)',
                    color: 'white'
                },
                ticks: {
                    autoSkip: true,
                    maxTicksLimit: 10,
                    color: 'white'
                },
            },
            x: {
                title: {
                    display: true,
                    text: 'Table Number', 
                    color: 'white'
                },
                ticks: {
                    autoSkip: true,
                    maxTicksLimit: 10,
                    color: 'white'
                },
            }
        },
        plugins: {
            legend: {
                labels: {
                    color: 'white'
                }
            }
        }
    };

    // Chart 1 - Waiting Time by Table Number
    const ctx1 = document.getElementById('waitingTimeChart1').getContext('2d');
    const waitingTimeChart1 = new Chart(ctx1, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Waiting Time (Minutes) - By Table',
                data: waitingTimes,
                borderColor: '#5B4B8A',  // Purple color
                backgroundColor: 'rgba(91, 75, 138, 0.2)',  // Translucent purple
                borderWidth: 1,
                fill: true,
            }]
        },
        options: commonOptions
    });

    // Chart 2 - Total Waiting Time by Date
    const ctx2 = document.getElementById('waitingTimeChart2').getContext('2d');
    const waitingTimeChart2 = new Chart(ctx2, {
        type: 'line',
        data: {
            labels: labels_2,
            datasets: [{
                label: 'Total Waiting Time (Minutes) - By Date',
                data: waitingTimesDate,
                borderColor: '#5B4B8A',  // Purple color
                backgroundColor: 'rgba(91, 75, 138, 0.2)',  // Translucent purple
                borderWidth: 1,
                fill: true,
            }]
        },
        options: {
            ...commonOptions,
            scales: {
                ...commonOptions.scales,
                x: {
                    ...commonOptions.scales.x,
                    title: {
                        display: true,
                        text: 'Date', 
                        color: 'white'
                    }
                }
            }
        }
    });

} else {
    console.error('Waiting time data or total waiting time data is not defined or is empty.');
}
