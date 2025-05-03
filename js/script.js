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

// Function to fetch car parks and populate the dropdown menu
function fetchCarParks() {
    fetch("/api/car-parks")
        .then(response => response.json())
        .then(data => {
            const dropdown = document.getElementById("carParkDropdown");
            dropdown.innerHTML = '<option value="">Select a car park...</option>';
            data.forEach(carPark => {
                const option = document.createElement("option");
                option.value = carPark.id;
                option.textContent = carPark.name;
                dropdown.appendChild(option);
            });
        })
        .catch(error => console.error("Error fetching car parks:", error));
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

    fetch("/api/car-parks", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({name})
    })
    .then(response => response.json())
    .then(() => {
        fetchCarParks(); // Refresh dropdown
        document.getElementById("newCarParkName").value = "";
    })
    .catch(error => console.error("Error adding car park:", error));
}
