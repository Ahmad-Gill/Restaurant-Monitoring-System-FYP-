document.addEventListener("DOMContentLoaded", function() {

    const logo = document.querySelector('.logo img'); // Select the img inside the logo class
    if (logo) {
        logo.classList.add('rotate');
    } else {
        console.error("Logo not found!");
    }
});
