document.addEventListener("DOMContentLoaded", function() {
    console.log("JavaScript file is loaded");
    const logo = document.querySelector('.logo img'); // Select the img inside the logo class
    if (logo) {
        console.log("Logo found:", logo);
        logo.classList.add('rotate');
    } else {
        console.error("Logo not found!");
    }
});
