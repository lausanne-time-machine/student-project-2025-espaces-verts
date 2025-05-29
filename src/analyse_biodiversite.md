---
title: Comparaison des espaces verts - Évolution de la biodiversité (Berney vs actuel)
toc: false
---

```js
// Import Leaflet
import L from "npm:leaflet";
```

```js
// Charger Leaflet.heat
if (L === undefined) console.error("L is undefined");
import "./plugins/leaflet-heat.js";
```

```js
// Charger le GeoJSON enrichi avec les données de biodiversité
const geojson1 = FileAttachment("./data/evolution_biodiv_Melotte_Berney.geojson").json()
const geojson2 = FileAttachment("./data/evolution_biodiv_Berney_Renove.geojson").json()
const geojson3 = FileAttachment("./data/evolution_biodiv_Renove_Actuel.geojson").json()

```

```js
function waitForMapContainer() {
  return new Promise(resolve => {
    function check() {
      const el = document.getElementById("map-container");
      if (el) resolve(el);
      else requestAnimationFrame(check);
    }
    check();
  });
}
```

```js
function createMapAndLayer(mapContainer, geojsonData) {
    if (L.DomUtil.get(mapContainer)?._leaflet_id) {
        L.DomUtil.get(mapContainer)._leaflet_id = null;
    }

    const map = L.map(mapContainer).setView([46.55, 6.65], 13);

    const osmLayer = L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: '&copy; OpenStreetMap contributors'
    });

    const cartoLayer = L.tileLayer("https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}@2x.png", {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    const layerControl = L.control.layers({
        "OSM": osmLayer,
        "Carto": cartoLayer
    }).addTo(map);

    function getColor(delta) {
        return delta > 1000 ? '#006837' :
               delta > 0     ? '#66bd63' :
               delta === 0   ? '#f7f7f7' :
               delta > -1000 ? '#f46d43' :
                               '#a50026';
    }

    const geoJsonLayer = L.geoJSON(geojsonData, {
        style: function (feature) {
            const delta = feature.properties.delta_biodiv || 0;
            return {
                color: "#000000",
                fillColor: getColor(delta),
                fillOpacity: 0.7,
                weight: 0.8
            };
        },
        onEachFeature: function (feature, layer) {
            const p = feature.properties;
            const popup = `
                <strong>Changement :</strong> ${p.changement}<br>
                <strong>Ancienne classe :</strong> ${p.macro_ev_old || "—"}<br>
                <strong>Nouvelle classe :</strong> ${p.macro_ev_new || "—"}<br>
                <strong>Δ biodiversité :</strong> ${Math.round(p.delta_biodiv || 0)}<br>
                <strong>Surface (m²) :</strong> ${Math.round(p.area_inter || p.area || 0)}
            `;
            layer.bindPopup(popup);
        }
    }).addTo(map);

    layerControl.addOverlay(geoJsonLayer, "Évolution biodiversité");

    // Légende colorée
    const legend = L.control({ position: "bottomright" });

    legend.onAdd = function () {
        const div = L.DomUtil.create("div", "legend");
        const grades = [
            { label: "Gain élevé", color: "#006837" },
            { label: "Gain modéré", color: "#66bd63" },
            { label: "Stable", color: "#f7f7f7" },
            { label: "Perte modérée", color: "#f46d43" },
            { label: "Perte forte", color: "#a50026" }
        ];

        let html = "<strong>Δ biodiversité</strong><br>";
        for (const g of grades) {
            html += `<i style="background:${g.color}; width: 18px; height: 18px; float: left; margin-right: 8px; opacity: 0.8;"></i>${g.label}<br>`;
        }

        div.innerHTML = html;
        div.style.background = "white";
        div.style.padding = "6px 8px";
        div.style.font = "14px Arial, sans-serif";
        div.style.boxShadow = "0 0 15px rgba(0,0,0,0.2)";
        div.style.borderRadius = "5px";
        div.style.lineHeight = "24px";
        return div;
    };

    legend.addTo(map);

    return { map, layerControl };
}
```

