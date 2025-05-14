---
title: Cadastre Rénové
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

# Cadastre Rénové
Cette page présente le cadastre rénové de Lausanne (1889).

## Carte

```js
const geojson = FileAttachment("./data/espaces_verts_macro.geojson").json()
```

<!-- Macro-class filter UI -->
<div id="macro-filter" style="margin-bottom: 1em;">
    <strong>Filtrer par catégorie :</strong><br>
    <label><input type="checkbox" value="foret" checked> foret</label>
    <label><input type="checkbox" value="bosquet" checked> bosquet</label>
    <label><input type="checkbox" value="pre" checked> pré</label>
    <label><input type="checkbox" value="champ" checked> champ</label>
    <label><input type="checkbox" value="vigne" checked> vigne</label>
    <label><input type="checkbox" value="jardin" checked> jardin</label>
</div>


<!-- Create the map container -->
<div id="map-container" style="height: 500px; margin: 1em 0 2em 0;"></div>

<style>
    .legend {
        background: white;
        padding: 6px 8px;
        font: 14px Arial, sans-serif;
        box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
        border-radius: 5px;
        line-height: 24px;
        color: #333;
    }

    .legend i {
        width: 18px;
        height: 18px;
        float: left;
        margin-right: 8px;
        opacity: 0.8;
        display: inline-block;
    }
</style>


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

    const categoryLayersMap = new Map();

    const geoJsonLayer = L.geoJSON(geojsonData, {
        style: function (feature) {
            const cat = feature.properties.macro_ev;
            return {
                color: "#333",
                fillColor: getColor(cat),
                fillOpacity: 0.6,
                weight: 1
            };
        },
        onEachFeature: function (feature, layer) {
        const cat = feature.properties.macro_ev;
        if (!categoryLayersMap.has(cat)) {
            categoryLayersMap.set(cat, []);
        }
        categoryLayersMap.get(cat).push(layer);
    }   
        
    }).addTo(map);
    
    layerControl.addOverlay(geoJsonLayer, "Points");

    // Create and add a legend control
    const legend = L.control({ position: "bottomright" });

    legend.onAdd = function (map) {
        const div = L.DomUtil.create("div", "info legend");

        const categories = ["foret", "bosquet", "pre", "champ", "vigne", "jardin"];
        const labels = categories.map(cat => {
            return `<i style="background:${getColor(cat)}"></i> ${cat}`;
        });

        div.innerHTML = "<strong>Catégories</strong><br>" + labels.join("<br>");
        return div;
    };

    legend.addTo(map);


    // Return the the map instance, the layer group, and the mapping
    return { map, layerControl, geoJsonLayer, categoryLayersMap };
}

// Call the creation function and store the results
const mapElements = createMapAndLayer("map-container", geojson);

// Function to apply macro-class filter
function applyMacroFilter(geoJsonLayer, categoryLayersMap) {
    const checked = Array.from(document.querySelectorAll("#macro-filter input:checked"))
        .map(input => input.value);

    // Clear all layers first
    geoJsonLayer.clearLayers();

    // Re-add only layers matching selected categories
    checked.forEach(cat => {
        const layers = categoryLayersMap.get(cat) || [];
        layers.forEach(layer => geoJsonLayer.addLayer(layer));
    });
}

// Add event listeners to checkboxes
document.querySelectorAll("#macro-filter input").forEach(input => {
    input.addEventListener("change", () => {
        applyMacroFilter(mapElements.geoJsonLayer, mapElements.categoryLayersMap);
    });
});

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
