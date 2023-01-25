// Base open street map layer
const baseLayerUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';

// DB scan layer group
// const dbscanLayerGroup = L.layerGroup([L.tileLayer(baseLayerUrl)]);

// K-Means layer groups
const kMeansLayerGroup = L.layerGroup([L.tileLayer(baseLayerUrl)]);

const map_kmeans = L.map('map_kmeans', {
    center: [32.2324682888, -110.9569233858],
    zoom: 11,
    zoomControl: false
});

// Add layers control
L.control.layers({
    // "DBScan": dbscanLayerGroup,
    "K-Means": kMeansLayerGroup
}, null, {collapsed: false, position: 'topright'}).addTo(map_kmeans);

kMeansLayerGroup.addTo(map_kmeans)

////// MAP DB SCAN

// Base open street map layer
// DB scan layer group
const dbscanLayerGroup = L.layerGroup([L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png')]);

const map_dbscan = L.map('map_dbscan', {
    center: [32.2324682888, -110.9569233858],
    zoom: 11,
    zoomControl: false
});

// Add layers control
L.control.layers({
    "DBScan": dbscanLayerGroup,
}, null, {collapsed: false, position: 'topleft'}).addTo(map_dbscan);

dbscanLayerGroup.addTo(map_dbscan)


function populateKMeansLayerGroup(){
    fetch("http://127.0.0.1:5500/get_clustered_df_kmeans")
        .then(response => response.json())
        .then(data => {
            console.log("arrived kmeans data")
            data.forEach(item => {
                createMarker(item["cluster"], item).addTo(kMeansLayerGroup)
            })
        });
}

function populateDBScanLayerGroup(){
    fetch("http://127.0.0.1:5500/get_clustered_df_dbscan")
        .then(response => response.json())
        .then(data => {
            console.log("arrived dbscan data")
            data.forEach(item => {
                createMarker(item["eps"], item).addTo(dbscanLayerGroup)
            })
        });
}


function createMarker(cluster, item){
    const myCustomColour = getClusterColor(cluster)

    const markerHtmlStyles = `
              background-color: ${myCustomColour};
              width: 1.5rem;
              height: 1.5rem;
              display: block;
              left: -1.5rem;
              top: -1.5rem;
              position: relative;
              border-radius: 3rem 3rem 0;
              transform: rotate(45deg);
              border: 1px solid #FFFFFF`

    const marker = L.marker([
        item["latitude"],
        item["longitude"]
    ], {
        'icon': L.divIcon({
            className: "my-custom-pin",
            iconAnchor: [0, 24],
            labelAnchor: [-6, 0],
            popupAnchor: [0, -36],
            html: `<span style="${markerHtmlStyles}" />`
        })
    })
    marker.bindPopup(
        "<p>Name: " + item['name'] + "</p>" +
        "<p>Address: " + item['address'] + "</p>"
    ).openPopup();

    return marker
}

const clusterColors = {}

function getClusterColor(cluster) {
    const cl_col = clusterColors[cluster]

    if (!cl_col) {
        const random_color = generateHex(6)
        clusterColors[cluster] = random_color
        return random_color
    } else {
        return cl_col
    }
}

function generateHex(size) {
    let result = [];
    let hexRef = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f'];

    for (let n = 0; n < size; n++) {
        result.push(hexRef[Math.floor(Math.random() * 16)]);
    }
    return "#" + result.join('');
}

populateKMeansLayerGroup()

populateDBScanLayerGroup()