<!-- 🗺️ Conteneur HTML pour la carte -->
```html

<h1>Analyse biodiversité</h1>

<p> Dans le prolongement de notre étude sur l’évolution des espaces verts lausannois, nous avons souhaité approfondir la question de la biodiversité en lien avec l’occupation du sol dans la région romande. Pour ce faire, nous avons défini un indice de richesse biologique pour six types de milieux : forêt, champ, pré, jardin, vigne et bosquet. Ces indices représentent une estimation relative de la richesse spécifique moyenne (tous groupes taxonomiques confondus) par unité de surface, à l’échelle contemporaine. </p> <p> L’objectif est de croiser ces coefficients avec des données historiques de surface (provenant notamment de plans cadastraux) afin de modéliser les pertes ou gains de biodiversité sur plusieurs siècles. </p> <ul> <li><strong>Forêt – indice 100</strong> : Milieu le plus riche en espèces aujourd’hui en Suisse, grâce à une grande diversité structurelle et écologique.</li> <li><strong>Champ – indice 20</strong> : L’agriculture intensive appauvrit considérablement la biodiversité, réduisant le nombre d’espèces présentes.</li> <li><strong>Pré – indice 40</strong> : Les prairies traditionnelles ont perdu une grande part de leur richesse, mais restent localement importantes.</li> <li><strong>Jardin – indice 50</strong> : Diversité intermédiaire, très variable selon la gestion humaine. Refuges importants en milieu urbain.</li> <li><strong>Vignoble – indice 30</strong> : Potentiel écologique faible en moyenne, sauf dans les cas de gestion extensive ou biologique.</li> <li><strong>Bosquet – indice 80</strong> : Corridors et refuges essentiels pour de nombreuses espèces, presque aussi riches que les forêts.</li> </ul> <p> Ces indices doivent être compris comme des valeurs relatives destinées à être couplées avec les données spatiales pour étudier l’évolution de la richesse écologique régionale. Bien qu’ils ne tiennent pas compte de la variation temporelle des pratiques de gestion, ils offrent un cadre utile pour une analyse historique à grande échelle. </p> 



<h2>Melotte (1727) vs. Berney (1830)</h2>
<div id="map-container" style="height: 500px; margin: 1em 0;"></div>

<p> La comparaison entre le cadastre Melotte (1721) et le cadastre Berney (1831) montre une perte marquée de biodiversité, concentrée autour du noyau historique de Lausanne. Cette dynamique reflète l’intensification agricole et les débuts de l’urbanisation. Les surfaces autrefois occupées par des bosquets ou des prairies riches (indice 40–80) sont transformées en champs cultivés (indice 20), appauvrissant fortement la biodiversité. En fait, la région connaît une augmentation de la pression foncière liée à la croissance démographique, entre le XVIIIe et le début du XIXe siècle. L’introduction progressive de l’agriculture intensive, déjà amorcée avec les réformes agraires (enclosures, assolement triennal), contribue à la réduction des habitats semi-naturels. </p>

<h2>Berney (1830) vs. Renove (1880)</h2>

<div id="map2" style="height: 500px; margin: 1em 0;"></div>

<p>
Sur la période 1831-1888 (cadastre Berney et Rénové), la heatmap montre une dynamique plus nuancée. Bien que l’urbanisation continue, certaines zones montrent des gains ou une stabilité. Cela correspond à une transformation partielle de l’espace agricole (champs) en jardins ou parcs, typique de la structuration urbaine bourgeoise du XIXe siècle. Ainsi, le développement du chemin de fer dès les années 1850 et l’expansion industrielle s’accompagnent de la création d’espaces verts urbains (ex. Parc Mon-Repos, Parc de Milan). Les jardins (indice 50) remplacent parfois des surfaces agricoles peu riches, induisant localement une hausse de biodiversité.
</p>
<h2>Renove (1880) vs. Actuel (2024)</h2>

<div id="map3" style="height: 500px; margin: 1em 0;"></div>

<p>
Sur une période allant de 1888 à 2024, on observe des tendances contrastées : pertes persistantes dans les zones très urbanisées (centre-ville) mais gains notables en périphérie. Ces gains s’expliquent par les politiques écologiques modernes (Plan d'aménagement fédéral du territoire, jardins communautaires, corridors verts, haies plantées, végétalisation urbaine). Depuis les années 1990, les politiques communales suisses promeuvent l’intégration de la nature en ville (Stratégie biodiversité Lausanne). Des friches industrielles ont été reconverties en espaces semi-naturels. Le retour de bosquets ou la préservation de forêts périurbaines contribuent significativement aux gains d’indice.
</p>

<p>
    En conclusion, les heatmaps illustrent trois siècles de tension entre urbanisation, pratiques agricoles, et préservation de la biodiversité. On passe d’un paysage rural semi-naturel riche à un système fragmenté, où la biodiversité a chuté dans les centres mais regagne du terrain en périphérie grâce à une gestion écologique plus fine. Cela reflète un schéma bien documenté dans l’histoire du territoire suisse : intensification – artificialisation – résilience écologique partielle.
    </p>
```

