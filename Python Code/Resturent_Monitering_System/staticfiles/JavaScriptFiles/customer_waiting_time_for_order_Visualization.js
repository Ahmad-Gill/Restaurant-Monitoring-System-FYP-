document.addEventListener("DOMContentLoaded", function () {
    try {
        // Retrieve JSON data from the hidden div
        let groupedDataElement = document.getElementById("groupedData");
        let jsonData = groupedDataElement.getAttribute("data-value");
        let groupedData = JSON.parse(jsonData); // Convert to JavaScript object

        console.log("🔍 Full JSON Data:", groupedData); // Debugging

        // Select all date elements
        let dateLinks = document.querySelectorAll(".date-link");

        dateLinks.forEach(link => {
            link.addEventListener("click", function (event) {
                event.preventDefault(); // Prevent default anchor action

                // Get selected date
                let selectedDate = this.textContent.trim();

                // Highlight selected date
                dateLinks.forEach(l => l.classList.remove("selected"));
                this.classList.add("selected");

                // Find selected date data
                let selectedData = groupedData.find(entry => entry.date === selectedDate);

                if (selectedData) {
                    console.log("📅 Selected Date Data:", JSON.stringify(selectedData, null, 2)); // Print JSON
                } else {
                    console.log("❌ No data found for this date.");
                }
            });
        });
    } catch (error) {
        console.error("🚨 JSON Parsing Error:", error);
    }
});
