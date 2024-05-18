document.addEventListener('DOMContentLoaded', function() {
    const light = document.getElementById('light');
    const changeLightButton = document.getElementById('change-light');

    changeLightButton.addEventListener('click', () => {
        fetch('http://localhost:5000/process', {
            method: 'POST',
            body: new FormData() // Assuming you have the form data to send to the server
        })
        .then(response => response.json())
        .then(data => {
            const vehicleCount = data.total_vehicle_count;
            if (vehicleCount < 20) {
                changeLightButton.style.backgroundColor = 'green';
            } else if (vehicleCount >= 20 && vehicleCount <= 30) {
                changeLightButton.style.backgroundColor = 'orange';
            } else {
                changeLightButton.style.backgroundColor = 'red';
            }
        })
        .catch(error => console.error('Error:', error));
    });

    // Road Conditions functionality
    const roadConditionsStatus = document.getElementById('road-conditions-status');
    const updateConditionsButton = document.getElementById('update-conditions');

    updateConditionsButton.addEventListener('click', () => {
        const conditions = ['Good', 'Fair', 'Poor'];
        const currentCondition = roadConditionsStatus.textContent;
        let newCondition = conditions[(conditions.indexOf(currentCondition) + 1) % conditions.length];
        roadConditionsStatus.textContent = newCondition;
    });

    // Accident Reports functionality
    const accidentReportsList = document.getElementById('accident-reports-list');
    const addReportButton = document.getElementById('add-report');

    addReportButton.addEventListener('click', () => {
        const newReport = prompt('Enter a new accident report:');
        if (newReport) {
            const listItem = document.createElement('li');
            listItem.textContent = newReport;
            accidentReportsList.appendChild(listItem);
        }
    });
});
