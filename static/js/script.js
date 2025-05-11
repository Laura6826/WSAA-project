// WSAA-project: Web Services and Applications.
// JAVASCRIPT for car-park space availability in Cork City.
// Author: Laura Lyons

// This makes showForm available globally
window.showForm = function(formId) {
  console.log("Showing form:", formId);

  // List of form IDs to hide
  const forms = ["addCarParkForm", "updateCarParkForm", "deleteCarParkForm"];
  forms.forEach(id => {
    const elem = document.getElementById(id);
    if (elem) {
      elem.classList.add("d-none");
    }
  });

  // Show the chosen form
  const formToShow = document.getElementById(formId);
  if (formToShow) {
    formToShow.classList.remove("d-none");
  } else {
    console.error(`Form with id "${formId}" not found!`);
  }
};

// Drop down car park menu and associated space availability.
document.addEventListener("DOMContentLoaded", async function () {
    await fetchCarParks(); // ✅ Fetch car park data and populate dropdowns
    updateCurrentTime();
    setInterval(updateCurrentTime, 1000);

    function showForm(formId) {
        console.log(`🔍 Showing form: ${formId}`);

        // ✅ Hide all forms first
        document.getElementById("addCarParkForm").classList.add("d-none");
        document.getElementById("updateCarParkForm").classList.add("d-none");
        document.getElementById("deleteCarParkForm").classList.add("d-none");

        // ✅ Show the requested form
        document.getElementById(formId).classList.remove("d-none");
    }

    // ✅ Attach event listeners to buttons
    document.getElementById("addCarParkButton").addEventListener("click", function () {
        showForm("addCarParkForm");
    });

    // ✅ Attach event listener AFTER ensuring `showForm` exists globally

    document.getElementById("updateCarParkButton").addEventListener("click", function () {
        showForm("updateCarParkForm"); // ✅ Show the Update Car Park form
        fetchCarParksForUpdate(); // ✅ Populate dropdown with car parks
    });

    document.getElementById("deleteCarParkButton").addEventListener("click", function () {
        showForm("deleteCarParkForm");
        fetchCarParksForDeletion(); // ✅ Ensures dropdown is populated
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
                resultContainer.innerText = "There is no verified data on space availability for this car park.";
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

// Function to add a new car park
async function addCarPark() {
    const carParkName = document.getElementById("carParkName").value;
    const heightRestriction = document.getElementById("heightRestriction").value;
    const is24Hours = document.getElementById("is24Hours").checked;

    const openingHours = {
        "Monday": [document.getElementById("Monday_open").value, document.getElementById("Monday_close").value],
        "Tuesday": [document.getElementById("Tuesday_open").value, document.getElementById("Tuesday_close").value],
        "Wednesday": [document.getElementById("Wednesday_open").value, document.getElementById("Wednesday_close").value],
        "Thursday": [document.getElementById("Thursday_open").value, document.getElementById("Thursday_close").value],
        "Friday": [document.getElementById("Friday_open").value, document.getElementById("Friday_close").value],
        "Saturday": [document.getElementById("Saturday_open").value, document.getElementById("Saturday_close").value],
        "Sunday": [document.getElementById("Sunday_open").value, document.getElementById("Sunday_close").value],
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

        // Refresh dropdown list immediately after adding a car park
        await fetchCarParks();

        //Hide the form automatically after submission
        document.getElementById("addCarParkForm").classList.add("d-none");

    } catch (error) {
        console.error("❌ Error adding car park:", error);
    }
}

// Function to copy opening hours from the previous day
function copyPrevious(day) {
    const days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
    const currentIndex = days.indexOf(day);

    if (currentIndex > 0) { 
        const previousDay = days[currentIndex - 1];
        
        document.getElementById(`${day}_open`).value = document.getElementById(`${previousDay}_open`).value;
        document.getElementById(`${day}_close`).value = document.getElementById(`${previousDay}_close`).value;

        console.log(`✅ Copied hours from ${previousDay} to ${day}`);
    }
}

// Function to set a day as closed
function setClosed(day) {
    document.getElementById(`${day}_open`).value = "";
    document.getElementById(`${day}_close`).value = "";
    document.getElementById(`${day}_open`).disabled = true;
    document.getElementById(`${day}_close`).disabled = true;

    console.log(`✅ Marked ${day} as Closed`);
}

// Function to add car park opening hours.
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

        // Refresh dropdowns after updating opening hours
        const updatedResponse = await fetch('/api/get-car-parks');
        const updatedParkingData = await updatedResponse.json();
        populateDropdown(["carParkDropdown"], updatedParkingData);

    } catch (error) {
        console.error("❌ Error adding opening hours:", error);
    }
}

// Function to retreive car park details
async function fetchOpeningHours(carParkId) {
    try {
        const response = await fetch(`/api/opening-hours/${carParkId}`);
        const openingHours = await response.json();

        const openingHoursContainer = document.getElementById("openingHoursContent");

        if (openingHours.is_24_hours) {
            openingHoursContainer.innerHTML = `<p><strong>This car park is open 24 hours today.</strong></p>`;
        } else if (openingHours.opening_time && openingHours.closing_time) {
            const openingTimeFormatted = openingHours.opening_time.slice(0, 5); 
            const closingTimeFormatted = openingHours.closing_time.slice(0, 5); 

            openingHoursContainer.innerHTML = `<p><strong>${openingHours.day}:</strong> ${openingTimeFormatted} - ${closingTimeFormatted}</p>`;
        } else {
            openingHoursContainer.innerHTML = "<p>No opening hours available.</p>";
        }

        document.getElementById("openingHoursResult").classList.remove("d-none"); 

    } catch (error) {
        console.error("❌ Error fetching opening hours:", error);
    }
}

// Function to add car park details
document.addEventListener("DOMContentLoaded", function () {
    const carParkNameInput = document.getElementById("carParkName");
    const open24HoursCheckbox = document.getElementById("open24HoursCheckbox");
    const addCarParkButton = document.getElementById("addCarParkButton");

    carParkNameInput.addEventListener("input", function () {
        if (carParkNameInput.value.trim() !== "") {  
            open24HoursCheckbox.style.display = "block";  // Show checkbox
            addCarParkButton.style.display = "block";    // Show button
        } else {
            open24HoursCheckbox.style.display = "none";  // Hide again if empty
            addCarParkButton.style.display = "none";    // Hide again if empty
        }
    });
});

// Function to fetch car park details for deletion
async function fetchCarParksForDeletion() {
    try {
        const response = await fetch("/api/car-parks");
        const carParks = await response.json();

        const dropdown = document.getElementById("deleteCarParkDropdown");
        dropdown.innerHTML = '<option value="">Select Car Park</option>';

        carParks.forEach(carPark => {
            let option = document.createElement("option");
            option.value = carPark.id;
            option.textContent = carPark.name;
            dropdown.appendChild(option);
        });

        console.log("✅ Dropdown updated!");

    } catch (error) {
        console.error("❌ Error fetching car parks:", error);
    }
}

// Function to delete a car park form
function showDeleteCarParkForm() {
    console.log("✅ Click to Confirm button clicked!");

    const form = document.getElementById("deleteCarParkDetails");
    if (!form) {
        console.error("❌ Error: deleteCarParkDetails not found.");
        return; // Prevent crashing if the element doesn't exist
    }

    form.classList.remove("d-none"); // ✅ Make sure it's visible
}

async function deleteCarPark() {
    console.log("✅ Delete Car Park button clicked!");

    const carParkId = document.getElementById("deleteCarParkDropdown").value;

    if (!carParkId) {
        alert("Please select a car park to delete.");
        return;
    }

    try {
        const response = await fetch("/delete_car_park", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: `car_park_id=${carParkId}`
        });

        const result = await response.json();
        alert(result.message); // ✅ Show success or error message

        if (response.ok) {
            console.log("✅ Car park deleted, refreshing dropdown...");

            await fetchCarParks(); // ✅ Refresh dropdown list
            document.getElementById("deleteCarParkForm").classList.add("d-none"); // ✅ Hide the form
        }

    } catch (error) {
        console.error("❌ Error deleting car park:", error);
        alert("An error occurred while deleting the car park.");
    }
}

// Populate Dropdown with Existing Car Parks
async function fetchCarParksForUpdate() {
    const dropdown = document.getElementById("updateCarParkDropdown");
    dropdown.innerHTML = '<option value="">Select Car Park</option>';

    try {
        const response = await fetch("/api/car-parks");
        if (!response.ok) throw new Error("❌ Server error: " + response.status);

        const carParks = await response.json();
        carParks.forEach(carPark => {
            let option = document.createElement("option");
            option.value = carPark.id;
            option.textContent = carPark.name;
            dropdown.appendChild(option);
        });

    } catch (error) {
        console.error("❌ Error fetching car parks:", error);
    }
}

// Function to load existing car park details
// Function to load existing car park details
async function loadCarParkDetails() {
    const selectedId = document.getElementById("updateCarParkDropdown").value;
    if (!selectedId) return;

    try {
        const response = await fetch(`/api/car-parks/${selectedId}`);
        if (!response.ok) {
            throw new Error("❌ Error fetching car park details!");
        }
        const carPark = await response.json();
        console.log("🔍 Car Park Data:", carPark);

        // Ensure opening_hours exists; if not, use default empty times.
        const openingHours = carPark.opening_hours || {};

        // Declare the days array only once.
        const days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
        
        days.forEach(day => {
            // Use the day key from the API response; if missing, set empty defaults.
            const hours = openingHours[day] || { open: "", close: "" };

            // Populate the corresponding fields using the same day format as in your HTML
            document.getElementById(`update_${day}_open`).value = hours.open || "";
            document.getElementById(`update_${day}_close`).value = hours.close || "";
        });
        
        // Height restriction field
        document.getElementById("updateHeightRestriction").value = carPark.height_restriction || "";
        
        // Handle checkbox for 24-hour status
        const twentyFour = document.getElementById("updateIs24Hours");
        if (twentyFour) {
            twentyFour.checked = carPark.is_24_hours || false;
        }
    } catch (error) {
        console.error("Error in loadCarParkDetails:", error);
    }
}

  
        // Height restriction field (if not present, defaults to empty)
        document.getElementById("updateHeightRestriction").value = carPark.height_restriction || "";
        
        // If you have a checkbox for 24-hour status, set it accordingly.
        const twentyFour = document.getElementById("updateIs24Hours");
        if (twentyFour) {
            twentyFour.checked = carPark.is_24_hours || false;
        }
    } catch (error) {
        console.error("Error in loadCarParkDetails:", error);
    }
}

