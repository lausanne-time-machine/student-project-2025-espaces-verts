---
title: Comparaison des espaces verts - Cadastre Berney vs Actuel
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
# Cadastre Berney
Cette page présente le cadastre Berney de Lausanne (1831).

## Carte
```js
const geojson = FileAttachment("./data/comparaison_macro.geojson").json()
```
```js
// Create Map and Layer - Runs Once
function createMapAndLayer(mapContainer, geojsonData) {
    const map = L.map(mapContainer).setView([46.55, 6.65], 11);

    const osmLayer = L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: '&copy; OpenStreetMap contributors'
    });

    const cartoLayer = L.tileLayer("https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}@2x.png", {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    // Crate a control to switch between layers
    const layerControl = L.control.layers().addTo(map);

    // Add the OSM and Carto layers to the control
    layerControl.addBaseLayer(osmLayer, "OSM");
    layerControl.addBaseLayer(cartoLayer, "Carto");

    // Crate a control to switch between layers
    const layerControl = L.control.layers().addTo(map);

    // Fonction de couleur en fonction du type de changement
    function getColor(status) {
        return {
            "gagné": "#2E8B57",      // Vert
            "perdu": "#B22222",      // Rouge
            "true": "#FFD700",       // Modifié (changement de classe)
        }[status] || "#555555";      // Autres / inconnus
    }

    const geoJsonLayer = L.geoJSON(geojsonData, {
        style: function (feature) {
            const s = feature.properties.status || feature.properties.changement;
            return {
                color: "#000",
                fillColor: getColor(s),
                fillOpacity: 0.6,
                weight: 1
            };
        },
        onEachFeature: function (feature, layer) {
            const props = feature.properties;
            const popup = `
                <strong>Statut :</strong> ${props.status || "modifié"}<br>
                <strong>Ancienne classe :</strong> ${props.macro_ev_old || "—"}<br>
                <strong>Nouvelle classe :</strong> ${props.macro_ev_new || "—"}<br>
                <strong>Surface (m²) :</strong> ${Math.round(props.area_m2 || 0)}
            `;
            layer.bindPopup(popup);
        }
    }).addTo(map);

    layerControl.addOverlay(geoJsonLayer, "Changements");
    return { map, geoJsonLayer, layerControl };
}

// Call the creation function and store the results
const mapElements = createMapAndLayer("map-container", geojson);
```

```js
// Reactive Update Cell - Runs when filteredMergeIDsSet changes
function updateMapFilter(geoJsonLayer, featureLayersMap, filteredMergeIDsSet) {
    let featuresAdded = 0;
    let featuresRemoved = 0;

    // Iterate through all the layers we stored
    featureLayersMap.forEach((layerSet, merge_id) => {
        const shouldBeVisible = filteredMergeIDsSet.has(merge_id);
        // LayerSet may contain multiple layers for the same merge_id
        layerSet.forEach(layer => {
            const isVisible = geoJsonLayer.hasLayer(layer);
            if (shouldBeVisible && !isVisible) {
                // If the layer is not already added, add it
                geoJsonLayer.addLayer(layer);
                featuresAdded++;
            } else if (!shouldBeVisible && isVisible) {
                // If the layer is currently displayed but should not be, remove it
                geoJsonLayer.removeLayer(layer);
                featuresRemoved++;
            }
        });
    });
}

// Call the update function. This cell depends on filteredMergeIDsSet and mapElements.
const mapUpdateStatus = updateMapFilter(mapElements.geoJsonLayer, mapElements.featureLayersMap, filteredMergeIDsSet)
```

```js
// Map the GeoJSON data to an array of entries matching the required pattern for the heatmap
// e.g. [50.5, 30.5, 0.2] // lat, lng, intensity
const heatmapData = geojson.features.map(feature => {
    const coords = feature.geometry.coordinates;
    const lat = coords[1];
    const lng = coords[0];
    const intensity = 0.5;
    return [lat, lng, intensity];
});
```

```js
// Create a heatmap layer using the heatmapData
const heatmapLayer = L.heatLayer(heatmapData, {
    radius: 10,
    blur: 15,
});

// Add the heatmap layer to the layer control
mapElements.layerControl.addOverlay(heatmapLayer, "Heatmap");
```

