---
title: Carte 2024
toc: false
---

```js
// Explicit import of leaflet to avoid issues with the Leaflet.heat plugin
import L from "npm:leaflet";
```

```js
// Wait for L to be defined before importing the Leaflet.heat plugin
// This is necessary because Leaflet.heat depends on the L variable being defined
if (L === undefined) console.error("L is undefined");

// Leaflet.heat: https://github.com/Leaflet/Leaflet.heat/
import "./plugins/leaflet-heat.js";
```

```js
import turf from "npm:@turf/turf";
```


# Carte 2024
Cette page présente le carte actuelle de Lausanne (2024).

## Carte

```js
const geojson = FileAttachment("./data/2024_espaces_verts_macro.geojson").json()
```

```js
// Calcul des centroïdes de chaque patch
centroids = patches.features.map(f => turf.centroid(f).geometry.coordinates)

// Seuil de distance (km) pour définir un lien de connectivité
threshold = 0.5

// Comptage du nombre de voisins sous le seuil pour chaque patch\ nneighborCounts = patches.features.map((f, i) =>
  patches.features.reduce((sum, g, j) => {
    if (i === j) return sum
    const d = turf.distance(
      centroids[i],
      turf.centroid(g).geometry.coordinates,
      { units: "kilometers" }
    )
    return sum + (d < threshold ? 1 : 0)
  }, 0)
)

// Normalisation pour obtenir un indice [0,1]
gmax = Math.max(...neighborCounts)
patches.features.forEach((f, i) => {
  f.properties.connectivityIndex = neighborCounts[i] / (gmax || 1)
})
```







<!-- Create the map container -->
<div id="map-container" style="height: 500px; margin: 1em 0 2em 0;"></div>

```js
// Create Map and Layer - Runs Once
function createMapAndLayer(mapContainer, geojsonData) {
    const map = L.map(mapContainer).setView([46.55, 6.65], 11);


    const osmLayer = L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    });

    const cartoLayer = L.tileLayer("https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}@2x.png", {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    // Crate a control to switch between layers
    const layerControl = L.control.layers().addTo(map);

    // Add the OSM and Carto layers to the control
    layerControl.addBaseLayer(osmLayer, "OSM");
    layerControl.addBaseLayer(cartoLayer, "Carto");

    // Store map from geom_id -> leaflet layer instance
    const featureLayersMap = new Map();

        // Define getColor outside the object
    function getColor(cat) {
        return {
            foret: "#228B22",
            bosquet: "#006400",
            pre: "#7CFC00",
            champ: "#DEB887",
            vigne: "#8FBC8F",
            jardin: "#FFD700",
        }[cat] || "#000000";
    }

    // Affichage des patches
    L.geoJSON(patches, {
        style: f => ({
        color: '#333',
        fillColor: getColor(f.properties.macro_ev),
        fillOpacity: 0.5,
        weight: 1
        })
    }).addTo(map)

    // Ajout des épicentres
    patches.features.forEach(f => {
        const [lon, lat] = turf.centroid(f).geometry.coordinates
        const idx = f.properties.connectivityIndex || 0
        const radius = 4 + (20 - 4) * idx
        const opacity = 0.3 + 0.6 * idx

        L.circleMarker([lat, lon], {
        radius,
        fillColor: '#000',
        fillOpacity: opacity,
        color: '#333',
        weight: 1
        }).addTo(map)
    })

    return container
    }
```