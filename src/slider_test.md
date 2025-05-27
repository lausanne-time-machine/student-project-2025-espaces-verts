---
title: Slider 1800–1830–2024
toc: false
---

```js
import L from "npm:leaflet";
```




<div id="map-container" style="height: 500px; margin: 1em 0 2em 0; position: relative;">
  <!-- Leaflet will draw the map here -->

  <div class="legend">
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
    bottom: 30px;
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
const geojson1721 = FileAttachment("./data/Melotte-1721.geojson").json();
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

const heatmapData1721 = geojson1721.features
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
map.createPane("pane1721"); map.getPane("pane1721").style.zIndex = 200;

// Build category→array-of-layers maps for each year
const categoryLayersMap1800 = new Map();
const categoryLayersMap1830 = new Map();
const categoryLayersMap2024 = new Map();
const categoryLayersMap1721 = new Map()



//1721


const layer1721 = L.geoJSON(geojson1721, {
  pane: "pane1721",
  style: f => ({
    color: "#333",
    fillColor: getColor(f.properties.macro_ev),
    fillOpacity: 0.6,
    weight: 1
  }),
  onEachFeature(feature, layer) {
    const cat = feature.properties.macro_ev
    if (!categoryLayersMap1721.has(cat)) categoryLayersMap1721.set(cat, [])
    categoryLayersMap1721.get(cat).push(layer)
  }
}).addTo(map)

globalThis.layer1721 = layer1721
globalThis.categoryLayersMap1721 = categoryLayersMap1721
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
map.getPane("pane1721").style.opacity = 1;
map.getPane("pane1800").style.opacity = 0;
map.getPane("pane1830").style.opacity = 0;
map.getPane("pane2024").style.opacity = 0;
```

<!-- 1️⃣ UPDATED STYLES FOR SLIDER, FILTER BUTTONS, AND FIXED BOTTOM-LEFT BOX -->
<style>
  /* — Slider widget container, fixed bottom-left of viewport — */
  #slider-container {
    position: relative;
    width: 1000px;
    padding: 1em 1.25em;
    background: #fafafa;
    border: 1px solid #ddd;
    border-radius: 6px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  }
  #slider-container label {
    display: block;
    margin-bottom: 0.75em;
    font-weight: bold;
    color: #333;
  }

  /* — Slider track & thumb styling — */
  #time-slider {
    -webkit-appearance: none;
    appearance: none;
    width: 100%;
    height: 8px;
    border-radius: 4px;
    background: #ddd;
    outline: none;
    cursor: pointer;
    transition: background 0.2s ease;
  }
  #time-slider:hover { background: #ccc; }
  #time-slider::-webkit-slider-runnable-track {
    height: 8px;
    border-radius: 4px;
    background: #ddd;
  }
  #time-slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background: #fafafa;
    border: 1px solid #ddd;
    box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    margin-top: -4px;
    transition: background 0.2s ease, box-shadow 0.2s ease;
  }
  #time-slider:active::-webkit-slider-thumb {
    background: #333;
    border-color: #333;
  }
  /* Firefox */
  #time-slider::-moz-range-track {
    height: 8px;
    border-radius: 4px;
    background: #ddd;
  }
  #time-slider::-moz-range-thumb {
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background: #fafafa;
    border: 1px solid #ddd;
    box-shadow: 0 1px 2px rgba(0,0,0,0.05);
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
    background: #ddd;
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

  /* — Filter buttons styles — (unchanged) */
  #macro-filter {
    display: flex;
    flex-direction: column;
    gap: 0.25em;
    margin: 1em 0;
    max-width: 200px;
  }
  #macro-filter input[type=checkbox] { display: none; }
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

<!-- 2️⃣ SLIDER + LEGEND MARKUP -->
<div id="slider-container">
  <label for="time-slider">
    Année : <strong id="time-value">1721</strong>
  </label>
  <input
    id="time-slider"
    type="range"
    min="0" max="3" step="0.01" value="0"
  >
  <div style="
      display: flex;
      justify-content: space-between;
      font-size: 0.8em;
      margin-top: 0.75em;
    ">
    <span>Melotte 1721</span>
    <span>Berney 1831</span>
    <span>Rénové 1888</span>
    <span>Actuel 2024</span>
  </div>
</div>

<!-- 3️⃣ SLIDER FADE LOGIC -->
<script>
  const slider = document.getElementById("time-slider");
  const output = document.getElementById("time-value");

  function updateOpacity() {
    const t = +slider.value;
    let o1721=0, o1800=0, o1830=0, o2024=0;

    if (t <= 1) {
      o1721 = 1 - t;
      o1800 = t;
    } else if (t <= 2) {
      const u = t - 1;
      o1800 = 1 - u;
      o1830 = u;
    } else {
      const u = t - 2;
      o1830 = 1 - u;
      o2024 = u;
    }

    if (t <= 1)      output.textContent = "1721 – 1831";
    else if (t <= 2) output.textContent = "1831 – 1888";
    else             output.textContent = "1888 – 2024";

    map.getPane("pane1721").style.opacity = o1721;
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
      [layer1721, categoryLayersMap1721],
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


<style>
  /* 1) Make it absolutely positioned inside your map container */
  #macro-filter {
    position: absolute;
    top: 10px;      /* distance from the top edge of the map */
    right: 10px;    /* distance from the right edge */
    z-index: 1000;  /* ensure it sits above the map tiles/controls */
    
    /* 2) Tweak sizing & typography */
    font-size: 0.85em;    /* smaller text */
    line-height: 1.2;     /* tighter lines */
    padding: 6px 8px;     /* less padding */
    
    /* 3) Keep your existing look */
    background: rgba(255,255,255,0.9);
    border: 1px solid #ccc;
    border-radius: 4px;
  }

  /* 4) Optional: tighten up the checkboxes/labels */
  #macro-filter label {
    display: inline-block;
    margin-right: 6px;
  }
  #macro-filter input {
    margin-right: 2px;
    transform: scale(0.9); /* slightly smaller checkboxes */
    vertical-align: text-top;
  }
</style>










<!-- SURFACE ANALYSIS -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Évolution des surfaces par classe</title>
  <!-- 1️⃣ Load Chart.js from CDN -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    body {
      font-family: Arial, sans-serif;
      padding: 1em;
      background: #f9f9f9;
    }
    #chart-container {
      max-width: 700px;
      margin: auto;
      background: #fff;
      padding: 0.5em;
      box-shadow: 0 1px 4px rgba(0,0,0,0.1);
      border-radius: 4px;
    }
  </style>
</head>
<body>
  <h2>Évolution des surfaces par classe</h2>
  <div id="chart-container">
    <!-- 2️⃣ Canvas for Chart.js -->
    <canvas id="areaChart"></canvas>
  </div>

  <script>
  // 3️⃣ Your CSV data inline; you could also fetch it
  const dataRaw = `year,class,total_area_m2
