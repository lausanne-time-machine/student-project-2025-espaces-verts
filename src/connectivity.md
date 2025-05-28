---
title: connectivity
toc: false
---

```js
// Explicit import of leaflet to avoid issues with the Leaflet.heat plugin
// 1) Charger Leaflet
leaflet = require("leaflet@1.7.1")
// 2) Charger Turf pour les centroïdes
turf    = require("https://cdn.jsdelivr.net/npm/@turf/turf@6/turf.min.js")

```

```js
// 3) Lire le GeoJSON depuis la pièce jointe
patches = await FileAttachment("2024_espaces_verts_macro.geojson").json()
```



<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <title>Connectivité 2024</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/leaflet@1.7.1/dist/leaflet.css"/>
  <style>
    #map { height: 600px; }
    .legend {
      position: absolute;
      bottom: 10px;
      left: 10px;
      background: #fff;
      padding: 10px;
      border-radius: 4px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.2);
      font-size: 14px;
    }
    .legend i {
      display: inline-block;
      width: 12px;
      height: 12px;
      margin-right: 6px;
      border-radius: 50%;
    }
  </style>
</head>
<body>
  <div id="map"></div>
  <div class="legend">
    <h4>Épicentres de connectivité</h4>
    <i style="background: rgba(0,0,0,0.3)"></i> Faible<br/>
    <i style="background: rgba(0,0,0,0.6)"></i> Moyen<br/>
    <i style="background: rgba(0,0,0,0.9)"></i> Fort
  </div>

  <script src="https://cdn.jsdelivr.net/npm/leaflet@1.7.1/dist/leaflet.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/Turf.js/6.5.0/turf.min.js"></script>
  <script>
    // Initialisation de la carte
    const map = L.map('map').setView([46.5191, 6.5668], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{ attribution:'&copy; OpenStreetMap' }).addTo(map);

    // Chargement du GeoJSON
    fetch('src/data/2024_espaces_verts_macro.geojson')
      .then(res => res.json())
      .then(json => {
        // Affichage des patches
        L.geoJSON(json, {
          style: f => ({
            color: getColor(f.properties.class),
            weight: 1,
            fillOpacity: 0.4
          })
        }).addTo(map);

        // Calcul et affichage des epicentres
        json.features.forEach(f => {
          const centroid = turf.centroid(f).geometry.coordinates;
          const idx = f.properties.connectivityIndex || 0; // normalisé 0-1
          const {radius, opacity} = styleEpicenter(idx);
          L.circleMarker([centroid[1], centroid[0]], {
            radius,
            fillOpacity: opacity,
            fillColor: '#000',
            color: '#333',
            weight: 1
          }).addTo(map);
        });
      });

    // Palette pastel par classe
    function getColor(cat) {
      return {
        bosquet: '#A8D5BA',
        champ:   '#F5E1A4',
        foret:   '#B2CDA1',
        jardin:  '#F7C6C7',
        pre:     '#D5E8D4',
        vigne:   '#D8B4E2'
      }[cat] || '#999';
    }

    // Détermine rayon et opacité selon indice
    function styleEpicenter(idx) {
      const rmin = 4, rmax = 20;
      return { radius: rmin + (rmax - rmin) * idx, opacity: 0.3 + 0.6 * idx };
    }
  </script>
</body>
</html>