let frameNumber = 1;
    let maxFrames = 200; // Set a max number of frames you want to simulate
    let loadingMessageElement = document.getElementById("loading-message");
    let startButton = document.getElementById("start-button");
    let loadingMessageContainer = document.getElementById("loading-message-container");
    
    let totalFrames = maxFrames; // For calculating progress

    function startPreprocessing() {
        // Hide the button once clicked
        startButton.style.display = "none";

        // Show the loading message container
        loadingMessageContainer.style.display = "block";

        loadingMessageElement.innerHTML = "Starting preprocessing...";
        let interval = setInterval(function() {
            if (frameNumber <= maxFrames) {
                let progress = (frameNumber / totalFrames) * 100;
                let remainingTime = (maxFrames - frameNumber) * 100; // Assuming 10 seconds per frame
                
                loadingMessageElement.innerHTML += `
                    <br>Saving frame ${frameNumber}... 
                    Progress: ${Math.round(progress)}% 
                    | Estimated time remaining: ${remainingTime} seconds
                `;
                frameNumber++;
                loadingMessageContainer.scrollTop = loadingMessageContainer.scrollHeight; // Auto-scroll to the bottom
            } else {
                clearInterval(interval);
                loadingMessageElement.innerHTML += "<br>Preprocessing is complete! <br> Finalizing ...";
                loadingMessageContainer.scrollTop = loadingMessageContainer.scrollHeight; // Auto-scroll to the bottom
            }
        }, 10000); // Update every second
    }