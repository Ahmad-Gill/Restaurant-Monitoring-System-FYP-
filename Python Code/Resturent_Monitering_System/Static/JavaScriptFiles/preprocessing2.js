document.addEventListener("DOMContentLoaded", () => {
    const startButton = document.getElementById("start-preprocessing");
    const overlay = document.getElementById("overlay");
    const lottieContainer = document.getElementById("lottie-container");

    console.log("DOM loaded, script running...");

    if (startButton) {
        console.log("Start Button found.");
        startButton.addEventListener("click", () => {
            console.log("Start button clicked");

            // Show the overlay
            overlay.style.display = "block";
            console.log("Overlay visible");

            // Load the Lottie animation
            const animation = lottie.loadAnimation({
                container: lottieContainer,  // The container where the animation will be shown
                renderer: 'svg',  // Render the animation as SVG
                loop: true,       // Keep the animation looping
                autoplay: true,   // Start the animation as soon as it's loaded
                path: '{% static "Animation/animation1.json" %}'  // Path to your Lottie JSON file
            });

            console.log("Lottie animation loaded.");
        });
    } else {
        console.log("Start button not found.");
    }
});
