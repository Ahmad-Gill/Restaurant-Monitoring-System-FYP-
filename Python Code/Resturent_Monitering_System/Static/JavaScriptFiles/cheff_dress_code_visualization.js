// Global chart instances
let barChartInstance = null;
let pieChartInstance = null;
let chartData = null;

// Function to check if thresholds have been crossed
function hasThresholdChanged(oldData, newData) {
    if (!oldData || !newData) return false;
    
    // Get violation counts from both datasets
    const oldCounts = oldData.time_data.map(item => item.violations);
    const newCounts = newData.time_data.map(item => item.violations);
    
    // Check if any violations crossed a threshold
    const thresholds = [0, 2, 5, 8, 10];
    
    for (let i = 0; i < oldCounts.length; i++) {
        const oldCount = oldCounts[i];
        const newCount = newCounts[i];
        
        // Check if counts crossed any threshold
        for (const threshold of thresholds) {
            if ((oldCount <= threshold && newCount > threshold) || 
                (oldCount > threshold && newCount <= threshold)) {
                return true;
            }
        }
    }
    
    return false;
}

// Function to check for threshold violations and update charts
function checkThresholdAndUpdateCharts(newData) {
    // Compare with previous data to detect threshold changes
    const previousData = chartData;
    chartData = newData;
    
    try {
        // Check if violation thresholds have changed
        const thresholdChanged = hasThresholdChanged(previousData, newData);
        
        // Update bar chart data
        if (barChartInstance) {
            barChartInstance.data.labels = newData.time_data.map(item => item.time_slot);
            barChartInstance.data.datasets[0].data = newData.time_data.map(item => item.violations);
            barChartInstance.update();
        }

        // Update pie chart data with special handling for threshold changes
        if (pieChartInstance) {
            // Calculate new violation ranges
            let violationRanges = {
                'No Violations': 0,
                '1-2 Violations': 0,
                '3-5 Violations': 0,
                '6-8 Violations': 0,
                '9-10 Violations': 0,
                'More than 10 Violations': 0
            };
            
            // Count violations for each range
            newData.time_data.forEach(item => {
                const count = item.violations;
                if (count === 0) {
                    violationRanges['No Violations']++;
                } else if (count <= 2) {
                    violationRanges['1-2 Violations']++;
                } else if (count <= 5) {
                    violationRanges['3-5 Violations']++;
                } else if (count <= 8) {
                    violationRanges['6-8 Violations']++;
                } else if (count <= 10) {
                    violationRanges['9-10 Violations']++;
                } else {
                    violationRanges['More than 10 Violations']++;
                }
            });
            
            // Check if ranges have actually changed
            const rangesChanged = !previousData || 
                JSON.stringify(violationRanges) !== JSON.stringify(previousData.violation_ranges);
            
            // Update pie chart data
            pieChartInstance.data.labels = Object.keys(violationRanges);
            pieChartInstance.data.datasets[0].data = Object.values(violationRanges);
            
            // If threshold or ranges changed, add visual feedback
            if (thresholdChanged || rangesChanged) {
                // Flash the chart background
                const canvas = pieChartInstance.canvas;
                canvas.style.transition = 'background-color 0.3s ease';
                canvas.style.backgroundColor = 'rgba(255, 255, 255, 0.1)';
                setTimeout(() => {
                    canvas.style.backgroundColor = 'rgba(255, 255, 255, 0.05)';
                }, 300);
                
                // Add a subtle scale animation
                canvas.style.transform = 'scale(1.02)';
                setTimeout(() => {
                    canvas.style.transform = 'scale(1)';
                }, 500);
                
                // Log changes for debugging
                console.log("🔄 Changes detected - Updating pie chart with new ranges");
                console.log("New violation ranges:", violationRanges);
            }
            
            // Update with animation
            pieChartInstance.update({
                duration: (thresholdChanged || rangesChanged) ? 1000 : 500,
                easing: 'easeInOutQuart'
            });
        }
    } catch (error) {
        console.error("Error updating charts:", error);
        showError("Failed to update charts with new data");
    }
}

