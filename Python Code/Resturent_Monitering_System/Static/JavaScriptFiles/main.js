
// Add A slider

document.addEventListener('DOMContentLoaded', function () {
    const sliderThumb = document.getElementById('sliderThumb');
    const sliderTrack = document.querySelector('.slider-track');
    const sliderFill = document.getElementById('sliderFill'); 
    const progressDisplay = document.getElementById('progressDisplay'); 

    let isDragging = false;

    // For Mouse
    sliderThumb.addEventListener('mousedown', function () {
        isDragging = true;
    });

    // For Touchscreen
    sliderThumb.addEventListener('touchstart', function () {
        isDragging = true;
    });

    // Mouse Move Handler
    document.addEventListener('mousemove', function (e) {
        if (isDragging) {
            let newPosition = e.clientX - sliderTrack.getBoundingClientRect().left - (sliderThumb.offsetWidth / 2);
            updateSliderPosition(newPosition);
        }
    });

    // Touch Move Handler
    document.addEventListener('touchmove', function (e) {
        if (isDragging) {
            let newPosition = e.touches[0].clientX - sliderTrack.getBoundingClientRect().left - (sliderThumb.offsetWidth / 2);
            updateSliderPosition(newPosition);
        }
    });

    // End Dragging for Mouse
    document.addEventListener('mouseup', function () {
        if (isDragging) {
            resetSlider();
        }
    });

    // End Dragging for Touch
    document.addEventListener('touchend', function () {
        if (isDragging) {
            resetSlider();
        }
    });

    // Update slider position and show progress
    function updateSliderPosition(newPosition) {
        const maxPosition = sliderTrack.offsetWidth - sliderThumb.offsetWidth;

        if (newPosition < 0) {
            newPosition = 0;
        } else if (newPosition > maxPosition) {
            newPosition = maxPosition;
            window.location.href = "/categories/"; // Navigate to the categories page
        }

        sliderThumb.style.left = `${newPosition}px`;

        // Calculate progress as a percentage
        const progressPercentage = Math.round((newPosition / maxPosition) * 100);
        sliderFill.style.width = `${progressPercentage}%`; // Update the fill width
        if (progressPercentage > 1) {
            sliderThumb.textContent = `${progressPercentage}%`; // Update the thumb with percentage
        } else {
            sliderThumb.textContent = 'Start'; // Reset to 'Slide' when percentage is 1% or less
        }
        progressDisplay.textContent = `${progressPercentage}%`; // Update the progress display
    }

    // Reset slider position if it doesn't reach the end
    function resetSlider() {
        isDragging = false;
        sliderThumb.style.left = "0px"; 
        sliderFill.style.width = "0%"; 
        sliderThumb.textContent = "Start";
        progressDisplay.textContent = "0%"; 
    }
});

// add seffect on TExt Writing 


function typeEffect(element, text, speed) {
    let i = 0;
    element.innerHTML = "";  // Clear any existing content before typing starts
    element.style.visibility = "visible"; 
    let interval = setInterval(function () {
        if (i < text.length) {
            element.innerHTML += text.charAt(i); // Add one character at a time
            i++;
        } else {
            clearInterval(interval); // Stop when all text is written
        }
    }, speed); // Speed at which characters are added (in milliseconds)
}

document.addEventListener("DOMContentLoaded", function() {
    const headline1 = document.getElementById("headline1");
    const headline2 = document.getElementById("headline2");
    const description = document.getElementById("description");

    typeEffect(headline1, "Innovative Monitoring Awaits", 100); // 100ms per character
    setTimeout(() => {
        typeEffect(headline2, "Optimize Your Operations with Precision Monitoring", 50);
    }, 2000); // Delay to start the second headline
    setTimeout(() => {
        typeEffect(description, "Our system delivers real-time insights to streamline your restaurant’s efficiency.", 50);
    }, 4000); // Delay for the description
});
