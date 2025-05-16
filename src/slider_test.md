---
title: Slider 1800–1830–2024
toc: false
---

```js
import L from "npm:leaflet";
```


```js
if (L === undefined) console.error("L is undefined");
import "./plugins/leaflet-heat.js";
```

<div id="map-container" style="height: 500px; margin: 1em 0 2em 0;"></div>

```js
const geojson1830 = FileAttachment("./data/Berney_espaces_verts_macro.geojson").json();
```

```js
const geojson2024 = FileAttachment("./data/2024_espaces_verts_macro.geojson").json();
```
```js
function featureCentroid(feature) {
  const { type, coordinates } = feature.geometry;
  // unwrap to a flat list of [lon, lat] pairs
  let pts;
  if (type === "Point") {
    pts = [coordinates];
  } else if (type === "Polygon") {
    pts = coordinates[0];           // exterior ring
  } else if (type === "MultiPolygon") {
    pts = coordinates[0][0];        // first polygon’s exterior ring
  } else return null;
  // average them
  const [lonSum, latSum] = pts.reduce(
    ([lonAcc, latAcc], [lon, lat]) => [lonAcc + lon, latAcc + lat],
    [0, 0]
  );
  const n = pts.length || 1;
  return [latSum / n, lonSum / n];
}

const heatmapData1830 = geojson1830.features
  .map(f => {
    const c = featureCentroid(f);
    return c && [c[0], c[1], 0.5];
  })
  .filter(Boolean);

const heatmapData2024 = geojson2024.features
  .map(f => {
    const c = featureCentroid(f);
    return c && [c[0], c[1], 0.5];
  })
  .filter(Boolean);
```




```js
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



const map = L.map("map-container").setView([46.55, 6.65], 11);
globalThis.map = map;


L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

map.createPane("pane1830");
map.getPane("pane1830").style.zIndex = 400;

map.createPane("pane2024");
map.getPane("pane2024").style.zIndex = 401;

const layer1830 = L.geoJSON(geojson1830, {
  pane: "pane1830",
  style: f => ({
    color: "#333",
    fillColor: getColor(f.properties.macro_ev),
    fillOpacity: 0.6,
    weight: 1
  })
}).addTo(map);

//L.heatLayer(heatmapData1830, {
  //pane: "pane1830",
  //radius: 10,
  //blur: 15
//}).addTo(map);

const layer2024 = L.geoJSON(geojson2024, {
  pane: "pane2024",
  style: f => ({
    color: "#333",
    fillColor: getColor(f.properties.macro_ev),
    fillOpacity: 0.6,
    weight: 1
  })
}).addTo(map);

//L.heatLayer(heatmapData2024, {
  //pane: "pane2024",
  //radius: 10,
  //blur: 15
//}).addTo(map);


map.getPane("pane1830").style.opacity = 1;
map.getPane("pane2024").style.opacity = 0;

```



<label for="time-slider">
  Année : <strong id="time-value">1830</strong>
</label>
<br>
<input
  type="range"
  id="time-slider"
  min="1"
  max="2"
  step="0.01"
  value="1"
  style="width:100%; max-width:400px; margin:1em 0;"
>
<div style="display:flex; justify-content:space-between; font-size:0.8em; max-width:400px;">
  <span>1831</span><span>2024</span>
</div>

<script>
  const slider = document.getElementById("time-slider");
  const output = document.getElementById("time-value");

  function updateOpacity() {
    const t = +slider.value;        // 1 → 2
    const α = Math.max(0, Math.min((t - 1) / 1, 1));
    output.textContent = α < 0.5 ? "1831 - 2024" : "1831 - 2024";
    map.getPane("pane1830").style.opacity = 1 - α;
    map.getPane("pane2024").style.opacity = α;
  }

  slider.addEventListener("input", updateOpacity);
  updateOpacity();
</script>
