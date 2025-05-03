// WSAA-project: Web Services and Applications.
// JAVASCRIPT for car-park space availability in Cork City.
// Author: Laura Lyons

document.addEventListener("DOMContentLoaded", function () {
    fetchCarParks();
    updateCurrentTime();
    setInterval(updateCurrentTime, 1000);
});

// Function to update the current time dynamically
function updateCurrentTime() {
    const now = new Date();
    document.getElementById("currentTime").innerText = now.toLocaleTimeString();
}

// Function to fetch car parks and populate dropdown menus
function fetchCarParks() {
    fetch("/api/car-parks")
        .then(response => response.json())
        .then(data => {
            populateDropdown("carParkDropdown", data);
            populateDropdown("updateCarParkDropdown", data);
            populateDropdown("deleteCarParkDropdown", data);
        })
        .catch(error => console.error("Error fetching car parks:", error));
}

// Utility function to populate dropdown menus
function populateDropdown(dropdownId, data) {
    const dropdown = document.getElementById(dropdownId);
    dropdown.innerHTML = '<option value="">Select a car park...</option>';
    data.forEach(carPark => {
        const option = document.createElement("option");
        option.value = carPark.id;
        option.textContent = carPark.name;
        dropdown.appendChild(option);
    });
}

// Function to check availability of free spaces
function checkFreeSpaces() {
    const selectedId = document.getElementById("carParkDropdown").value;
    if (!selectedId) {
        alert("Please select a car park.");
        return;
    }

    fetch(`/api/parking-availability?id=${selectedId}`)
        .then(response => response.json())
        .then(data => {
            const resultContainer = document.getElementById("checkFreeSpaces");
            resultContainer.classList.remove("d-none", "alert-danger", "alert-success");
            
            if (data.free_spaces > 0) {
                resultContainer.textContent = `Available: ${data.free_spaces} free spaces.`;
                resultContainer.classList.add("alert-success");
            } else {
                resultContainer.textContent = "No free spaces available.";
                resultContainer.classList.add("alert-danger");
            }
        })
        .catch(error => console.error("Error checking spaces:", error));
}

// Function to add a new car park
function addCarPark() {
    const name = document.getElementById("newCarParkName").value;
    if (!name.trim()) {
        alert("Please enter a car park name.");
        return;
    }

    fetch("/api/car-parks", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({name})
    })
    .then(response => response.json())
    .then(() => {
        fetchCarParks(); // Refresh dropdowns
        document.getElementById("newCarParkName").value = "";
    })
    .catch(error => console.error("Error adding car park:", error));
}

// Function to update a car park
function updateCarPark() {
    const id = document.getElementById("updateCarParkDropdown").value;
    const newName = document.getElementById("updateCarParkName").value;

    if (!id || !newName.trim()) {
        alert("Please select a car park and enter a new name.");
        return;
    }

    fetch(`/api/car-parks/${id}`, {
        method: "PUT",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({name: newName})
    })
    .then(response => response.json())
    .then(() => {
        fetchCarParks(); // Refresh dropdowns
        document.getElementById("updateCarParkName").value = "";
    })
    .catch(error => console.error("Error updating car park:", error));
}

// Function to delete a car park
function deleteCarPark() {
    const id = document.getElementById("deleteCarParkDropdown").value;
    if (!id) {
        alert("Please select a car park to delete.");
        return;
    }

    fetch(`/api/car-parks/${id}`, {method: "DELETE"})
    .then(response => response.json())
    .then(() => fetchCarParks()) // Refresh dropdowns after deletion
    .catch(error => console.error("Error deleting car park:", error));
}

