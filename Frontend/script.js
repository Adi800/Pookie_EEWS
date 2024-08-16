// Function to show notification
function showNotification(message) {
    const notification = document.getElementById('notification');
    notification.innerText = message;
    notification.classList.remove('hidden');

    // Automatically hide notification after 60 seconds
    setTimeout(() => {
        notification.classList.add('hidden');
    }, 60000);
}

// Function to fetch earthquake data from the backend and show in a list
async function fetchEarthquakeData() {
    const response = await fetch('/api/earthquake', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    });

    if (response.ok) {
        const data = await response.json();
        showDataList(data);
    } else {
        console.error('Error fetching earthquake data:', response.statusText);
    }
}

// Function to show a list of earthquake data
function showDataList(dataList) {
    const dataListContainer = document.getElementById('dataListContainer');
    dataListContainer.innerHTML = ''; // Clear previous results

    dataList.forEach((data, index) => {
        const listItem = document.createElement('li');
        listItem.innerText = `Earthquake ${index + 1}: Magnitude ${data.magnitude}, Location: ${data.location}`;
        listItem.addEventListener('click', () => updateMapAndNotification(data));
        dataListContainer.appendChild(listItem);
    });
}

// Function to update the map and notification based on earthquake data
function updateMapAndNotification(data) {
    const { magnitude, latitude, longitude, location, range } = data;

    // Show notification with earthquake details
    const message = `Earthquake detected! Magnitude: ${magnitude}, Location: ${location}`;
    showNotification(message);

    // Update the map
    const mapSrc = `https://maps.google.com/maps?q=${latitude},${longitude}&z=${range}&output=embed`;
    document.getElementById('map').src = mapSrc;
}

// WebSocket connection to receive real-time earthquake data
const socket = new WebSocket('wss://your-websocket-url');

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    updateMapAndNotification(data);
};

// Event listener for the fetch data button (for testing purposes)
document.getElementById('fetchDataBtn').addEventListener('click', fetchEarthquakeData);

/*
// Simulate earthquake data for Adisaptagram, West Bengal
const simulatedData = {
    magnitude: 6.5,
    latitude: 22.9076,  // Latitude for Adisaptagram
    longitude: 88.3394, // Longitude for Adisaptagram
    location: 'Adisaptagram, West Bengal',
    range: 10
};

// Call the function to update the map and notification
updateMapAndNotification(simulatedData);
*/
