document.addEventListener('DOMContentLoaded', function () {
    let gridNumbers = []; // Array to hold the entered grid numbers

    // DOM Elements
    const form = document.querySelector("form");
    const overlay = document.getElementById("overlay");
    const gridInputField = document.getElementById("gridInput");
    const addGridBtn = document.getElementById("addGridBtn");
    const gridList = document.getElementById("gridList");
    const submitSection = document.getElementById("submitSection");
    const submitGridsBtn = document.getElementById("submitGridsBtn");

    // Inline styles for buttons
    const editButtonStyle = {
        backgroundColor: '#4CAF50',
        color: 'white',
        border: 'none',
        padding: '5px 10px',
        marginLeft: '10px',
        cursor: 'pointer',
        borderRadius: '5px',
    };

    const deleteButtonStyle = {
        backgroundColor: '#f44336',
        color: 'white',
        border: 'none',
        padding: '5px 10px',
        marginLeft: '5px',
        cursor: 'pointer',
        borderRadius: '5px',
    };

    // Show loading animation during form submission
    if (form && overlay) {
        form.onsubmit = function (event) {
            event.preventDefault();
            overlay.style.display = 'block'; // Show overlay
            form.submit(); // Proceed with form submission
        };
    }

    // Handle grid-related functionality
    if (gridInputField && addGridBtn && gridList && submitSection && submitGridsBtn) {
        // Add grid number to the list
        addGridBtn.addEventListener("click", function () {
            const gridNumber = gridInputField.value.trim();

            if (gridNumber === '0') {
                finalizeGridInput();
                return;
            }

            if (!validateGridInput(gridNumber)) {
                return;
            }

            gridNumbers.push(gridNumber);
            displayGrids();
            gridInputField.value = ''; // Clear input field
        });

        // Finalize input when '0' is entered
        function finalizeGridInput() {
            gridInputField.disabled = true;
            addGridBtn.disabled = true;
            submitSection.style.display = 'block'; // Show submit section after '0' is entered
            gridInputField.value = ''; // Clear input field
        }

        // Validate grid input
        function validateGridInput(gridNumber) {
            if (!gridNumber || gridNumber <= 0 || gridNumbers.includes(gridNumber)) {
                alert("Please enter a unique, valid grid number greater than 0.");
                return false;
            }
            return true;
        }

        // Display the grid list
        function displayGrids() {
            gridList.innerHTML = ''; // Clear the list

            gridNumbers.forEach((grid, index) => {
                const listItem = document.createElement("li");
                listItem.textContent = `Grid ${grid}`;
            
                // Add edit and delete buttons
                listItem.appendChild(createEditButton(index));
                listItem.appendChild(createDeleteButton(index));
            
                // Add spacing between list items
                listItem.style.marginBottom = '10px'; // Adjust space as needed
                
                gridList.appendChild(listItem);
            });
            

            // Ensure submit section visibility based on grid numbers
            submitSection.style.display = gridNumbers.length > 0 ? 'none' : 'block'; // Hide submit section initially
        }

        // Create edit button with inline styles
        function createEditButton(index) {
            const editBtn = document.createElement("button");
            editBtn.textContent = "Edit";
            Object.assign(editBtn.style, editButtonStyle); // Apply styles
            editBtn.addEventListener("click", () => editGrid(index));
            return editBtn;
        }

        // Create delete button with inline styles
        function createDeleteButton(index) {
            const deleteBtn = document.createElement("button");
            deleteBtn.textContent = "Delete";
            Object.assign(deleteBtn.style, deleteButtonStyle); // Apply styles
            deleteBtn.addEventListener("click", () => deleteGrid(index));
            return deleteBtn;
        }

        // Edit grid number
        function editGrid(index) {
            const newGridValue = prompt("Enter a new grid number", gridNumbers[index]);
            if (validateGridInput(newGridValue)) {
                gridNumbers[index] = newGridValue;
                displayGrids();
            } else {
                alert("Invalid or duplicate grid number.");
            }
        }

        // Delete grid number
        function deleteGrid(index) {
            gridNumbers.splice(index, 1); // Remove grid
            displayGrids();
        }

        // Inline style for submit section
        submitSection.style.textAlign = 'center';
        submitSection.style.marginTop = '20px';
        submitSection.style.display = 'none'; // Initially hide submit section

        // Submit grids via AJAX
        submitGridsBtn.addEventListener("click", function () {
            if (gridNumbers.length === 0) {
                alert("No grids to submit.");
                return;
            }

            sendGridsToServer(gridNumbers);
        });

        // Send grids to the server
        function sendGridsToServer(grids) {
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            const xhr = new XMLHttpRequest();
            xhr.open("POST", "/preprocessing_1", true);
            xhr.setRequestHeader("X-CSRFToken", csrfToken);
            xhr.setRequestHeader("Content-Type", "application/json");

            xhr.onreadystatechange = function () {
                if (xhr.readyState === 4) {
                    overlay.style.display = 'none'; // Hide overlay
                    if (xhr.status === 200) {
                        alert("Grids submitted successfully!");
                        window.location.href = '/preprocessing_1';
                        gridNumbers = [];
                        displayGrids();
                    } else {
                        alert("Error submitting grids.");
                    }
                }
            };

            xhr.send(JSON.stringify({ grids })); // Send grid data
        }
    } else {
        console.error("Some grid-related elements are missing in the DOM.");
    }
});





