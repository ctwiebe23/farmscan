import { map, tileLayer } from "leaflet";

const main = () => {
  const submit_button = document.getElementById("submit");
  if (!submit_button) {
    console.error("no submit button");
    return;
  }

  const leaflet_map = map("leaflet-map").fitBounds([
    [41.4, -99],
    [41.7, -98],
  ]);

  const tiles = tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution:
      '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
  }).addTo(leaflet_map);

  submit_button.addEventListener("click", () => {
    const bounds = leaflet_map.getBounds();
    const bounds_obj = {
      minlat: bounds.getSouth(),
      maxlat: bounds.getNorth(),
      minlon: bounds.getEast(),
      maxlon: bounds.getWest(),
    };
    const params = new URLSearchParams(bounds_obj);

    window.open("/result?" + params, "_self");
  });
};

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", main);
} else {
  main();
}
