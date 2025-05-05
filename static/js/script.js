// WSAA-project: Web Services and Applications.
// JAVASCRIPT for car-park space availability in Cork City.
// Author: Laura Lyons

// Drop down car park menu and associated space availability.
document.addEventListener("DOMContentLoaded", async function () {
    await fetchCarParks(); // ✅ Fetch car park data and populate dropdowns
    updateCurrentTime();
    setInterval(updateCurrentTime, 1000);

    function showForm(formId) {
        console.log(`🔍 Showing form: ${formId}`); // Debugging output

        // ✅ Hide all forms first
        document.getElementById("addCarParkForm").classList.add("d-none");
        document.getElementById("updateCarParkForm").classList.add("d-none");
        document.getElementById("deleteCarParkForm").classList.add("d-none");

        // Show the selected form
        document.getElementById(formId).classList.remove("d-none");
    }

    // ✅ Attach event listeners to buttons
    document.getElementById("addCarParkButton").addEventListener("click", function () {
        showForm("addCarParkForm");
    });

    document.getElementById("updateCarParkButton").addEventListener("click", function () {
        showForm("updateCarParkForm");
    });

    document.getElementById("deleteCarParkButton").addEventListener("click", function () {
        showForm("deleteCarParkForm");
    });

    // ✅ Attach logic for handling car park selection changes
    document.getElementById("carParkDropdown").addEventListener("change", async function () {
        const selectedId = this.value;
        const resultContainer = document.getElementById("checkFreeSpaces");

        // Hide previous results
        document.getElementById("openingHoursResult").classList.add("d-none");
        document.getElementById("openingHoursContent").innerHTML = "";
        document.getElementById("heightRestrictionNotice").classList.add("d-none");
        document.getElementById("heightRestrictionContent").innerHTML = "";
        
        if (!selectedId) {
            resultContainer.classList.add("d-none");
            resultContainer.innerText = "";
            return;
        }

        try {
            const response = await fetch(`/api/car-parks/${selectedId}`);  
            if (!response.ok) throw new Error(`❌ Server Error: ${response.status} ${response.statusText}`);

            const carPark = await response.json();
            console.log("🔍 Live free spaces:", carPark.free_spaces);

            resultContainer.classList.remove("d-none");
            resultContainer.className = "alert mt-3";

            if (carPark.free_spaces === "Closed") {
                resultContainer.innerText = "This car park is closed.";
                resultContainer.classList.add("alert-warning");
            } else if (parseInt(carPark.free_spaces) > 0) {
                resultContainer.innerText = `Yes, ${carPark.free_spaces} free spaces available.`;
                resultContainer.classList.add("alert-success");
            } else {
                resultContainer.innerText = "No, the car park is full.";
                resultContainer.classList.add("alert-danger");
            }
        } catch (error) {
            console.error("❌ Error fetching availability:", error);
            resultContainer.innerText = "No live data available.";
        }
    });
});


// Opening Hours
document.addEventListener("DOMContentLoaded", function () {
    const showOpeningHoursBtn = document.getElementById("toggleOpeningHoursBtn");
    const openingHoursContainer = document.getElementById("openingHoursContent");
    const openingHoursResult = document.getElementById("openingHoursResult");

    if (!showOpeningHoursBtn) {
        console.error("❌ 'Show Opening Hours' button not found.");
        return;
    }

    showOpeningHoursBtn.addEventListener("click", async function () {
        console.log("✅ 'Show Opening Hours' button clicked!");

        const selectedId = document.getElementById("carParkDropdown").value;
        if (!selectedId) {
            openingHoursContainer.innerHTML = "<p>Please select a car park first.</p>";
            openingHoursResult.classList.remove("d-none");
            return;
        }

        try {
            console.log(`🔍 Fetching opening hours for Car Park ID ${selectedId}...`);
            const response = await fetch(`/api/opening-hours/${selectedId}`);
            if (!response.ok) throw new Error(`❌ Server Error: ${response.status}`);

            const todayHours = await response.json();
            console.log("✅ API Response:", todayHours);

            openingHoursContainer.innerHTML = todayHours.message
                ? `<p>${todayHours.message}</p>`
                : `<p><strong>${todayHours.day}:</strong> ${todayHours.opening_time || "N/A"} - ${todayHours.closing_time || "N/A"}</p>`;

            openingHoursResult.classList.remove("d-none"); // ✅ Make visible

        } catch (error) {
            console.error("❌ Error fetching opening hours:", error);
            openingHoursContainer.innerHTML = "<p>No data available.</p>";
            openingHoursResult.classList.remove("d-none");
        }
    });
});

