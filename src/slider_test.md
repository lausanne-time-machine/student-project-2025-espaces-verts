---
title: Carte 1831–2024 (Fade)
toc: false
---

```js
import L from "npm:leaflet";
import "./plugins/leaflet-heat.js"; // Optional if using heatmap features
import {Inputs} from "@observablehq/inputs";
```

```js
// Slider to blend between 1831 (Berney) and modern (2024)
viewof mix = Inputs.range([0, 1], {
  step: 0.01,
  value: 0.5,
  label: "Mix 1831 → 2024"
})
```

```js
// Display the current mix value (0 = fully 1831, 1 = fully 2024)
mix
```

```js
// Load both GeoJSON datasets
geojson1831 = FileAttachment("./data/**Berney_espaces_verts_macro**.geojson").json()
geojson2024 = FileAttachment("./data/2024_espaces_verts_macro.geojson").json()
```

<!-- Map container -->
<div id="map-fade" style="height: 500px; margin: 1em 0;"></div>

```js
// Initialize map and two empty layers
map = L.map("map-fade").setView([46.55, 6.65], 11)
L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map)

// Prepare two GeoJSON layers for fade blending
deriveOnEach = onEachFeature  // reuse your popup logic
layer1831 = L.geoJSON([], { onEachFeature: deriveOnEach, style: () => ({}) }).addTo(map)
layer2024 = L.geoJSON([], { onEachFeature: deriveOnEach, style: () => ({}) }).addTo(map)
```

```js
// Color function by category
function getColor(cat) {
  return {
    foret: "#228B22",
    bosquet: "#006400",
    pre: "#7CFC00",
    champ: "#DEB887",
    vigne: "#8FBC8F",
    jardin: "#FFD700"
  }[cat] || "#000000"
}

// Base style without opacity
function baseStyle(feature) {
  return {
    color: "#333",
    fillColor: getColor(feature.properties.macro_ev),
    weight: 1
  }
}
```

```js
// Reactive update: blend the two layers by 'mix'
{
  // 1831 layer fades out as mix→1
  layer1831
    .clearLayers()
    .addData(geojson1831)
    .setStyle(f => ({
      ...baseStyle(f),
      fillOpacity: 1 - mix,
      opacity:     1 - mix
    }))

  // 2024 layer fades in as mix→1
  layer2024
    .clearLayers()
    .addData(geojson2024)
    .setStyle(f => ({
      ...baseStyle(f),
      fillOpacity: mix,
      opacity:     mix
    }))
}
```

```js
// Optionally, add legends or heatmap overlays for each layer as needed
