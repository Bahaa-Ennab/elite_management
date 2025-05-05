const select = document.getElementById("time");
const times = [];
for (let hour = 8; hour <= 16; hour++) {
    times.push(`${hour}:00`);
    times.push(`${hour}:30`);
}

times.forEach(time => {
    let option = document.createElement("option");
    option.value = time;
    option.textContent = time;
    select.appendChild(option);
});