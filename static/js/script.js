// WSAA-project: Web Services and Applications.
// JAVASCRIPT for car-park space availability in Cork City.
// Author: Laura Lyons

document.addEventListener("DOMContentLoaded", async function () {
    await fetchCarParks(); // Fetch car park data and populate dropdowns
    updateCurrentTime();
    setInterval(updateCurrentTime, 1000);
});

// Function to update current time dynamically
function updateCurrentTime() {
    document.getElementById('currentTime').innerText = new Date().toLocaleTimeString("en-GB", { hour12: false });
}

// Fetch car parks and populate dropdowns
async function fetchCarParks() {
    try {
        const response = await fetch("/api/car-parks");
        if (!response.ok) throw new Error(`Server Error: ${response.status} ${response.statusText}`);

        const data = await response.json();
        console.log("API response received:", data); // Debugging

        populateDropdown(["carParkDropdown", "updateCarParkDropdown", "deleteCarParkDropdown"], data);
    } catch (error) {
        console.error("Error fetching car park data:", error);
    }
}

// Function to populate multiple dropdowns dynamically
function populateDropdown(dropdownIds, parkingData) {
    dropdownIds.forEach(dropdownId => {
        const dropdown = document.getElementById(dropdownId);
        dropdown.innerHTML = '<option value="">Select Car Park</option>';

        if (!parkingData || parkingData.length === 0) {
            dropdown.innerHTML += '<option disabled>No car parks available</option>';
            console.error("❌ No car park data received.");
            return;
        }

        parkingData.forEach(park => {
            const option = document.createElement("option");
            option.value = park.id; // Set the ID for later retrieval
            option.innerText = park.name;
            dropdown.appendChild(option);
        });

        console.log(`Populated ${dropdownId} with ${parkingData.length} car parks.`);
    });
}

// Check availability of free spaces
function checkFreeSpaces() {
    const dropdown = document.getElementById("carParkDropdown");
    const selectedId = dropdown.value;
    
    if (!selectedId) {
        console.error("No valid selection.");
        return;
    }

    const freeSpaces = dropdown.options[dropdown.selectedIndex].dataset.freeSpaces;
    const resultContainer = document.getElementById("checkFreeSpaces");
    resultContainer.className = "alert mt-3";

    if (freeSpaces === "Closed") {
        resultContainer.innerText = "This car park is closed.";
        resultContainer.classList.add("alert-warning");
    } else if (parseInt(freeSpaces) > 0) {
        resultContainer.innerText = `Yes, ${freeSpaces} free spaces available.`;
        resultContainer.classList.add("alert-success");
    } else {
        resultContainer.innerText = "No, the car park is full.";
        resultContainer.classList.add("alert-danger");
    }
    resultContainer.classList.remove("d-none");
}

// Manage car park CRUD operations (Add, Update, Delete)
async function manageCarPark(action) {
    const id = document.getElementById(`${action}CarParkDropdown`)?.value;
    const name = document.getElementById(`${action}CarParkName`)?.value?.trim();

    if (action !== "delete" && (!id || !name)) {
        alert(`Please provide valid ${action} details.`);
        return;
    }

    const method = action === "delete" ? "DELETE" : (action === "add" ? "POST" : "PUT");
    const body = action !== "delete" ? JSON.stringify({ name }) : null;

    try {
        const response = await fetch(`/api/car-parks${action !== "add" ? "/" + id : ""}`, {
            method,
            headers: { "Content-Type": "application/json" },
            body
        });

        if (!response.ok) throw new Error(`Failed to ${action} car park. Status: ${response.status}`);
        console.log(`Car park ${action} successful`);

        await fetchCarParks(); // Refresh dropdowns
        if (name) document.getElementById(`${action}CarParkName`).value = "";
    } catch (error) {
        console.error(`Error ${action}ing car park:`, error);
    }
}


