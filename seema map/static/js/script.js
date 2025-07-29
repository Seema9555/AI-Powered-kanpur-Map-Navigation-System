

const map = L.map('map', {
  center: [26.4499, 80.3319],
  zoom: 13,
});

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Mapbox Geocoders
const geocoderSource = new MapboxGeocoder({
  accessToken: mapboxgl.accessToken,
  placeholder: 'Search Source',
  mapboxgl: mapboxgl
});

const geocoderDestination = new MapboxGeocoder({
  accessToken: mapboxgl.accessToken,
  placeholder: 'Search Destination',
  mapboxgl: mapboxgl
});

document.querySelector('#source').parentNode.insertBefore(
  geocoderSource.onAdd(map),
  document.querySelector('#source')
);

document.querySelector('#destination').parentNode.insertBefore(
  geocoderDestination.onAdd(map),
  document.querySelector('#destination')
);

// Handle the button click for finding the path
function findPath() {
  const source = document.getElementById('source').value;
  const destination = document.getElementById('destination').value;

  fetch('/shortest-path', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ source, destination })
  })
  .then(res => res.json())
  .then(data => {
    if (data.error) return alert(data.error);

    if (blueLine) map.removeLayer(blueLine);
    redLines.forEach(line => map.removeLayer(line));
    redLines = [];
    if (movingMarker) map.removeLayer(movingMarker);

    data.edges.forEach(edge => {
      const poly = L.polyline(edge, { color: 'red', weight: 2, opacity: 0.5 }).addTo(map);
      redLines.push(poly);
    });

    blueLine = L.polyline(data.route, { color: 'blue', weight: 5 }).addTo(map);
    map.fitBounds(blueLine.getBounds());

    let i = 0;
    movingMarker = L.marker(data.route[0], {
      icon: L.icon({
        iconUrl: 'https://cdn-icons-png.flaticon.com/512/684/684908.png',
        iconSize: [30, 30]
      })
    }).addTo(map);

    const interval = setInterval(() => {
      if (i < data.route.length - 1) {
        i++;
        movingMarker.setLatLng(data.route[i]);
      } else {
        clearInterval(interval);
      }
    }, 300);
  })
  .catch(error => {
    console.error("Error fetching path:", error);
    alert("Something went wrong.");
  });
}

// Icons for start and destination
const startIcon = L.icon({
  iconUrl: 'https://cdn-icons-png.flaticon.com/512/684/684908.png',
  iconSize: [30, 30],
  className: 'bounce-marker'
});

const endIcon = L.icon({
  iconUrl: 'https://cdn-icons-png.flaticon.com/512/535/535239.png', // destination flag
  iconSize: [30, 30],
  className: 'bounce-marker'
});

let startMarker, endMarker, movingMarker;

function findPath() {
  const source = document.getElementById('source').value;
  const destination = document.getElementById('destination').value;

  fetch('/shortest-path', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ source, destination })
  })
  .then(res => res.json())
  .then(data => {
    if (data.error) return alert(data.error);

    if (blueLine) map.removeLayer(blueLine);
    redLines.forEach(line => map.removeLayer(line));
    redLines = [];
    if (movingMarker) map.removeLayer(movingMarker);
    if (startMarker) map.removeLayer(startMarker);
    if (endMarker) map.removeLayer(endMarker);

    // Add red edges
    data.edges.forEach(edge => {
      const poly = L.polyline(edge, { color: 'red', weight: 2, opacity: 0.5 }).addTo(map);
      redLines.push(poly);
    });

    // Blue shortest path
    blueLine = L.polyline(data.route, { color: 'blue', weight: 5 }).addTo(map);
    map.fitBounds(blueLine.getBounds());

    // Animated start and end markers
    startMarker = L.marker(data.route[0], { icon: startIcon }).addTo(map);
    endMarker = L.marker(data.route[data.route.length - 1], { icon: endIcon }).addTo(map);

    // Optional: animated movement
    let i = 0;
    movingMarker = L.marker(data.route[0], { icon: startIcon }).addTo(map);
    const interval = setInterval(() => {
      if (i < data.route.length - 1) {
        i++;
        movingMarker.setLatLng(data.route[i]);
      } else {
        clearInterval(interval);
      }
    }, 300);
  })
  .catch(error => {
    console.error("Error fetching path:", error);
    alert("Something went wrong.");
  });
}
