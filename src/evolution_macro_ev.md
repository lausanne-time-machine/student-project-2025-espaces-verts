---
title: Comparaison des espaces verts - Cadastre Berney vs Actuel
toc: false
---

```js
// Import Leaflet
import L from "npm:leaflet";
```
```js
// Charger Leaflet.heat (nécessite que L soit défini)
if (L === undefined) console.error("L is undefined");
import "./plugins/leaflet-heat.js";
```

```js
// Charger le GeoJSON
const geojson = FileAttachment("./data/evolution_Melotte_Berney.geojson").json()
const geojson2 = FileAttachment("./data/evolution_Berney_Renove.geojson").json()
const geojson3 = FileAttachment("./data/evolution_Renove_Actuel.geojson").json()
```

<!-- === Titre et introduction === -->
<h1>Comparaison des espaces verts – Lausanne, évolution cadastrale</h1>

<p> Cette série de cartes interactives présente l’évolution des espaces verts à Lausanne à travers trois périodes clés de transformation urbaine, en s’appuyant sur les différents états du cadastre. Chaque carte met en évidence les changements entre deux étapes successives, en montrant les zones végétalisées inchangées, modifiées, ajoutées ou disparues. Les comparaisons sont organisées ainsi : </p> <ol> <li><strong>Melotte (1727)</strong> vs. <strong>Berney (1830)</strong> – Premiers grands bouleversements liés à l’urbanisation préindustrielle.</li> <li><strong>Berney (1830)</strong> vs. <strong>Cadastre rénové (1880)</strong> – Période de consolidation et de développement urbain structuré.</li> <li><strong>Cadastre rénové (1880)</strong> vs. <strong>Cadastre actuel</strong> – Transformations récentes, requalifications et revalorisation écologique.</li> </ol>
</p>

<!-- Conteneur pour la carte -->
<h2>Melotte (1727) vs. Berney (1830)</h2>
<div id="map-container" style="height: 500px; margin: 1em 0 2em 0;"></div>


<!-- === Texte / images === -->
<section>
  <p>  Cette première carte compare le plan Melotte, dressé en 1727, au cadastre Berney, édité en 1830. Tout d’abord, il convient de noter que certaines zones apparaissant comme « nouvelles », notamment au sud-ouest de la carte, résultent avant tout d’une différence d’emprise entre les deux documents cadastraux : le plan Berney couvre un territoire plus étendu que le plan Melotte
  </p>
  <p> La comparaison entre les plans Melotte (1727) et Berney (1830) révèle une nette réduction des petits espaces verts au cœur de la ville. De nombreux jardins privés, souvent situés à l’arrière des maisons ou entre les îlots bâtis, disparaissent progressivement au profit d’un tissu urbain plus dense et régulier. Ces pertes, bien que modestes en surface, marquent le début d’une longue dynamique de réduction de la végétation intra-muros. </p>
</section>

<!-- === Carte 2 === -->
<h2>Berney (1830) vs. Renove (1880)</h2>
<div id="map2" style="height: 500px; margin: 1em 0 2em 0;"></div>

<!-- === Texte / images === -->
<section>


  
<h3>Disparition des petits espaces verts au centre-ville</h3> <p> La comparaison entre le cadastre Berney de 1830 et le cadastre rénové de 1880 met en évidence une augmentation marquée des disparitions d’espaces verts, en particulier dans le centre-ville lausannois. Cette évolution s’explique par la densification progressive du tissu urbain, avec le comblement des interstices végétalisés — cours, jardins privés ou friches — au profit d’une trame bâtie plus continue. Ces petites pertes ponctuelles, souvent invisibles à grande échelle, deviennent ici perceptibles grâce à la granularité du cadastre. </p> <p> Il est toutefois important de souligner que la méthode utilisée pour générer la carte repose sur une heatmap, qui agrège chaque perte d’une parcelle d’espace vert, quelle que soit sa taille. Cette approche permet de détecter les zones les plus actives en termes de disparition végétale, mais peut introduire un biais : une multitude de petites pertes a visuellement plus de poids qu’une disparition ponctuelle mais massive. Ainsi, certains aménagements d’envergure — comme la construction de la ligne de chemin de fer — peuvent ne pas apparaître clairement dans la visualisation, bien que leur impact ait été structurant à l’échelle de la ville. </p>

