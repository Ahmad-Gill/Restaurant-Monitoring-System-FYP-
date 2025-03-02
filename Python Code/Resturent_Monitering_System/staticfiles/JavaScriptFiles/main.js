// Function to handle the typing effect
function typeEffect(element, text, speed, callback) {
    let i = 0;
    element.innerHTML = "";  // Clear any existing content before typing starts
    element.style.visibility = "visible"; 
    let interval = setInterval(function () {
        if (i < text.length) {
            element.innerHTML += text.charAt(i); // Add one character at a time
            i++;
        } else {
            clearInterval(interval); // Stop when all text is written
            if (callback) callback();  // Call the callback when typing is done
        }
    }, speed); // Speed at which characters are added (in milliseconds)
}

// Function to show the slider after text animation
function showSlider() {
    const sliderContainer = document.querySelector('.slider-container');
    sliderContainer.style.visibility = "visible"; // Make the slider visible
    sliderContainer.style.opacity = 1; // Fade in the slider
}

document.addEventListener("DOMContentLoaded", function() {
    const headline1 = document.getElementById("headline1");
    const headline2 = document.getElementById("headline2");
    const description = document.getElementById("description");

    // Get text content from HTML elements
    const headline1Text = headline1.textContent.trim(); 
    const headline2Text = headline2.textContent.trim(); 
    const descriptionText = description.textContent.trim(); 

    // Clear the initial content in the HTML before typing effect
    headline1.textContent = "";
    headline2.textContent = "";
    description.textContent = "";

    // Apply typing effect using the retrieved text
    typeEffect(headline1, headline1Text, 100); // 100ms per character
    setTimeout(() => {
        typeEffect(headline2, headline2Text, 50);
    }, 2000); // Delay for the second headline
    setTimeout(() => {
        typeEffect(description, descriptionText, 50);
    }, 4000); // Delay for the description

    // Show slider after text typing is done
    setTimeout(showSlider, 6500); // Adjust timing to match text completion
});



// ------------------------------Add A slider---------------------------------

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
    
            window.location.href = "/login/"; 
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
        sliderThumb.textContent = "Login";
        progressDisplay.textContent = "0%"; 
    }
});




$(document).ready(function(){
    $("#testimonial-slider").owlCarousel({
        items: 3, 
        loop: true,
        autoplay: true,
        autoplayTimeout: 5000,
        autoplayHoverPause: true,
        smartSpeed: 800,
        nav: true,
        dots: true,
        navText: ["<span class='owl-prev'>&lt;</span>", "<span class='owl-next'>&gt;</span>"]
    });
});

