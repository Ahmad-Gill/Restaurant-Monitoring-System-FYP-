document.addEventListener("DOMContentLoaded", function() {
    const waitingTimeElements = document.querySelectorAll('.total_time');

    waitingTimeElements.forEach(function(element) {
        const timeBeforeMeal = parseFloat(element.getAttribute('time_before_meal'));
        const totalTime = parseFloat(element.getAttribute('total_time'));

        if (!isNaN(timeBeforeMeal) && !isNaN(totalTime)) {
            // Convert totalTime from minutes to hours, minutes, seconds
            const totalSeconds = Math.floor(totalTime * 60); 
            const hours = Math.floor(totalSeconds / 3600);
            const minutes = Math.floor((totalSeconds % 3600) / 60);
            const seconds = totalSeconds % 60;

            element.textContent = `${hours}h ${minutes}m ${seconds}s`;
        } else {
            element.textContent = "Invalid time";
        }
    });
});
