document.addEventListener("DOMContentLoaded", function () {
    try {
        // Get data from Django template
        let analyticsDataElement = document.getElementById("analyticsData");
        if (!analyticsDataElement) {
            showError("Analytics data element not found.");
            return;
        }

        let jsonData = analyticsDataElement.getAttribute("data-value");
        if (!jsonData) {
            showError("No data available from server.");
            return;
        }

        // Try to parse the JSON data
        let analyticsData;
        try {
            analyticsData = JSON.parse(jsonData);
        } catch (e) {
            console.error("Failed to parse JSON data:", e);
            showError("Failed to parse analytics data.");
            return;
        }

        // Debug: Log the data structure to console
        console.log("Analytics Data:", analyticsData);

        if (!analyticsData || Object.keys(analyticsData).length === 0) {
            console.error("❌ No data found in analyticsData");
            showError("No data available. Please try again later.");
            return;
        }

        // Get canvas elements
        let dishesCanvas = document.getElementById("barChart");
        let customerCanvas = document.getElementById("lineChart");
        let peakHoursCanvas = document.getElementById("pieChart");

        if (!dishesCanvas || !customerCanvas || !peakHoursCanvas) {
            console.error("❌ Canvas elements missing");
            showError("Chart elements not found. Please refresh the page.");
            return;
        }

        // Chart colors
        const chartColors = {
            primary: '#5B4B8A',
            secondary: '#FFB400',
            accent: '#FF5733',
            pieColors: [
                '#5B4B8A', '#FFB400', '#FF5733', '#17A589', '#3498DB', 
                '#E74C3C', '#9B59B6', '#1ABC9C', '#F1C40F', '#34495E'
            ]
        };
        
        // Common chart options
        const commonOptions = {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                tooltip: {
                    backgroundColor: '#222',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    displayColors: false
                },
                legend: {
                    labels: {
                        color: '#fff'
                    }
                },
                title: {
                    display: true,
                    color: '#fff',
                    font: {
                        size: 14,
                        weight: 'bold'
                    },
                    padding: {
                        top: 10,
                        bottom: 10
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: '#fff',
                        font: {
                            size: 10
                        }
                    }
                },
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: '#fff',
                        font: {
                            size: 10
                        }
                    }
                }
            }
        };

        // Prepare data for each chart
        // For Popular Dishes (Bar Chart)
        let dishesLabels = [];
        let dishesValues = [];
        
        if (analyticsData.popular_dishes && analyticsData.popular_dishes.length > 0) {
            dishesLabels = analyticsData.popular_dishes.map(item => item.dish_name);
            dishesValues = analyticsData.popular_dishes.map(item => item.count);
        } else if (analyticsData.meals_data && analyticsData.meals_data.labels) {
            dishesLabels = analyticsData.meals_data.labels;
            dishesValues = analyticsData.meals_data.values;
        } else {
            // Default data if nothing is available
            dishesLabels = ["No Data"];
            dishesValues = [0];
        }

        // For Customer Trends (Line Chart)
        let customerLabels = [];
        let customerValues = [];
        
        if (analyticsData.customer_types && analyticsData.customer_types.length > 0) {
            customerLabels = analyticsData.customer_types.map(item => item.type);
            customerValues = analyticsData.customer_types.map(item => item.count);
        } else if (analyticsData.customer_data && analyticsData.customer_data.dates) {
            customerLabels = analyticsData.customer_data.dates;
            customerValues = analyticsData.customer_data.counts;
        } else {
            // Default data if nothing is available
            customerLabels = ["No Data"];
            customerValues = [0];
        }

        // For Peak Hours (Pie Chart)
        let peakHoursLabels = [];
        let peakHoursValues = [];
        
        if (analyticsData.peak_hours && analyticsData.peak_hours.hours) {
            peakHoursLabels = analyticsData.peak_hours.hours;
            peakHoursValues = analyticsData.peak_hours.counts;
        } else {
            // Default data showing hours of the day
            peakHoursLabels = Array.from({length: 12}, (_, i) => `${i+1}:00 ${i < 11 ? 'AM' : 'PM'}`);
            peakHoursValues = Array.from({length: 12}, () => Math.floor(Math.random() * 10));
        }

        // 1. Popular Dishes Chart (Bar Chart)
        new Chart(dishesCanvas, {
            type: 'bar',
            data: {
                labels: dishesLabels,
                datasets: [{
                    label: 'Orders',
                    data: dishesValues,
                    backgroundColor: chartColors.primary,
                    borderColor: 'rgba(255, 255, 255, 0.3)',
                    borderWidth: 1,
                    borderRadius: 4
                }]
            },
            options: {
                ...commonOptions,
                plugins: {
                    ...commonOptions.plugins,
                    legend: {
                        display: false
                    },
                    title: {
                        ...commonOptions.plugins.title,
                        text: 'Popular Dishes'
                    }
                }
            }
        });

        // 2. Customer Trends Chart (Line Chart)
        new Chart(customerCanvas, {
            type: 'line',
            data: {
                labels: customerLabels,
                datasets: [{
                    label: 'Customers',
                    data: customerValues,
                    borderColor: chartColors.accent,
                    backgroundColor: 'rgba(255, 87, 51, 0.1)',
                    borderWidth: 2,
                    tension: 0.3,
                    fill: true,
                    pointBackgroundColor: chartColors.accent,
                    pointBorderColor: '#fff',
                    pointRadius: 4
                }]
            },
            options: {
                ...commonOptions,
                plugins: {
                    ...commonOptions.plugins,
                    legend: {
                        display: false
                    },
                    title: {
                        ...commonOptions.plugins.title,
                        text: 'Customer Trends'
                    }
                }
            }
        });

        // 3. Peak Hours Chart (Pie Chart)
        new Chart(peakHoursCtx, {
            type: 'pie',
            data: {
                labels: peakHoursLabels,
                datasets: [{
                    data: peakHoursValues,
                    backgroundColor: chartColors.pieColors,
                    borderColor: 'rgba(255, 255, 255, 0.3)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    tooltip: {
                        backgroundColor: '#222',
                        titleColor: '#fff',
                        bodyColor: '#fff'
                    },
                    legend: {
                        display: true,
                        position: 'right',
                        labels: {
                            color: '#fff',
                            font: {
                                size: 10
                            },
                            boxWidth: 10
                        }
                    },
                    title: {
                        display: true,
                        text: 'Peak Hours',
                        color: '#fff',
                        font: {
                            size: 14,
                            weight: 'bold'
                        },
                        padding: {
                            top: 10,
                            bottom: 10
                        }
                    }
                }
            }
        });

    } catch (error) {
        console.error("🚨 Error:", error);
        showError("An error occurred while loading the analytics data.");
    }
});

// Function to show error messages
function showError(message) {
    const container = document.getElementById('error-container');
    if (container) {
        container.innerHTML = `
            <div class="error-message">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"></circle>
                    <line x1="12" y1="8" x2="12" y2="12"></line>
                    <line x1="12" y1="16" x2="12.01" y2="16"></line>
                </svg>
                <p>${message}</p>
            </div>
        `;
    } else {
        console.error("Error container not found");
        alert(message);
    }
}