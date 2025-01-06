document.addEventListener("DOMContentLoaded", function() {
    const overlay = document.getElementById('overlay');
    const startButton = document.getElementById('start-preprocessing');
    const uploadStatus = document.getElementById('upload-status');

    // Initially hide the upload status
    uploadStatus.style.display = 'none';

    // Initialize Lottie animation (but do not show it yet)
    var animation = lottie.loadAnimation({
        container: document.getElementById('lottie-animation'), // Animation container
        renderer: 'svg',  // Render as SVG
        loop: true,       // Loop the animation
        autoplay: true,   // Start automatically
        path: document.getElementById('lottie-animation').getAttribute('data-animation-path') // Animation path
    });

    // Event listener for "Start Preprocessing" button
    startButton.addEventListener('click', function() {
        // Show the overlay with animation
        overlay.style.display = 'block';

        // Simulate sending a request to the server to start preprocessing
        fetch("{% url 'start_preprocessing' %}", {
            method: "POST",
            headers: {
                "X-CSRFToken": "{{ csrf_token }}",
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ action: "start" })
        })
        .then(response => response.json())
        .then(data => {
            if (data.preprocessing === true) {
                // Hide the overlay and show the status when preprocessing is done
                overlay.style.display = 'none';
                alert("Preprocessing completed!");
                location.reload();  // Optionally reload the page to reflect the updated state
            }
        })
        .catch(error => {
            console.error("Error during preprocessing:", error);
            alert("An error occurred.");
        });
    });
});


document.addEventListener("DOMContentLoaded", function () {
    const startButton = document.getElementById("start-preprocessing");
    const overlay = document.getElementById("overlay");

    // Check if preprocessing is already complete (via context from the backend)
    const preprocessingComplete = "{{ preprocessing|yesno:'true,false' }}" === "true";

    if (preprocessingComplete) {
        startButton.style.display = "none"; // Hide the "Start Preprocessing" button
    } else {
        overlay.style.display = "none"; // Ensure overlay is hidden initially
    }

    // Handle "Start Preprocessing" button click
    startButton.addEventListener("click", function () {
        startButton.style.display = "none"; // Hide the button
        overlay.style.display = "block"; // Show the overlay

        // Simulate preprocessing with a timeout (replace this with actual backend call if needed)
        setTimeout(() => {
            overlay.style.display = "none"; // Hide the overlay when done
            location.reload(); // Reload the page to show the Exit Preprocessing button
        }, 10000); // Example delay of 10 seconds
    });
});
