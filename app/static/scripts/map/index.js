import { map, tileLayer } from "leaflet";

const main = () => {
  const leaflet_map = map("leaflet-map").fitBounds([
    [41.4, -99],
    [41.7, -98]
  ]);

  const tiles = tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution:
      '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
  }).addTo(leaflet_map);
};

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", main);
} else {
  main();
}
