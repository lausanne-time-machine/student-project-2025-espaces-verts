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

```js
import * as turf from "npm:@turf/turf";
```



<div id="map-container" style="height: 500px; margin: 1em 0 2em 0; position: relative;">
  <!-- Leaflet will draw the map here -->

  <div class="legend">
    <strong>Catégories</strong><br>
    <i style="background:#228B22"></i> foret<br>
    <i style="background:#006400"></i> bosquet<br>
    <i style="background:#7CFC00"></i> pré<br>
    <i style="background:#DEB887"></i> champ<br>
    <i style="background:#8FBC8F"></i> vigne<br>
    <i style="background:#FFD700"></i> jardin
  </div>
</div>

<style>
  .legend {
    /* your existing styles… */
    background: white;
    padding: 6px 8px;
    font: 14px Arial, sans-serif;
    box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
    border-radius: 5px;
    line-height: 24px;
    color: #333;

    /* NEW */
    position: absolute;
    top: 10px;
    right: 10px;
    z-index: 1000;
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
const geojson1830 = FileAttachment("./data/espaces_verts_macro.geojson").json();
```

```js
const geojson2024 = FileAttachment("./data/2024_espaces_verts_macro.geojson").json();
```

```js
const geojson1800 = FileAttachment("./data/Berney_espaces_verts_macro.geojson").json();
```


```js

```

```js

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

const heatmapData1800 = geojson1800.features
  .map(f => {
    const c = featureCentroid(f);
    return c && [c[0], c[1], 0.5];
  })
  .filter(Boolean);

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

//L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  //attribution: '&copy; OpenStreetMap'
//}).addTo(map);

L.tileLayer(
  "https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}@2x.png",
  { attribution: "© OpenStreetMap, © CartoDB" }
).addTo(map);


map.createPane("pane1800"); map.getPane("pane1800").style.zIndex = 300;
map.createPane("pane1830"); map.getPane("pane1830").style.zIndex = 400;
map.createPane("pane2024"); map.getPane("pane2024").style.zIndex = 401;

// Build category→array-of-layers maps for each year
const categoryLayersMap1800 = new Map();
const categoryLayersMap1830 = new Map();
const categoryLayersMap2024 = new Map();

// 1800
const layer1800 = L.geoJSON(geojson1800, {
  pane: "pane1800",
  style: f => ({
    color: "#333",
    fillColor: getColor(f.properties.macro_ev),
    fillOpacity: 0.6,
    weight: 1
  }),
  onEachFeature(feature, layer) {
    const cat = feature.properties.macro_ev;
    if (!categoryLayersMap1800.has(cat)) categoryLayersMap1800.set(cat, []);
    categoryLayersMap1800.get(cat).push(layer);
  }
}).addTo(map);
globalThis.layer1800 = layer1800;
globalThis.categoryLayersMap1800 = categoryLayersMap1800;

// 1830
const layer1830 = L.geoJSON(geojson1830, {
  pane: "pane1830",
  style: f => ({
    color: "#333",
    fillColor: getColor(f.properties.macro_ev),
    fillOpacity: 0.6,
    weight: 1
  }),
  onEachFeature(feature, layer) {
    const cat = feature.properties.macro_ev;
    if (!categoryLayersMap1830.has(cat)) categoryLayersMap1830.set(cat, []);
    categoryLayersMap1830.get(cat).push(layer);
  }
}).addTo(map);
globalThis.layer1830 = layer1830;
globalThis.categoryLayersMap1830 = categoryLayersMap1830;

// 2024
const layer2024 = L.geoJSON(geojson2024, {
  pane: "pane2024",
  style: f => ({
    color: "#333",
    fillColor: getColor(f.properties.macro_ev),
    fillOpacity: 0.6,
    weight: 1
  }),
  onEachFeature(feature, layer) {
    const cat = feature.properties.macro_ev;
    if (!categoryLayersMap2024.has(cat)) categoryLayersMap2024.set(cat, []);
    categoryLayersMap2024.get(cat).push(layer);
  }
}).addTo(map);
globalThis.layer2024 = layer2024;
globalThis.categoryLayersMap2024 = categoryLayersMap2024;

// Initialize visibility
map.getPane("pane1800").style.opacity = 1;
map.getPane("pane1830").style.opacity = 0;
map.getPane("pane2024").style.opacity = 0;
```




<!-- 1️⃣ STYLES FOR SLIDER & FILTER BUTTONS -->
<style>
  /* — Slider styles, matching your buttons — */
  #time-slider {
    -webkit-appearance: none;
    appearance: none;
    width: 100%;
    max-width: 400px;
    height: 8px;
    border-radius: 4px;
    background: #fafafa;           /* same as button background */
    outline: none;
    margin: 1em 0;
    cursor: pointer;
    transition: background 0.2s ease;
  }
  #time-slider:hover {
    background: #f0f0f0;           /* slightly darker on hover */
  }
  #time-slider::-webkit-slider-runnable-track {
    height: 8px;
    border-radius: 4px;
    background: #fafafa;
  }
  #time-slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background: #fafafa;           /* same as un-checked button */
    border: 1px solid #ddd;
    box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    transition: background 0.2s ease, box-shadow 0.2s ease;
    margin-top: -4px;              /* center on track */
  }
  #time-slider::-webkit-slider-thumb:hover {
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }
  #time-slider:active::-webkit-slider-thumb {
    background: #333;              /* same as checked button */
    border-color: #333;
  }
  /* Firefox */
  #time-slider::-moz-range-track {
    height: 8px;
    border-radius: 4px;
    background: #fafafa;
  }
  #time-slider::-moz-range-thumb {
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background: #fafafa;
    border: 1px solid #ddd;
    box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    transition: background 0.2s ease, box-shadow 0.2s ease;
  }
  #time-slider:active::-moz-range-thumb {
    background: #333;
    border-color: #333;
  }
  /* IE */
  #time-slider::-ms-track {
    width: 100%;
    height: 8px;
    background: transparent;
    border-color: transparent;
    color: transparent;
  }
  #time-slider::-ms-fill-lower,
  #time-slider::-ms-fill-upper {
    background: #fafafa;
    border-radius: 4px;
  }
  #time-slider::-ms-thumb {
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background: #fafafa;
    border: 1px solid #ddd;
    box-shadow: 0 1px 2px rgba(0,0,0,0.05);
  }
  #time-slider:active::-ms-thumb {
    background: #333;
    border-color: #333;
  }

  /* — Filter buttons styles — */
  #macro-filter {
    display: flex;
    flex-direction: column;
    gap: 0.25em;
    margin: 1em 0;
    max-width: 200px;
  }
  #macro-filter input[type=checkbox] {
    display: none;
  }
  #macro-filter label {
    display: block;
    background: #fafafa;
    color: #444;
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 0.35em 0.75em;
    cursor: pointer;
    transition: background 0.2s, box-shadow 0.2s;
    box-shadow: 0 1px 2px rgba(0,0,0,0.05);
  }
  #macro-filter label:hover {
    background: #f0f0f0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }
  #macro-filter label:has(input:checked) {
    background: #333;
    color: #fff;
    border-color: #333;
    box-shadow: 0 2px 6px rgba(0,0,0,0.15);
  }
</style>

<!-- 2️⃣ SLIDER HTML & SCRIPT -->
<label for="time-slider">
  Année : <strong id="time-value">1800</strong>
</label><br>
<input
  id="time-slider"
  type="range"
  min="0" max="2" step="0.01" value="0"
/>
<div style="display:flex; justify-content:space-between; font-size:0.8em; max-width:400px;">
  <span>Berney (1831)</span>
  <span>Rénové (1888)</span>
  <span>Actuel (2024)</span>
</div>

<script>
  const slider = document.getElementById("time-slider");
  const output = document.getElementById("time-value");
  function updateOpacity() {
    const t = +slider.value;
    let o1800 = 0, o1830 = 0, o2024 = 0;
    if (t <= 1) {
      o1800 = 1 - t; o1830 = t;
      output.textContent = "1831 – 1888";
    } else {
      const u = t - 1;
      o1830 = 1 - u; o2024 = u;
      output.textContent = "1888 – 2024";
    }
    map.getPane("pane1800").style.opacity = o1800;
    map.getPane("pane1830").style.opacity = o1830;
    map.getPane("pane2024").style.opacity = o2024;
  }
  slider.addEventListener("input", updateOpacity);
  updateOpacity();
  
</script>




<!-- 3️⃣ FILTER HTML & SCRIPT -->
<div id="macro-filter">
  <strong>Filtrer par catégorie :</strong>
  <label><input type="checkbox" value="foret"   checked> forêt</label>
  <label><input type="checkbox" value="bosquet" checked> bosquet</label>
  <label><input type="checkbox" value="pre"     checked> pré</label>
  <label><input type="checkbox" value="champ"   checked> champ</label>
  <label><input type="checkbox" value="vigne"   checked> vigne</label>
  <label><input type="checkbox" value="jardin"  checked> jardin</label>
</div>

<script>
  const boxes = Array.from(document.querySelectorAll("#macro-filter input"));
  function applyMacroFilter() {
    const allowed = boxes.filter(cb => cb.checked).map(cb => cb.value);
    [
      [layer1800, categoryLayersMap1800],
      [layer1830, categoryLayersMap1830],
      [layer2024, categoryLayersMap2024]
    ].forEach(([layer, catMap]) => {
      layer.clearLayers();
      allowed.forEach(cat =>
        (catMap.get(cat) || []).forEach(f => layer.addLayer(f))
      );
    });
  }
  boxes.forEach(cb => cb.addEventListener("change", applyMacroFilter));
  applyMacroFilter();
</script>



