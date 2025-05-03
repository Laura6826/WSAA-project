// WSAA-project: Web Services and Applications.
// JAVASCRIPT for car-park space availability in Cork City.
// Author: Laura Lyons

document.addEventListener("DOMContentLoaded", async function () {
    await populateDropdown(); // Populate dropdown with any existing local data
    updateCurrentTime();
    setInterval(updateCurrentTime, 1000);

    // Fetch latest parking availability from Flask API
    try {
        const response = await fetch("/api/car-parks");
        const data = await response.json();

        const dropdown = document.getElementById("carParkDropdown");
        dropdown.innerHTML = ""; // Clear previous data

        data.forEach(carPark => {
            const option = document.createElement("option");
            option.value = carPark.id;
            option.textContent = carPark.name;
            dropdown.appendChild(option);
        });
    } catch (error) {
        console.error("Error fetching car parks:", error);
    }
});

// Function to update the current time dynamically
function updateCurrentTime() {
    const now = new Date(); // Get the current date and time
    const hours = String(now.getHours()).padStart(2, '0'); // Format hours (24-hour format)
    const minutes = String(now.getMinutes()).padStart(2, '0'); // Format minutes
    const seconds = String(now.getSeconds()).padStart(2, '0'); // Format seconds
    const formattedTime = `${hours}:${minutes}:${seconds}`; // Combine into a time string
    document.getElementById('currentTime').innerText = formattedTime; // Update the content of span
}

// Call the function immediately and then every second
updateCurrentTime(); // Initialize the time display
setInterval(updateCurrentTime, 1000); // Update every second

// Get Current Day Name
function getCurrentDayName() {
    const dayIndex = new Date().getDay(); // 0 = Sunday, 1 = Monday, etc.
    const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
    return days[dayIndex];
}

// Function to fetch car parks and populate dropdown menus
function fetchCarParks() {
    fetch("/api/car-parks")
        .then(response => response.json())
        .then(data => {
            console.log("✅ API response received:", data); // Debugging step
            document.getElementById("debugOutput").innerText = JSON.stringify(data, null, 2); // ✅ Show API data on the webpage
            populateDropdown("carParkDropdown", data);
            populateDropdown("updateCarParkDropdown", data);
            populateDropdown("deleteCarParkDropdown", data);
        })
        .catch(error => {
            console.error("❌ Error fetching car parks:", error);
            document.getElementById("debugOutput").innerText = "❌ Error fetching car parks: " + error; // ✅ Show errors on the webpage
        });
}

// Initial fetch to populate dropdowns
async function fetchParkingData() {
    return fetch("/api/car-parks")
        .then(response => {
            if (!response.ok) {
                throw new Error(`❌ Server Error: ${response.status} ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("✅ API response received:", data);
            return data;
        })
        .catch(error => {
            console.error("❌ Error fetching parking data:", error);
            return []; // Return empty array to prevent further errors
        });
}


// Utility function to populate dropdown menus
async function populateDropdown() {
    const parkingData = await fetchParkingData(); // Get data from the live API
    console.log("Populating dropdown with parking data:", parkingData); // Debugging

    const dropdown = document.getElementById("carParkDropdown");
    dropdown.innerHTML = '<option value="">Select Car Park</option>'; // Default option

    if (!parkingData || parkingData.length === 0) {
        dropdown.innerHTML += '<option disabled>No car parks available</option>';
        return;
    }

    parkingData.forEach(park => {
        const option = document.createElement("option");
        option.value = park.id;  // Ensure 'id' is used correctly for selection
        option.dataset.freeSpaces = park.free_spaces || "0"; // Dynamically set free spaces
        option.innerText = park.name || "Unnamed Car Park";
        dropdown.appendChild(option);
    });
}

// Function to check availability of free spaces
async function checkFreeSpaces() {
    const parkingData = await fetchParkingData(); // Fetch live data
    console.log("Checking parking availability:", parkingData); // Debugging

    const dropdown = document.getElementById("carParkDropdown");
    const selectedId = dropdown.value; // Get selected car park ID

    if (!selectedId) {
        console.error("No valid selection.");
        return;
    }

    const selectedCarPark = parkingData.find(park => park.id == selectedId);
    console.log("Matched car park from live data:", selectedCarPark); // Debugging

    if (!selectedCarPark) {
        console.error("Car park not found in live data.");
        return;
    }

    const freeSpaces = parseInt(selectedCarPark.free_spaces) || 0;
    console.log("Free spaces available:", freeSpaces); // Debugging

    const resultContainer = document.getElementById("checkFreeSpaces");
    resultContainer.className = "alert mt-3"; // Reset classes
    if (freeSpaces > 0) {
        resultContainer.innerText = `Yes, there are ${freeSpaces} free spaces available.`;
        resultContainer.classList.add("alert-success");
    } else {
        resultContainer.innerText = "No, the car park is full.";
        resultContainer.classList.add("alert-danger");
    }
    resultContainer.classList.remove("d-none");
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

