import { map, tileLayer } from "leaflet";

const main = () => {
  const params = new URLSearchParams(window.location.search);
  const bounds = [
    [params.get("minlat"), params.get("minlon")],
    [params.get("maxlat"), params.get("maxlon")],
  ];

  const leaflet_map = map("leaflet-map").fitBounds(bounds);

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
