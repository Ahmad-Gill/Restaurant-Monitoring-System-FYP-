document.addEventListener("DOMContentLoaded", function () {
    const images = document.querySelectorAll('.image-item');
    let currentIndex = 0;
    const totalImages = images.length;
    let isTransitioning = false;
    let scrollTimeout;

    function isLargeScreen() {
        return window.innerWidth > 900;
    }

    function updateImagePositions(direction) {
        if (!isLargeScreen() || isTransitioning) return;
        isTransitioning = true;

        images.forEach((image) => {
            image.style.display = 'none';
            image.style.opacity = '0';
            image.classList.remove('center', 'top-right', 'bottom-right');
        });

        setTimeout(() => {
            const centerIndex = currentIndex;
            const topRightIndex = (currentIndex + 1) % totalImages;
            const bottomRightIndex = (currentIndex + 2) % totalImages;

            [centerIndex, topRightIndex, bottomRightIndex].forEach(index => {
                images[index].style.display = 'block';
            });

            images[centerIndex].classList.add('center');
            images[topRightIndex].classList.add('top-right');
            images[bottomRightIndex].classList.add('bottom-right');

            setTimeout(() => {
                images[centerIndex].style.opacity = '1';
                images[topRightIndex].style.opacity = '0.35';
                images[bottomRightIndex].style.opacity = '0.35';
            }, 50);

            currentIndex = direction === 'down'
                ? (currentIndex + 1) % totalImages
                : (currentIndex - 1 + totalImages) % totalImages;

            setTimeout(() => isTransitioning = false, 250);
        }, 50);
    }

    function handleScroll(event) {
        if (isLargeScreen()) {
            event.preventDefault();
            clearTimeout(scrollTimeout);
            scrollTimeout = setTimeout(() => {
                updateImagePositions(event.deltaY > 0 ? 'down' : 'up');
            }, 50);
        }
    }

    function applySettings() {
        if (isLargeScreen()) {
            window.addEventListener('wheel', handleScroll, { passive: false });
            updateImagePositions('down');
        } else {
            window.removeEventListener('wheel', handleScroll);
            images.forEach(image => {
                image.style.display = 'block';
                image.style.opacity = '1';
            });
        }
    }

    applySettings();
    window.addEventListener('resize', applySettings);
});