// Function to fetch latest data
async function fetchLatestData() {
    try {
        // Add timestamp to URL to prevent caching
        const timestamp = new Date().getTime();
        const url = new URL(window.location.href);
        url.searchParams.set('_', timestamp);
        
        const response = await fetch(url.toString(), {
            headers: {
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache'
            }
        });
        
        const html = await response.text();
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const newDataElement = doc.getElementById('chart_data_json');
        
        if (newDataElement) {
            const newJsonData = newDataElement.getAttribute('data-value');
            if (newJsonData) {
                try {
                    const newChartData = JSON.parse(newJsonData);
                    
                    // Validate the new data structure
                    if (newChartData && 
                        newChartData.time_data && 
                        Array.isArray(newChartData.time_data) && 
                        newChartData.time_data.length > 0) {
                        
                        // Check if data has actually changed before updating
                        if (JSON.stringify(chartData) !== JSON.stringify(newChartData)) {
                            console.log("🔄 New data received, updating charts...");
                            checkThresholdAndUpdateCharts(newChartData);
                        }
                    } else {
                        console.warn("Received invalid data structure");
                    }
                } catch (parseError) {
                    console.error("Error parsing new data:", parseError);
                }
            }
        }
    } catch (error) {
        console.error("Error fetching latest data:", error);
    }
}

// Set up periodic data updates
function setupDataUpdates() {
    // Initial quick checks
    let quickCheckCount = 0;
    const quickCheckInterval = setInterval(() => {
        fetchLatestData();
        quickCheckCount++;
        
        // After 5 quick checks, switch to normal interval
        if (quickCheckCount >= 5) {
            clearInterval(quickCheckInterval);
            // Regular updates every 5 seconds
            setInterval(fetchLatestData, 5000);
        }
    }, 1000);
}

// Function to show error messages in the UI
function showError(message) {
  const errorContainer = document.getElementById("chart-error-container");
  if (errorContainer) {
    errorContainer.textContent = message;
    errorContainer.style.display = "block";
  } else {
    console.error("Error container not found:", message);
  }
}

// Function to hide error messages
function hideError() {
  const errorContainer = document.getElementById("chart-error-container");
  if (errorContainer) {
    errorContainer.style.display = "none";
  }
}

// Function to show the loading indicator
function showLoading() {
  const loadingElement = document.getElementById("chart-loading");
  if (loadingElement) {
    loadingElement.style.display = "flex";
  }
}

// Function to hide the loading indicator
function hideLoading() {
  const loadingElement = document.getElementById("chart-loading");
  if (loadingElement) {
    loadingElement.style.display = "none";
  }
}

// Function to destroy existing chart instances
function destroyChartInstances() {
  if (barChartInstance) {
    barChartInstance.destroy();
    barChartInstance = null;
  }
  if (pieChartInstance) {
    pieChartInstance.destroy();
    pieChartInstance = null;
  }
}