// Function to fetch car parks for update
async function fetchCarParksForUpdate() {
    console.log("🔍 Fetching car parks for update...");

    try {
        const response = await fetch("/api/car-parks"); // ✅ Request car park data from backend
        if (!response.ok) throw new Error(`❌ Server error: ${response.status}`);

        const carParks = await response.json();
        console.log("✅ Car Parks received:", carParks); // Debugging output

        const dropdown = document.getElementById("updateCarParkDropdown");

        dropdown.innerHTML = '<option value="">Select Car Park</option>';

        if (carParks.length === 0) {
            dropdown.innerHTML += '<option disabled>No car parks available</option>';
            return;
        }

        carParks.forEach(carPark => {
            let option = document.createElement("option");
            option.value = carPark.id;
            option.textContent = carPark.name;
            dropdown.appendChild(option);
        });

    } catch (error) {
        console.error("❌ Error fetching car parks:", error);
    }
}

async function updateCarPark() {
    const carParkId = document.getElementById("updateCarParkDropdown").value;
    const newHeight = document.getElementById("updateHeightRestriction").value;
    
    // Build the new_hours object with keys matching your DB entry (e.g., "Monday", "Tuesday", etc.)
    const new_hours = {
        "Monday": {
            open: document.getElementById("update_Monday_open").value,
            close: document.getElementById("update_Monday_close").value
        },
        "Tuesday": {
            open: document.getElementById("update_Tuesday_open").value,
            close: document.getElementById("update_Tuesday_close").value
        },
        "Wednesday": {
            open: document.getElementById("update_Wednesday_open").value,
            close: document.getElementById("update_Wednesday_close").value
        },
        "Thursday": {
            open: document.getElementById("update_Thursday_open").value,
            close: document.getElementById("update_Thursday_close").value
        },
        "Friday": {
            open: document.getElementById("update_Friday_open").value,
            close: document.getElementById("update_Friday_close").value
        },
        "Saturday": {
            open: document.getElementById("update_Saturday_open").value,
            close: document.getElementById("update_Saturday_close").value
        },
        "Sunday": {
            open: document.getElementById("update_Sunday_open").value,
            close: document.getElementById("update_Sunday_close").value
        }
    };
    
    if (!carParkId) {
        alert("Please select a car park to update.");
        return;
    }
    
    try {
        const response = await fetch("/update_car_park", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                id: carParkId,
                opening_hours: new_hours,
                height_restriction: newHeight
            })
        });
    
        const result = await response.json();
        alert(result.message);
        if (response.ok) {
            // Optionally hide the update form or refresh lists.
        }
    } catch (error) {
        console.error("❌ Error updating car park:", error);
        alert("An error occurred while updating the car park.");
    }
}

