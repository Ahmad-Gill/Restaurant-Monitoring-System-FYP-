// Function to show the login item and hide the sign-up item
function showLogin() {
    // Show login button and hide sign up button
    document.getElementById("loginButton").style.display = "none";
    document.getElementById("signUpButton").style.display = "inline-block";

    // Show the login item and hide the sign up item
    document.getElementById("loginItem").style.display = "block";
    document.getElementById("signUpItem").style.display = "none";

    document.getElementById("additionalText").innerHTML = "Switch to Ageneral  Pre Processing";
    // Change text content
    document.getElementById("leftTextContent").innerText = "Dress Code";
}

// Function to show the sign-up item and hide the login item
function showSignUp() {
    // Show sign up button and hide login button
    document.getElementById("signUpButton").style.display = "none";
    document.getElementById("loginButton").style.display = "inline-block";

    // Show the sign up item and hide the login item
    document.getElementById("signUpItem").style.display = "block";
    document.getElementById("loginItem").style.display = "none";

    // Change text content
    document.getElementById("additionalText").innerHTML = "Switch to Chef Dres Code Pre Processing";
    document.getElementById("leftTextContent").innerHTML = "<span class='analytics-text'>Analytics</span>";

}