document.addEventListener("DOMContentLoaded", () => {
  showLoading();
  hideError();

  try {
    // Get the chart data element from the HTML
    const chartDataElement = document.getElementById("chart_data_json");
    if (!chartDataElement) {
      throw new Error("Chart data element not found");
    }

    const jsonData = chartDataElement.getAttribute("data-value");
    if (!jsonData) {
      throw new Error("No data-value attribute found");
    }

    chartData = JSON.parse(jsonData);
    console.log("🟢 Parsed JSON:", chartData);

    // Validate chart data structure
    if (!chartData || Object.keys(chartData).length === 0) {
      throw new Error("No data found in chartData");
    }

    if (!chartData.time_data || !Array.isArray(chartData.time_data) || chartData.time_data.length === 0) {
      throw new Error("Time data is missing or empty");
    }

    if (!chartData.violation_ranges || Object.keys(chartData.violation_ranges).length === 0) {
      throw new Error("Violation ranges data is missing or empty");
    }

    // Get the canvas elements for the charts
    const barCanvas = document.getElementById("violationsBarChart");
    const pieCanvas = document.getElementById("violationsPieChart");

    if (!barCanvas || !pieCanvas) {
      throw new Error("Canvas elements missing");
    }

    const barCtx = barCanvas.getContext("2d");
    const pieCtx = pieCanvas.getContext("2d");

    // Destroy any existing chart instances
    destroyChartInstances();

    // Initialize the bar chart - Violations by Time Slot
    barChartInstance = new Chart(barCtx, {
      type: "bar",
      data: {
        labels: chartData.time_data.map((item) => item.time_slot),
        datasets: [
          {
            label: `Dress Code Violations by Time (${chartData.date_key})`,
            data: chartData.time_data.map((item) => item.violations),
            backgroundColor: "#5B4B8A",
            borderColor: "#483D8B",
            borderWidth: 1,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: {
          duration: 1000,
          easing: 'easeInOutQuart',
          onProgress: function(animation) {
            // Flash background briefly when threshold changes
            if (animation.currentStep === 1) {
              const container = document.querySelector('.black-chart-container');
              if (container) {
                container.style.transition = 'background-color 0.3s ease';
                container.style.backgroundColor = '#1a1a1a';
                setTimeout(() => {
                  container.style.backgroundColor = 'black';
                }, 300);
              }
            }
          }
        },
        plugins: {
          title: {
            display: true,
            text: "Chef Dress Code Violations By Time Slot",
            font: {
              size: 16,
            },
          },
          tooltip: {
            callbacks: {
              title: (tooltipItems) => {
                return `Time: ${tooltipItems[0].label}`;
              },
              label: (context) => {
                return `Violations: ${context.parsed.y}`;
              },
            },
          },
        },
        scales: {
          x: {
            beginAtZero: true,
            grid: {
              color: "#000", // Full black grid lines
            },
            title: {
              display: true,
              text: "Time Slot",
              font: {
                weight: "bold",
              },
            },
            ticks: {
              color: "#fff", // White ticks for better contrast
              font: {
                size: 12,
              },
            },
          },
          y: {
            beginAtZero: true,
            grid: {
              color: "#000", // Full black grid lines
            },
            title: {
              display: true,
              text: "Number of Violations",
              font: {
                weight: "bold",
              },
            },
            ticks: {
              color: "#fff", // White ticks for better contrast
              font: {
                size: 12,
              },
            },
          },
        },
      },
    });

    // Initialize the pie chart - Violation Distribution
    pieChartInstance = new Chart(pieCtx, {
      type: "pie",
      data: {
        labels: Object.keys(chartData.violation_ranges),
        datasets: [
          {
            label: `Violation Count Distribution (${chartData.date_key})`,
            data: Object.values(chartData.violation_ranges),
            backgroundColor: ["#FFB400", "#FF5733", "#17A589", "#3498DB", "#E74C3C", "#9B59B6"],
            borderColor: "#FFFFFF",
            borderWidth: 1,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: {
          duration: 1000,
          easing: 'easeInOutQuart'
        },
        plugins: {
          title: {
            display: true,
            text: "Violation Count Distribution",
            font: {
              size: 16,
            },
          },
          legend: {
            position: "right",
            labels: {
              boxWidth: 15,
              padding: 15,
              font: {
                size: 12,
              },
            },
          },
          tooltip: {
            callbacks: {
              title: (tooltipItems) => {
                return `Range: ${tooltipItems[0].label}`;
              },
              label: (context) => {
                const label = context.label || "";
                const value = context.raw || 0;
                return `${label}: ${value} time slots`;
              },
              afterLabel: (context) => {
                const percentage = (context.raw / context.dataset.data.reduce((a, b) => a + b, 0)) * 100;
                return `${percentage.toFixed(1)}% of total`;
              },
            },
          },
        },
      },
    });

    // Set up automatic data updates
    setupDataUpdates();

    // Hide loading indicator once charts are ready
    hideLoading();
  } catch (error) {
    console.error("🚨 Error:", error);
    showError(`Error loading charts: ${error.message}`);
    hideLoading();
  }

  // Add window resize event listener to handle chart resizing
  window.addEventListener("resize", function () {
    if (barChartInstance && pieChartInstance) {
      barChartInstance.resize();
      pieChartInstance.resize();
    }
  });
});