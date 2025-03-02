document.addEventListener("DOMContentLoaded", function() {
    const uploadStatus = document.getElementById('upload-status');

    uploadStatus.style.display = 'none';  // Ensures upload status is hidden initially

    // Initialize Lottie animation
    var animation = lottie.loadAnimation({
        container: document.getElementById('lottie-animation'), // Animation container
        renderer: 'svg',  // Render as SVG
        loop: true,       // Loop the animation
        autoplay: true,   // Start automatically
        path: document.getElementById('lottie-animation').getAttribute('data-animation-path') // Get animation path from data-attribute
    });

    // Dynamically adjust the size of the Lottie animation
    function resizeLottieAnimation() {
        const lottieContainer = document.getElementById('lottie-animation');
        lottieContainer.style.width = '50vw';  // Set the width to 50% of the viewport
        lottieContainer.style.height = 'auto'; // Height adjusts automatically
    }

    // Adjust Lottie animation size on window load or resize
    window.addEventListener('resize', resizeLottieAnimation);
    window.addEventListener('load', resizeLottieAnimation);

    // Event listener for file input
    document.getElementById('videoInput').addEventListener('change', function(event) {
        const files = event.target.files;

        if (files.length > 0) {
            // Show the overlay animation
            document.getElementById('overlay').classList.add('show');

            // Automatically submit the form to upload the file
            document.getElementById('video-upload-form').submit();

            // Disable the "Choose videos" button while uploading
            document.querySelector('.custom-file-input').style.pointerEvents = 'none';
        } else {
            alert("Please select a video file.");
        }
    });

    // Event listener for form submission (uploading the video)
    document.getElementById('video-upload-form').addEventListener('submit', function(event) {
        event.preventDefault();  // Prevent default form submission

        var formData = new FormData(event.target);
        var files = document.getElementById('videoInput').files;

        if (files.length === 0) {
            alert("Please select at least one video to upload.");
            return;
        }

        // Create XMLHttpRequest to upload files asynchronously
        var xhr = new XMLHttpRequest();
        xhr.open("POST", event.target.action, true);

        xhr.onload = function() {
            // Hide the overlay animation after upload
            document.getElementById('overlay').classList.remove('show');

            if (xhr.status === 200) {
                // Display upload status and show "Next" button
                uploadStatus.innerText = "Upload Complete! You can now proceed.";
                uploadStatus.style.display = 'block'; // Show the upload status message

            } else {
                alert("Upload failed, please try again.");
            }
        };

        // Show progress bar (optional, for better user experience)
        xhr.upload.onprogress = function(event) {
            if (event.lengthComputable) {
                var percent = (event.loaded / event.total) * 100;
                console.log('Upload progress: ' + percent + '%');
            }
        };

        // Append files to FormData object and send it to the server
        for (var i = 0; i < files.length; i++) {
            formData.append('videos', files[i]);
        }

        // Send the FormData (including files)
        xhr.send(formData);
    });
});
