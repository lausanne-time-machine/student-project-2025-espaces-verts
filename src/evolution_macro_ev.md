---
title: Comparaison des espaces verts - Cadastre Berney vs Actuel
toc: false
---

```js
// Explicit import of leaflet
import L from "npm:leaflet";

import "./plugins/leaflet-heat.js";

const geojson = FileAttachment("./data/comparaison_macro.geojson").json()

function createMapAndLayer(mapContainer, geojsonData) {
    const map = L.map(mapContainer).setView([46.55, 6.65], 11);

    const osmLayer = L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: '&copy; OpenStreetMap contributors'
    });

    const cartoLayer = L.tileLayer("https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}@2x.png", {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    const layerControl = L.control.layers().addTo(map);
    layerControl.addBaseLayer(osmLayer, "OSM");
    layerControl.addBaseLayer(cartoLayer, "Carto");

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

const mapElements = createMapAndLayer("map-container", geojson);
