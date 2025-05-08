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
                rresultContainer.innerText = "There is no verified data on space availability for this car park.";
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

            let heightFormatted = restrictionData.height_restriction.replace("mm", "m"); // ✅ Corrects unit label

            heightRestrictionContainer.innerHTML = restrictionData.height_restriction
                ? `<p><strong>Height Restriction:</strong> ${heightFormatted}</p>`
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
        const carParks = await response.json();

        const dropdown = document.getElementById("carParkDropdown");
        dropdown.innerHTML = '<option value="">Select Car Park</option>'; // ✅ Clear old options

        carParks.forEach(carPark => {
            const option = document.createElement("option");
            option.value = carPark.id;
            option.textContent = carPark.name;
            dropdown.appendChild(option);
        });

        console.log("✅ Dropdown updated with new car park list!");

    } catch (error) {
        console.error("❌ Error fetching car parks:", error);
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

async function addCarPark() {
    const carParkName = document.getElementById("carParkName").value;
    const heightRestriction = document.getElementById("heightRestriction").value;
    const is24Hours = document.getElementById("is24Hours").checked;

    const openingHours = {
        "Monday": [document.getElementById("monday_open").value, document.getElementById("monday_close").value],
        "Tuesday": [document.getElementById("tuesday_open").value, document.getElementById("tuesday_close").value],
        "Wednesday": [document.getElementById("wednesday_open").value, document.getElementById("wednesday_close").value],
        "Thursday": [document.getElementById("thursday_open").value, document.getElementById("thursday_close").value],
        "Friday": [document.getElementById("friday_open").value, document.getElementById("friday_close").value],
        "Saturday": [document.getElementById("saturday_open").value, document.getElementById("saturday_close").value],
        "Sunday": [document.getElementById("sunday_open").value, document.getElementById("sunday_close").value],
    };

    console.log("🔍 Debugging: Opening Hours Before Sending", openingHours);

    try {
        const response = await fetch('/api/add-car-park', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                name: carParkName,
                height_restriction: heightRestriction,
                is_24_hours: is24Hours,
                opening_hours: openingHours
            })
        });

        await response.json();

        console.log("✅ Car Park Added Successfully!");

        // ✅ Refresh dropdown list immediately after adding a car park
        await fetchCarParks();

        // ✅ Hide the form automatically after submission
        document.getElementById("addCarParkForm").classList.add("d-none");

    } catch (error) {
        console.error("❌ Error adding car park:", error);
    }
}





// Function to update car park opening hours.
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

// 
async function fetchOpeningHours(carParkId) {
    try {
        const response = await fetch(`/api/opening-hours/${carParkId}`);
        const openingHours = await response.json();

        const openingHoursContainer = document.getElementById("openingHoursContent");

        if (openingHours.is_24_hours) {
            openingHoursContainer.innerHTML = `<p><strong>This car park is open 24 hours today.</strong></p>`;
        } else if (openingHours.opening_time && openingHours.closing_time) {
            const openingTimeFormatted = openingHours.opening_time.slice(0, 5); // ✅ Remove seconds
            const closingTimeFormatted = openingHours.closing_time.slice(0, 5); // ✅ Remove seconds

            openingHoursContainer.innerHTML = `<p><strong>${openingHours.day}:</strong> ${openingTimeFormatted} - ${closingTimeFormatted}</p>`;
        } else {
            openingHoursContainer.innerHTML = "<p>No opening hours available.</p>";
        }

        document.getElementById("openingHoursResult").classList.remove("d-none"); 

    } catch (error) {
        console.error("❌ Error fetching opening hours:", error);
    }
}