```js
await waitForMapContainer();
const mapElements = createMapAndLayer("map-container", geojson1);
const mapElements2 = createMapAndLayer("map2", geojson2);
const mapElements3 = createMapAndLayer("map3", geojson3);

// 🔥 Création de la heatmap (zones de perte de biodiversité uniquement)
const heatmapData = geojson1.features
    .filter(f => (f.properties.delta_biodiv || 0) < 0)
    .map(f => {
        const geom = f.geometry;
        if (geom.type === "Polygon" || geom.type === "MultiPolygon") {
            const coords = geom.type === "Polygon" ? geom.coordinates[0] : geom.coordinates[0][0];
            const lats = coords.map(c => c[1]);
            const lngs = coords.map(c => c[0]);
            const lat = lats.reduce((a, b) => a + b) / lats.length;
            const lng = lngs.reduce((a, b) => a + b) / lngs.length;
            return [lat, lng, 0.5]; // intensité uniforme
        }
        return null;
    })
    .filter(d => d !== null);

const heatmapLayer = L.heatLayer(heatmapData, {
    radius: 15,
    blur: 20,
    maxZoom: 17,
    gradient: {
        0.4: 'blue',
        0.65: 'lime',
        1: 'red'
    }
}).addTo(mapElements.map);

mapElements.layerControl.addOverlay(heatmapLayer, "Pertes biodiversité (heatmap)");

// 🔥 Création de la heatmap (zones de perte de biodiversité uniquement)
const heatmapData2 = geojson2.features
    .filter(f => (f.properties.delta_biodiv || 0) < 0)
    .map(f => {
        const geom = f.geometry;
        if (geom.type === "Polygon" || geom.type === "MultiPolygon") {
            const coords = geom.type === "Polygon" ? geom.coordinates[0] : geom.coordinates[0][0];
            const lats = coords.map(c => c[1]);
            const lngs = coords.map(c => c[0]);
            const lat = lats.reduce((a, b) => a + b) / lats.length;
            const lng = lngs.reduce((a, b) => a + b) / lngs.length;
            return [lat, lng, 0.5]; // intensité uniforme
        }
        return null;
    })
    .filter(d => d !== null);

const heatmapLayer2 = L.heatLayer(heatmapData2, {
    radius: 15,
    blur: 20,
    maxZoom: 17,
    gradient: {
        0.4: 'blue',
        0.65: 'lime',
        1: 'red'
    }
}).addTo(mapElements2.map);

mapElements2.layerControl.addOverlay(heatmapLayer2, "Pertes biodiversité (heatmap)");


// 🔥 Création de la heatmap (zones de perte de biodiversité uniquement)
const heatmapData3 = geojson3.features
    .filter(f => (f.properties.delta_biodiv || 0) < 0)
    .map(f => {
        const geom = f.geometry;
        if (geom.type === "Polygon" || geom.type === "MultiPolygon") {
            const coords = geom.type === "Polygon" ? geom.coordinates[0] : geom.coordinates[0][0];
            const lats = coords.map(c => c[1]);
            const lngs = coords.map(c => c[0]);
            const lat = lats.reduce((a, b) => a + b) / lats.length;
            const lng = lngs.reduce((a, b) => a + b) / lngs.length;
            return [lat, lng, 0.5]; // intensité uniforme
        }
        return null;
    })
    .filter(d => d !== null);

const heatmapLayer3 = L.heatLayer(heatmapData3, {
    radius: 15,
    blur: 20,
    maxZoom: 17,
    gradient: {
        0.4: 'blue',
        0.65: 'lime',
        1: 'red'
    }
}).addTo(mapElements3.map);

mapElements3.layerControl.addOverlay(heatmapLayer3, "Pertes biodiversité (heatmap)");



```

