import { heightRestrictions } from './heightRestrictions.js';

export function checkHeightCompatibility() {
    const dropdown = document.getElementById("carParkDropdown");
    const selectedOption = dropdown.options[dropdown.selectedIndex];
    const heightRestriction = heightRestrictions[selectedOption.value] || "Unknown";

    const vehicleHeight = parseFloat(document.getElementById("vehicleHeight").value);
    const resultContainer = document.getElementById("heightCheckResult");

    resultContainer.className = "alert mt-3";

    if (!selectedOption.value) {
        resultContainer.innerText = "Please select a valid car park.";
        resultContainer.classList.add("alert-warning");
    } else if (heightRestriction === "Unknown") {
        resultContainer.innerText = `Height restriction data is missing for "${selectedOption.value}".`;
        resultContainer.classList.add("alert-warning");
    } else if (vehicleHeight <= heightRestriction) {
        resultContainer.innerText = `Your vehicle fits the height restriction of ${heightRestriction} meters for "${selectedOption.value}".`;
        resultContainer.classList.add("alert-success");
    } else {
        resultContainer.innerText = `Your vehicle exceeds the height restriction of ${heightRestriction} meters for "${selectedOption.value}".`;
        resultContainer.classList.add("alert-danger");
    }
    resultContainer.classList.remove("d-none");
}
