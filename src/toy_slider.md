---
title: Toy slider 
toc: false
---

```js
import {leaflet} from "@observablehq/leaflet"
import {slider}   from "@jashkenas/inputs"

```

!!!```js
const epochs = [
  {year: 1900, url: "https://.../cad_1900.geojson"},
];
```
!!!

!!!```js

viewof epoch = slider({
  min: epochs[0].year,
  max: epochs[epochs.length-1].year,
  step: null,                   // discrete steps
  marks: epochs.map(d => d.year),
  value: epochs[0].year,
  format: d => `${d}`
})

```
!!!


!!!```js
map = leaflet({
  container: DOM.element("div", {style: "height: 500px"}),
  center: [46.52, 6.63],  // Lausanne
  zoom: 13
})
```
!!!

!!!```js
currentLayer = {
  let layer = null;
  // whenever “epoch” changes, swap the layer
  html`<div style="position:absolute;top:0;right:0;padding:8px;background:white;z-index:400;">
    Year: <strong>${epoch}</strong>
  </div>`,
  {
    // remove old
    if (layer) map.removeLayer(layer);
    // find the URL
    const obj = epochs.find(d => d.year === epoch);
    // fetch & add
    layer = await fetch(obj.url)
      .then(res => res.json())
      .then(js => L.geoJSON(js, {
        style: f => ({ color: "#006600", weight: 1, fillOpacity: 0.4 })
      }).addTo(map));
    return layer;
  }
}
```
!!!