---

<h2>Limites de l’approche par macroclasses et considérations sur la biodiversité</h2>

Bien que le regroupement des espaces verts en macroclasses facilite la comparaison cartographque à travers les siècles, cette simplification présente plusieurs limites, notamment lorsqu’il s’agit d’évaluer la qualité écologique et la biodiversité réelle des milieux concernés.
 Premièrement, les termes utilisés pour désigner certains types d’espaces ont évolué au fil du temps. Par exemple, le mot “jardin”, très fréquent dans les documents contemporains, était peu utilisé dans les cadastres anciens, ou désignait des réalités différentes. Aujourd’hui, un “jardin” peut désigner aussi bien un gazon ornemental qu’un espace végétalisé riche en espèces, alors qu’historiquement, il pouvait se référer à un potager ou à une simple cour plantée. Ces variations sémantiques rendent délicate l’interprétation directe des données anciennes.

De plus, la classification en grandes catégories masque des différences écologiques fondamentales. Un parc ou une prairie peuvent être très pauvres ou très riches en biodiversité, selon leur gestion. Par exemple, le gazon, forme extrême d’un espace végétal maîtrisé, est souvent dépourvu de fleurs et donc peu attractif pour les insectes. A l’inverse, les prairies maigres, souvent en pente et non fertilisées, peuvent abriter jusqu’à 60 espèces florales différentes, attirant une grande diversité d’insectes. Leur richesse biologique varie fortement selon la période de floraison, liée aux pratiques de fauche ou de pâturage.
L’usage intensif des herbicides, la disparition des lisières, haies et buissons indigènes-éléments clés pour l’avifaune-, ainsi que la perte de structures paysagères anciennes, sont autant de facteurs de déclin pour la flore sauvage. De surcroît, si certaines zones sont laissées sans entretien (notamment les prairies), elles évoluent naturellement vers des formations arbustives, voire vers la forêt, stade ultime de la succession végétale en milieu tempéré. Mais ce dernier état n’apparait qu’après une certaine période qui souvent trop longue dans le cas de notre dynamique urbaine qui change rapidement.
Ainsi, bien que les macroclasses offrent une lecture simplifiée et fonctionnelle de l’évolution des espaces verts, elles ne rendent pas compte des dynamiques internes de ces milieux ni de leur qualité écologique réelle. Pour une compréhension plus fine, il est nécessaire de croiser cette approche avec des données de terrain, des inventaires floristiques ou faunistiques, et des analyses de pratiques de gestion.

Un bel exemple illustrant ce phénomène est la zone de Vidy. Jusqu'en 1884, les eaux du Lémans furent soumis à une fluctution importante de leurs niveau (jusqu'à 2m). Ces territoires étaient classée, dans les cadastres Berney puis Rénové, comme pré avec un indice relativement faible de bio-diversité. Après la régulation du niveau du lac, la zone fut requalifiée en "jardin", avec, selon notre métrique, un plus fort coefficient de bio-diversité. Or, il va de soit qu'un marais possède une plus grande richesse en terme de bio-diversité qu'un parc comme on le connait à Vidy aujourd'hui. s




Source: HOFFER-MASSARD, Françoise, VUST, Mathias et BORNAND, Christophe, 2006. Flore de Lausanne, 1. A la découverte de la nature en ville, publié en 2006. ISBN-10 2-940365-05-9
