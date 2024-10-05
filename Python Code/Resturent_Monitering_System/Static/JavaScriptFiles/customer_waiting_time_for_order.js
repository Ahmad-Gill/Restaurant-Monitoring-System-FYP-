document.addEventListener("DOMContentLoaded", function() {
    const waitingTimeElements = document.querySelectorAll('.waiting-time');

    waitingTimeElements.forEach(function(element) {
        const startTimeString = element.getAttribute('data-start');
        const endTimeString = element.getAttribute('data-end');

        // Convert to Date objects
        const startTime = new Date(startTimeString);
        const endTime = new Date(endTimeString);

        // Check if dates are valid
        if (!isNaN(startTime) && !isNaN(endTime)) {
            // Calculate waiting time
            const waitingTimeInSeconds = Math.floor((endTime - startTime) / 1000);
            const hours = Math.floor(waitingTimeInSeconds / 3600);
            const minutes = Math.floor((waitingTimeInSeconds % 3600) / 60);
            const seconds = waitingTimeInSeconds % 60;

            // Display waiting time
            element.textContent = `${hours}h ${minutes}m ${seconds}s`;
        } else {
            element.textContent = "Invalid time";
        }
    });
});