<h3>Urbanisation d’Ouchy et infrastructures de liaison</h3> <p> L’urbanisation progressive de la zone d’Ouchy a conduit à la construction du funiculaire Lausanne-Ouchy, inauguré en 1877. Ce nouvel axe de transport a accompagné le développement du quartier, alors en pleine mutation pour accueillir une population croissante et répondre aux ambitions balnéaires des citadins. Sur la carte, on observe à l’est de la ligne de tram plusieurs pertes d’espaces verts, souvent sous forme de petites parcelles disparues ou fragmentées. Il est plausible que ces changements soient liés à un événement ou à une série de projets d’aménagement survenus entre 1830 et 1870, en lien avec le tracé du funiculaire ou avec les premières opérations d’urbanisation du secteur. Ces pertes localisées traduisent une dynamique de transformation rapide de cette zone autrefois plus végétalisée.
</p>

  <img src="img2.jpg" alt="Illustration 2" style="max-width:100%; margin: 1em 0;">
</section>

<!-- === Carte 3 === -->
<h2>Renove (1880) vs. Actuel (2024)</h2>
<div id="map3" style="height: 500px; margin: 1em 0 2em 0;"></div>


<!-- === Texte / images === -->
<section>
<h3>Cluster de changement dans la vallée du Flon</h3> <p> L’un des clusters les plus visibles de cette carte se situe dans la vallée du Flon, une zone qui a connu des transformations majeures à la fin du XIX<sup>e</sup> siècle. Le remblaiement progressif de la plateforme du Flon débuta en 1873 et se poursuivit jusqu’en 1915. Cette opération d’envergure visait à recouvrir la rivière pour créer une vaste zone d’implantation industrielle et logistique en cœur de ville. Elle marque une rupture nette avec le paysage rural qui dominait jusque-là, notamment les nombreuses vignes qui occupaient les pentes et le fond de vallée. </p> <p> Sur l’image ci-dessous, on distingue ces anciennes parcelles viticoles. Ces nombreuses micro-parcelles ont un effet amplificateur sur la heatmap : la métrique utilisée agglomère chaque perte, quelle que soit sa taille, ce qui donne un signal particulièrement intense dans cette zone. </p>
<img src="/data/Flon.jfif" alt="Illustration 3" style="max-width:100%; margin: 1em 0;"> <p style="font-size: 0.9em; color: #555; margin-top: -0.5em;">
<p style="font-size: 0.9em; color: #555; margin-top: -0.5em;"> <em>Photographie d’André Schmid, prise entre 1869 et 1870, montrant la vallée du Flon depuis le Grand-Pont. On y distingue la place Bel-Air, la maison Mercier-Secrétan et les premières traces d’urbanisation du secteur avant le remblaiement. Tirage sur papier albuminé. Collection MHL, cote C_MHL99037.</em> </p>



