function togglePasswordVisibility() {
    const passwordInput = document.getElementById('floatingPassword');
    const togglePassword = document.getElementById('togglePassword');

    // Check if checkbox is checked or not and toggle input type
    if (togglePassword.checked) {
        passwordInput.type = 'text'; // Show password
    } else {
        passwordInput.type = 'password'; // Hide password
    }
}