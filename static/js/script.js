// WSAA-project: Web Services and Applications.
// JAVASCRIPT for car-park space availability in Cork City.
// Author: Laura Lyons

document.addEventListener("DOMContentLoaded", async function () {
    await fetchCarParks(); // Fetch car park data and populate dropdowns
    updateCurrentTime();
    setInterval(updateCurrentTime, 1000);

    document.getElementById("carParkDropdown").addEventListener("change", async function () {
        const selectedId = this.value;
        const resultContainer = document.getElementById("checkFreeSpaces");
    
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
            openingHoursResult.style.display = "block";
            return;
        }

        try {
            console.log(`🔍 Fetching opening hours for Car Park ID ${selectedId}...`);
            const response = await fetch(`/api/opening-hours/${selectedId}`);
            if (!response.ok) throw new Error(`❌ Server Error: ${response.status}`);

            const todayHours = await response.json();
            console.log("✅ API Response:", todayHours);

            // ✅ Show special message for 24-hour car parks with no times
            if (todayHours.message) {
                openingHoursContainer.innerHTML = `<p>${todayHours.message}</p>`;
            } else {
                openingHoursContainer.innerHTML =
                    todayHours.opening_time && todayHours.closing_time
                        ? `<p><strong>${todayHours.day}:</strong> ${todayHours.opening_time} - ${todayHours.closing_time}</p>`
                        : `<p><strong>${todayHours.day}:</strong> ${todayHours.status || "Open as usual"}</p>`;
            }

            openingHoursResult.style.display = "block";

        } catch (error) {
            console.error("❌ Error fetching opening hours:", error);
            openingHoursContainer.innerHTML = "<p>No data available.</p>";
            openingHoursResult.style.display = "block";
        }
    });
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