<h3>Berges du Léman et transformation du littoral</h3>
<p> Cette dernière carte présente la heatmap des différences entre le cadastre rénové (vers 1880) et le cadastre actuel. Plusieurs points intéressants sont à relever. Tout d’abord, on peut apercevoir, sur les plaines de Vidy, une zone distincte où les espaces verts n’ont pas disparu mais ont été modifiés. Une explication plausible de ce phénomène pourrait résider dans la régulation du niveau du Léman. En effet, d’importants travaux ont été entrepris dès 1884 pour réduire la fluctuation du niveau du lac, soit après l’établissement du cadastre rénové. </p> <img src="/data/JeanDubois.jfif" alt="Illustration 3" style="max-width:100%; margin: 1em 0;"> <p style="font-size: 0.9em; color: #555; margin-top: -0.5em;"> <em>Aut. : DuBois, Jean. Aut. tech. : Weber, L.-M. — Titre : <strong>Lausanne</strong>. Date : 1830. Image : MHL114379.</em> </p>
<p> Sur cette illustration datée de 1830, on peut clairement remarquer, à travers le regard de l’artiste, l’aspect marécageux des rives du Léman, entre Dorigny et Vidy. Cette zone, autrefois constituée de terres basses et humides, contraste fortement avec l’aménagement paysager actuel. L’établissement de parcs et d’infrastructures récréatives n’a été rendu possible qu’après d’importants travaux d’aménagement hydrauliques entrepris à la fin du XIX<sup>e</sup> siècle. Ces interventions, notamment la régulation du niveau du lac dès 1884, ont permis de stabiliser les rives, d’assécher certaines zones et de maîtriser les inondations récurrentes. Ces transformations sont aujourd’hui visibles dans le cadastre actuel, qui reflète une occupation du sol profondément remaniée par rapport à l'état naturel représenté sur l’estampe. </p>
<p> On peut également observer une augmentation notable des espaces verts dans cette zone, liée à des remblais successifs et à la prise de terrain sur le lac. Cette avancée artificielle des rives a permis l’aménagement de vastes parcs publics entre Vidy et Bellerive, comme le parc Louis-Bourget ou encore la plage de Vidy, qui n’existaient pas sur les cadastres anciens. Ces espaces, bien que très artificiel, témoigne de la volonté de la ville de Lausanne au cours du XIXème siècle d'utiliser le front lacustre à des fins récréatives.</p>
<h3>Une dynamique différente des autres cartes</h3>
<p> Contrairement aux deux premières heatmaps, où les changements se concentraient principalement dans le centre-ville, cette dernière carte révèle une répartition des modifications en forme de « donut » : les zones de transition ou de disparition des espaces verts se situent désormais en périphérie, tandis que le centre-ville reste relativement stable – non pas par préservation, mais parce qu’il est déjà entièrement urbanisé et ne compte plus de parcelles végétalisées à transformer. Cette évolution spatiale fait écho aux orientations récentes du plan directeur cantonal et aux principes de la LAT (Loi sur l’aménagement du territoire) à l’échelle fédérale, qui encouragent une densification vers l’intérieur plutôt qu’un étalement. Ainsi, les nouvelles dynamiques d’aménagement tendent à préserver les surfaces non bâties en périphérie immédiate tout en consolidant l’existant dans les zones déjà urbanisées. </p>

