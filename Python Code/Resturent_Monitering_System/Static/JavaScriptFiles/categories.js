document.addEventListener("DOMContentLoaded", function () {
    const images = document.querySelectorAll('.image-item');
    let currentIndex = 0; 
    const totalImages = images.length;
    let isTransitioning = false; 
    let scrollTimeout; 

    // Initially show the first three images
    function showInitialImages() {
        images.forEach((image, index) => {
            if (index < 3) {
                image.style.display = 'block'; 
                image.style.opacity = '1';
            } else {
                image.style.display = 'none'; 
            }
        });
    }

    showInitialImages();

    function updateImagePositions(direction) {
        if (isTransitioning) return; 
        isTransitioning = true;

        images.forEach((image) => {
            image.style.display = 'none'; 
            image.style.transition = 'none'; 
            image.style.opacity = '0';
            image.classList.remove('center', 'top-right', 'bottom-right'); 
        });

        setTimeout(() => {
            const centerIndex = currentIndex;
            const topRightIndex = (currentIndex + 1) % totalImages;
            const bottomRightIndex = (currentIndex + 2) % totalImages;
            images[centerIndex].style.display = 'block';
            images[topRightIndex].style.display = 'block';
            images[bottomRightIndex].style.display = 'block';

            images[centerIndex].classList.add('center');
            images[topRightIndex].classList.add('top-right');
            images[bottomRightIndex].classList.add('bottom-right');

            setTimeout(() => {
                images[centerIndex].style.transition = 'opacity 0.15s linear'; 
                images[topRightIndex].style.transition = 'opacity 0.15s linear'; 
                images[bottomRightIndex].style.transition = 'opacity 0.15s linear';

                images[centerIndex].style.opacity = '1'; 
                images[topRightIndex].style.opacity = '0.35'; 
                images[bottomRightIndex].style.opacity = '0.35'; 
            }, 50); 

            if (direction === 'down') {
                currentIndex = (currentIndex + 1) % totalImages; 
            } else {
                currentIndex = (currentIndex - 1 + totalImages) % totalImages; 
            }

            setTimeout(() => {
                isTransitioning = false; 
            }, 250); 

        }, 50); 
    }

    // Prevent scrolling on the page
    function preventScroll(event) {
        event.preventDefault();
    }

    // Handle mouse wheel events
    function handleScroll(event) {
        event.preventDefault(); 
        clearTimeout(scrollTimeout); 
        scrollTimeout = setTimeout(() => {
            const scrollDirection = event.deltaY > 0 ? 'down' : 'up'; 
            updateImagePositions(scrollDirection); 
        }, 50); 
    }

    // Prevent default action on all keys
    function handleKeyDown(event) {
        event.preventDefault(); // Prevent all key defaults
    }

    // Add event listeners
    window.addEventListener('wheel', handleScroll, { passive: false });
    window.addEventListener('scroll', preventScroll, { passive: false }); // Prevent page scrolling
    window.addEventListener('keydown', handleKeyDown); // Prevent all key default actions

    updateImagePositions('down'); 
});