1800,bosquet,58160.307797483765
1800,champ,2469105.0297332285
1800,foret,375599.7681377862
1800,jardin,479224.51431752933
1800,pre,4016861.91537962
1800,vigne,2052771.6831927958
1830,bosquet,4488.835962014241
1830,champ,1380955.974013836
1830,foret,555212.9713601727
1830,jardin,675700.8423114982
1830,pre,4122339.7980536777
1830,vigne,1533033.0384950945
2024,foret,476654.2435590087
2024,jardin,4240887.377227397
2024,pre,96200.33831764334
2024,vigne,1644.423232589514`;

  // 4️⃣ Parse CSV into arrays
  function parseCSV(text) {
    const [header, ...lines] = text.trim().split("\n");
    const cols = header.split(",");
    return lines.map(line => {
      const vals = line.split(",");
      return cols.reduce((obj, key, i) => {
        obj[key] = isNaN(vals[i]) ? vals[i] : +vals[i];
        return obj;
      }, {});
    });
  }
  const data = parseCSV(dataRaw);

  // 5️⃣ Group by class and year
  const classes = [...new Set(data.map(d => d.class))];
  const years   = [1800,1830,2024];
  const datasets = years.map((year, idx) => ({
    label: year.toString(),
    backgroundColor: ["#888","#555","#333"][idx],
    data: classes.map(c => {
      const rec = data.find(d => d.year === year && d.class === c);
      return rec ? rec.total_area_m2 : 0;
    })
  }));

  // 6️⃣ Create the bar chart
  const ctx = document.getElementById("areaChart").getContext("2d");
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: classes,
      datasets: datasets
    },
    options: {
      responsive: true,
      scales: {
        x: {
          title: { display: true, text: 'Classe' }
        },
        y: {
          title: { display: true, text: 'Surface (m²)' },
          beginAtZero: true
        }
      },
      plugins: {
        legend: {
          position: 'top'
        },
        tooltip: {
          callbacks: {
            label: ctx => `${ctx.dataset.label}: ${ctx.parsed.y.toLocaleString()} m²`
          }
        }
      }
    }
  });
  </script>
</body>
</html>


