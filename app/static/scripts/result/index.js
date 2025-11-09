import { map, polygon, tileLayer } from "leaflet";

const main = async () => {
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
      // TODO: say none found
    ];
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
    polygon(polygon_points, { color: "green" }).addTo(
      leaflet_map
    );
  }
};

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", main);
} else {
  main();
}
