---
title: Slider 1800–1830–2024
toc: false
---

<label for="time-slider">
  Année : <strong id="time-value">1830</strong>
</label>
<br>
<input
  type="range"
  id="time-slider"
  min="0"
  max="2"
  step="any"
  value="1"
  style="width:100%; max-width:400px; margin:1em 0;"
>
<!-- Tick labels sous la barre -->
<div
  style="width:100%; max-width:400px; display:flex; justify-content:space-between; font-size:0.8em; margin-top:-0.5em;"
>
  <span>1800</span><span>1830</span><span>2024</span>
</div>

<script>
// 1) Références
const slider = document.getElementById("time-slider");
const output = document.getElementById("time-value");

// 2) Fonction de mapping continu entre 3 étapes
function updateYear() {
  const t = parseFloat(slider.value);
  let y;
  if (t <= 1) {
    // interpolation 1800 → 1830
    y = "1800 - 1830";
  } else {
    // interpolation 1830 → 2024
    y = "1830 - 2024";
  }
  output.textContent = y;

  // ← Ici tu peux appeler ta fonction de mise à jour de carte/graphique :
  // updateMapForYear(y);
}

// 3) Écouteur et initialisation
slider.addEventListener("input", updateYear);
updateYear();
</script>