// Height Restrictions
document.addEventListener("DOMContentLoaded", function () {
    const showHeightRestrictionBtn = document.getElementById("toggleHeightRestrictionBtn");
    const heightRestrictionContainer = document.getElementById("heightRestrictionContent");
    const heightRestrictionNotice = document.getElementById("heightRestrictionNotice");

    if (!showHeightRestrictionBtn) {
        console.error("❌ 'Car Park Height Restriction' button not found.");
        return;
    }

    showHeightRestrictionBtn.addEventListener("click", async function () {
        console.log("✅ 'Car Park Height Restriction' button clicked!");

        const selectedId = document.getElementById("carParkDropdown").value;
        if (!selectedId) {
            heightRestrictionContainer.innerHTML = "<p>Please select a car park first.</p>";
            heightRestrictionNotice.classList.remove("d-none");
            return;
        }

        try {
            console.log(`🔍 Fetching height restriction for Car Park ID ${selectedId}...`);
            const response = await fetch(`/api/height-restriction/${selectedId}`);
            if (!response.ok) throw new Error(`❌ Server Error: ${response.status}`);

            const restrictionData = await response.json();
            console.log("✅ API Response:", restrictionData);

            heightRestrictionContainer.innerHTML = restrictionData.height_restriction
                ? `<p><strong>Height Restriction:</strong> ${restrictionData.height_restriction}m</p>`
                : `<p>${restrictionData.message}</p>`;

            heightRestrictionNotice.classList.remove("d-none"); // ✅ Make visible

        } catch (error) {
            console.error("❌ Error fetching height restriction:", error);
            heightRestrictionContainer.innerHTML = "<p>No data available.</p>";
            heightRestrictionNotice.classList.remove("d-none");
        }
    });
});

// Function to update current time dynamically
function updateCurrentTime() {
    document.getElementById('currentTime').innerText = new Date().toLocaleTimeString("en-GB", { hour12: false });
}

// Function to show the form for adding a car park
document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ DOM fully loaded, adding event listeners...");
    console.log("🔍 Checking if button exists:", document.getElementById("addCarParkButton")); // ✅ Debugging line

    const addCarParkButton = document.getElementById("addCarParkButton");
    if (addCarParkButton) {
        addCarParkButton.addEventListener("click", function () {
            console.log("✅ Add Car Park button clicked!");
            showForm("addCarParkForm");
        });
    } else {
        console.error("❌ Button ID 'addCarParkButton' not found in HTML.");
    }
});

// Fetch car parks and populate dropdowns
async function fetchCarParks() {
    try {
        const response = await fetch("/api/car-parks");
        if (!response.ok) throw new Error(`Server Error: ${response.status} ${response.statusText}`);

        const data = await response.json();
        console.log("API response received:", data);

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
            option.value = park.id;
            option.innerText = park.name;
            dropdown.appendChild(option);
        });

        console.log(`Populated ${dropdownId} with ${parkingData.length} car parks.`);
    });
}

// Function to update car park details
async function addCarPark() {
    const carParkName = document.getElementById("newCarParkName").value;
    const heightRestriction = document.getElementById("newCarParkHeight").value;
    const openingTime = document.getElementById("newOpeningTime").value;
    const closingTime = document.getElementById("newClosingTime").value;
    const is24Hours = document.getElementById("is24Hours").checked; // ✅ Checkbox

    if (!carParkName) {
        alert("Please enter a car park name.");
        return;
    }

    try {
        const response = await fetch('/api/add-car-park', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                name: carParkName,
                height_restriction: heightRestriction,
                opening_time: openingTime,
                closing_time: closingTime,
                is_24_hours: is24Hours
            })
        });

        const result = await response.json();
        alert(result.message);
    } catch (error) {
        console.error("❌ Error adding car park:", error);
    }
}


//
async function addOpeningHours(carParkId) {
    const openingTime = document.getElementById("newOpeningTime").value;
    const closingTime = document.getElementById("newClosingTime").value;
    const is24Hours = document.getElementById("is24Hours").checked;

    try {
        await fetch('/api/add-opening-hours', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ car_park_id: carParkId, opening_time: openingTime, closing_time: closingTime, is_24_hours: is24Hours })
        });

        alert("Opening hours added!");

        // ✅ Refresh dropdowns after updating opening hours
        const updatedResponse = await fetch('/api/get-car-parks');
        const updatedParkingData = await updatedResponse.json();
        populateDropdown(["carParkDropdown"], updatedParkingData);

    } catch (error) {
        console.error("❌ Error adding opening hours:", error);
    }
}


