document.addEventListener("DOMContentLoaded", function () {
    try {
        let groupedDataElement = document.getElementById("groupedData");
        let jsonData = groupedDataElement.getAttribute("data-value");
        let groupedData = JSON.parse(jsonData);
        console.log("🟢 Parsed JSON:", groupedData);

        if (!groupedData || groupedData.length === 0) {
            console.error("❌ No data found in groupedData");
            return;
        }
        let canvas1 = document.getElementById("waitingTimeChart1");
        let canvas2 = document.getElementById("waitingTimeChart2");

        if (!canvas1 || !canvas2) {
            console.error("❌ Canvas elements missing");
            return;
        }
        let ctx1 = canvas1.getContext("2d");
        let ctx2 = canvas2.getContext("2d");

        let barChart, pieChart;
        let selectedDate = null; 
        function createChunks(data, ranges) {
            let chunkedData = new Array(ranges.length).fill(0);
            data.forEach(time => {
                for (let i = 0; i < ranges.length; i++) {
                    if (time <= ranges[i]) {
                        chunkedData[i]++;
                        break;
                    }
                }
            });
            return chunkedData;
        }
        function getAggregatedData() {
            return {
                dates: groupedData.map(d => d.date),
                totalWaitingTimes: groupedData.map(d => d.data.total_times.reduce((a, b) => a + b, 0)),
                waitingBeforeMeal: groupedData.map(d => d.data.waiting_times_before_meal.reduce((a, b) => a + b, 0))
            };
        }
        function getSelectedDateData(date) {
            let selectedData = groupedData.find(d => d.date === date);
            if (!selectedData) return null;

            return {
                totalTimeChunks: createChunks(selectedData.data.total_times, [10, 20, 30, 100]),
                beforeMealChunks: createChunks(selectedData.data.waiting_times_before_meal, [5, 10, 15, 20, 100])
            };
        }
        function updateCharts(date = null) {
            selectedDate = date;

            if (!date) {
                let { dates, totalWaitingTimes, waitingBeforeMeal } = getAggregatedData();
                barChart.data.labels = dates;
                barChart.data.datasets[0].data = totalWaitingTimes;
                barChart.data.datasets[0].label = "Total Waiting Time (All Dates)";
                barChart.update();

                pieChart.data.labels = dates;
                pieChart.data.datasets[0].data = waitingBeforeMeal;
                pieChart.data.datasets[0].label = "Waiting Times Before Meal (All Dates)";
                pieChart.update();
            } else {
                // Selected date view
                let selectedData = getSelectedDateData(date);
                if (!selectedData) {
                    console.error("❌ No data found for selected date:", date);
                    return;
                }

                let { totalTimeChunks, beforeMealChunks } = selectedData;

                barChart.data.labels = ["1-10", "10-20", "20-30", "30+"];
                barChart.data.datasets[0].data = totalTimeChunks;
                barChart.data.datasets[0].label = `Total Waiting Time (${date})`;
                barChart.update();

                pieChart.data.labels = ["0-5", "5-10", "10-15", "15-20", "20+"];
                pieChart.data.datasets[0].data = beforeMealChunks;
                pieChart.data.datasets[0].label = `Waiting Times Before Meal (${date})`;
                pieChart.update();
            }
        }
        barChart = new Chart(ctx1, {
            type: "bar",
            data: {
                labels: [],
                datasets: [{
                    label: "",
                    data: [],
                    backgroundColor: "#5B4B8A"
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        beginAtZero: true
                    },
                    y: {
                        beginAtZero: true
                    }
                },
                onHover: (event, chartElements) => {
                },
                onClick: (event, elements) => {
                    if (elements.length > 0) {
                        let clickedIndex = elements[0].index;
                        let clickedDate = barChart.data.labels[clickedIndex];
                        updateCharts(clickedDate);
                    }
                }
            }
        });
        pieChart = new Chart(ctx2, {
            type: "pie",
            data: {
                labels: [],
                datasets: [{
                    label: "",
                    data: [],
                    backgroundColor:  ["#FFB400", "#FF5733", "#17A589", "#3498DB", "#E74C3C"]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right'
                    }
                }
            }
        });
        document.addEventListener("click", function (event) {
            if (!canvas1.contains(event.target) && !canvas2.contains(event.target)) {
                console.log("🔄 Resetting to default view...");
                updateCharts(null);
            }
        });
        updateCharts();

    } catch (error) {
        console.error("🚨 Error:", error);
    }
});
