import { map, polygon, tileLayer } from "leaflet";

const main = async () => {
  const submit_button = document.getElementById("submit");
  if (!submit_button) {
    console.error("no submit button");
    return;
  }
  const no_data_found = document.getElementById("no-data-found");
  if (!no_data_found) {
    console.error("no data not found warning");
    return;
  }
  const loading_animation = document.getElementById("loading-animation");
  if (!loading_animation) {
    console.error("loading animation not found");
    return;
  }

  loading_animation.classList.remove("hidden");
  const params = new URLSearchParams(window.location.search);
  const api_input = ["maxlon", "minlat", "minlon", "maxlat"].map((name) =>
    params.get(name)
  );
  const api_resp =
    (await fetch("/api/find-best/" + api_input.join(","))
      .then((resp) => resp.json())
      .catch((reason) => console.log(reason))) || {};

  let bounds;
  if (api_resp.polygons.length == 0) {
    bounds = [
      [params.get("minlat"), params.get("minlon")],
      [params.get("maxlat"), params.get("maxlon")],
    ];

    no_data_found.classList.remove("hidden");
  } else {
    bounds = [
      [api_resp.minlat, api_resp.minlon],
      [api_resp.maxlat, api_resp.maxlon],
    ];
  }

  const leaflet_map = map("leaflet-map").fitBounds(bounds);

  tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution:
      '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
  }).addTo(leaflet_map);

  for (const polygon_points of api_resp.polygons) {
    polygon(polygon_points, { color: "green" }).addTo(leaflet_map);
  }
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
