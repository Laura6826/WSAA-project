export function handleCarParkSchedule(scheduleForToday, freeSpaces, selectedOption) {
    const resultContainer = document.getElementById("carParkInfoResult");
    const now = new Date();

    if (scheduleForToday?.status === "24 Hours") {
        resultContainer.innerHTML = `
            <strong>${selectedOption.value}:</strong> Open 24 hours today.<br>
            Free spaces: ${freeSpaces}.
        `;
        resultContainer.classList.add("alert-success");
        return;
    }

    const closingTime = scheduleForToday?.closingTime || "N/A";
    const [closingHours, closingMinutes] = closingTime.split(":").map(Number);
    const minutesUntilClosing = (closingHours * 60 + closingMinutes) - (now.getHours() * 60 + now.getMinutes());

    if (minutesUntilClosing <= 0) {
        resultContainer.innerHTML = `
            <strong>${selectedOption.value}:</strong> Already closed.<br>
            Free spaces: ${freeSpaces}.
        `;
        resultContainer.classList.add("alert-danger");
    } else if (minutesUntilClosing <= 60) {
        resultContainer.innerHTML = `
            <strong>${selectedOption.value}:</strong> Closes in ${minutesUntilClosing} minutes.<br>
            Free spaces: ${freeSpaces}.
        `;
        resultContainer.classList.add("alert-warning");
    } else {
        resultContainer.innerHTML = `
            <strong>${selectedOption.value}:</strong> Closes at ${closingTime} today.<br>
            Free spaces: ${freeSpaces}.
        `;
        resultContainer.classList.add("alert-info");
    }
}
