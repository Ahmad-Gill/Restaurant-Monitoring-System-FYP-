document.addEventListener("DOMContentLoaded", function () {
    try {
        // Get data from Django template
        let analyticsDataElement = document.getElementById("analyticsData");
        if (!analyticsDataElement) {
            console.error("❌ Analytics data element not found");
            showError("Analytics data element not found.");
            return;
        }

        let jsonData = analyticsDataElement.getAttribute("data-value");
        if (!jsonData) {
            console.error("❌ No data attribute found");
            showError("No data available from server.");
            return;
        }

        // Try to parse the JSON data
        let analyticsData;
        try {
            analyticsData = JSON.parse(jsonData);
            console.log("Successfully parsed JSON data:", analyticsData);
        } catch (e) {
            console.error("❌ Failed to parse JSON data:", e, "Raw data:", jsonData);
            showError("Failed to parse analytics data.");
            return;
        }

        if (!analyticsData || Object.keys(analyticsData).length === 0) {
            console.error("❌ No data found in analyticsData");
            showError("No data available. Please try again later.");
            return;
        }

        // Get URL parameters to check if a date is selected
        const urlParams = new URLSearchParams(window.location.search);
        const selectedDate = urlParams.get('date');
        console.log("Selected date from URL:", selectedDate);

        // Get canvas elements
        let dishesCanvas = document.getElementById("barChart");
        let customerCanvas = document.getElementById("lineChart");
        let peakHoursCanvas = document.getElementById("pieChart");

        if (!dishesCanvas || !customerCanvas || !peakHoursCanvas) {
            console.error("❌ Canvas elements missing");
            showError("Chart elements not found. Please refresh the page.");
            return;
        }

        // Initialize chart contexts
        let dishesCtx = dishesCanvas.getContext("2d");
        let customerCtx = customerCanvas.getContext("2d");
        let peakHoursCtx = peakHoursCanvas.getContext("2d");

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

        // For Popular Dishes (Bar Chart)
        let dishesLabels = [];
        let dishesValues = [];
        
        if (analyticsData.bar_chart && analyticsData.bar_chart.labels) {
            dishesLabels = analyticsData.bar_chart.labels;
            dishesValues = analyticsData.bar_chart.data;
        } else {
            // Default data if nothing is available
            dishesLabels = ["No Data"];
            dishesValues = [0];
        }

        // For Customer Trends (Line Chart) - Always show Max People Per Day
        let customerLabels = [];
        let customerValues = [];
        
        if (analyticsData.line_chart && analyticsData.line_chart.labels) {
            customerLabels = analyticsData.line_chart.labels;
            
            // If there are datasets, use the first one's data
            if (analyticsData.line_chart.datasets && analyticsData.line_chart.datasets.length > 0) {
                customerValues = analyticsData.line_chart.datasets[0].data;
            }
        } else {
            // Default data if nothing is available
            customerLabels = ["No Data"];
            customerValues = [0];
        }

        // For Peak Hours (Pie Chart)
        let peakHoursLabels = [];
        let peakHoursValues = [];
        
        if (analyticsData.pie_chart && analyticsData.pie_chart.labels) {
            peakHoursLabels = analyticsData.pie_chart.labels;
            peakHoursValues = analyticsData.pie_chart.data;
        } else {
            // Default data showing hours of the day
            peakHoursLabels = ["No Data"];
            peakHoursValues = [1];
        }

        console.log("Chart data prepared:", {
            dishes: { labels: dishesLabels, data: dishesValues },
            customers: { labels: customerLabels, data: customerValues },
            peakHours: { labels: peakHoursLabels, data: peakHoursValues }
        });

        // 1. Popular Dishes Chart (Bar Chart)
        new Chart(dishesCtx, {
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

        // 2. Customer Trends Chart (Line Chart) - Always Max People Per Day
        new Chart(customerCtx, {
            type: 'line',
            data: {
                labels: customerLabels,
                datasets: [{
                    label: 'Daily Customer Count',
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
                        text: 'Customer Trends (Max People Per Day)'
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
                    backgroundColor: chartColors.pieColors.slice(0, peakHoursLabels.length),
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
                        text: selectedDate ? `Peak Hours on ${selectedDate}` : 'Peak Hours Distribution',
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
        showError("An error occurred while loading the analytics data: " + error.message);
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