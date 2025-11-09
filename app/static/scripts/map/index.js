import { map, tileLayer } from "leaflet";

const main = () => {
  const submit_button = document.getElementById("submit");
  if (!submit_button) {
    console.error("no submit button");
    return;
  }
  const loading_animation = document.getElementById("loading-animation");
  if (!loading_animation) {
    console.error("loading animation not found");
    return;
  }

  loading_animation.classList.remove("hidden");
  const leaflet_map = map("leaflet-map").fitBounds([
    [41.4, -99],
    [41.7, -98],
  ]);

  tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution:
      '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
  }).addTo(leaflet_map);
  loading_animation.classList.add("hidden");

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