</section>


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
// Créer la carte et les couches
function createMapAndLayer(mapContainer, geojsonData) {
    if (L.DomUtil.get(mapContainer)._leaflet_id) {
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

    function getColor(status) {
        return {
            "inchangé": "#A9A9A9",     // gris
            "modifié": "#1E90FF",    // bleu
            "nouveau": "#32CD32",   // vert
            "disparu": "#DC143C"    // rouge
        }[status] || "#555555";
    }

    const geoJsonLayer = L.geoJSON(geojsonData, {
        style: function (feature) {
            const s = feature.properties.changement;
            return {
                color: "#000000",
                fillColor: getColor(s),
                fillOpacity: 0.6,
                weight: 1
            };
        },
        onEachFeature: function (feature, layer) {
            const props = feature.properties;
            const popup = `
                <strong>Statut :</strong> ${props.changement}<br>
                <strong>Ancienne classe :</strong> ${props.macro_ev_old || "—"}<br>
                <strong>Nouvelle classe :</strong> ${props.macro_ev_new || "—"}<br>
                <strong>Surface (m²) :</strong> ${Math.round(props.area_m2 || props.area_inter || 0)}
            `;
            layer.bindPopup(popup);
        }
    }).addTo(map);

    layerControl.addOverlay(geoJsonLayer, "Changements");

    // Créer et ajouter une légende
    const legend = L.control({ position: "bottomright" });

    legend.onAdd = function () {
        const div = L.DomUtil.create("div", "legend");

        const categories = {
            "inchangé": "#A9A9A9",
            "modifié": "#1E90FF",
            "nouveau": "#32CD32",
            "disparu": "#DC143C"
        };

        let html = "<strong>Type de changement</strong><br>";
        for (const [label, color] of Object.entries(categories)) {
            html += `<i style="background:${color}"></i> ${label}<br>`;
        }

        div.innerHTML = html;
        return div;
    };

    legend.addTo(map);


    return { map, layerControl };
}

const mapElements = createMapAndLayer("map-container", geojson);
const mapElements2 = createMapAndLayer("map2", geojson2);
const mapElements3 = createMapAndLayer("map3", geojson3);


// // Construire les données pour la heatmap uniquement à partir des zones disparues
// const heatmapData = geojson.features
//     .filter(feature => feature.properties.changement === "disparu")
//     .map(feature => {
//         const geom = feature.geometry;
//         if (geom.type === "Polygon" || geom.type === "MultiPolygon") {
//             // Moyenne simple des points du premier anneau
//             const coords = geom.type === "Polygon" ? geom.coordinates[0] : geom.coordinates[0][0];
//             const lats = coords.map(c => c[1]);
//             const lngs = coords.map(c => c[0]);
//             const lat = lats.reduce((a, b) => a + b) / lats.length;
//             const lng = lngs.reduce((a, b) => a + b) / lngs.length;
//             return [lat, lng, 0.5]; // Intensité fixe ici
//         }
//         return null;
//     })
//     .filter(d => d !== null);

// // Ajouter la heatmap
// const heatmapLayer = L.heatLayer(heatmapData, {
//     radius: 15,
//     blur: 20,
//     maxZoom: 17,
//     gradient: {
//         0.4: 'blue',
//         0.65: 'lime',
//         1: 'red'
//     }
// }).addTo(mapElements.map);


// === Carte 1 : heatmap à partir de geojson ===
const heatmapData1 = geojson.features
    .filter(f => f.properties.changement === "disparu")
    .map(f => {
        const coords = f.geometry.type === "Polygon" ? f.geometry.coordinates[0] : f.geometry.coordinates[0][0];
        const lat = coords.map(c => c[1]).reduce((a, b) => a + b) / coords.length;
        const lng = coords.map(c => c[0]).reduce((a, b) => a + b) / coords.length;
        return [lat, lng]; // pondération par surface
    });

const heatmap1 = L.heatLayer(heatmapData1, {
    radius: 15, blur: 20, maxZoom: 17,
    gradient: { 0.4: 'blue', 0.65: 'lime', 1: 'red' }
}).addTo(mapElements.map);



// === Carte 2 : heatmap à partir de geojson2 ===
const heatmapData2 = geojson2.features
    .filter(f => f.properties.changement === "disparu")
    .map(f => {
        const coords = f.geometry.type === "Polygon" ? f.geometry.coordinates[0] : f.geometry.coordinates[0][0];
        const lat = coords.map(c => c[1]).reduce((a, b) => a + b) / coords.length;
        const lng = coords.map(c => c[0]).reduce((a, b) => a + b) / coords.length;
        return [lat, lng]; // pondération par surface
    });

const heatmap2 = L.heatLayer(heatmapData2, {
    radius: 15, blur: 20, maxZoom: 17,
    gradient: { 0.4: 'blue', 0.65: 'lime', 1: 'red' }
}).addTo(mapElements2.map);



// === Carte 3 : heatmap à partir de geojson3 ===
const heatmapData3 = geojson3.features
    .filter(f => f.properties.changement === "disparu")
    .map(f => {
        const coords = f.geometry.type === "Polygon" ? f.geometry.coordinates[0] : f.geometry.coordinates[0][0];
        const lat = coords.map(c => c[1]).reduce((a, b) => a + b) / coords.length;
        const lng = coords.map(c => c[0]).reduce((a, b) => a + b) / coords.length;
        return [lat, lng]; // pondération par surface
    });

const heatmap3 = L.heatLayer(heatmapData3, {
    radius: 15, blur: 20, maxZoom: 17,
    gradient: { 0.4: 'blue', 0.65: 'lime', 1: 'red' }
}).addTo(mapElements3.map);



mapElements.layerControl.addOverlay(heatmap1, "Zones disparues (heatmap)");
mapElements2.layerControl.addOverlay(heatmap2, "Zones disparues (heatmap)");
mapElements3.layerControl.addOverlay(heatmap3, "Zones disparues (heatmap)");







