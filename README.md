# FarmScan

Web application that identifies ideal plots of farmland within a given area
inside the continental United States.

Created by Carston Wiebe and Cale Sigerson for Cornhacks 2025 2: Bananahacks.

# Running FarmScan

Navigate to the root directory (that contains this README) and run:

```
flask run
```

# Dependencies

- [Flask](https://flask.palletsprojects.com) — Python webapp framework.
- [Watchdog](https://pythonhosted.org/watchdog/) — Enables hot reloading of the
  page during development.
- [PyShp](https://pypi.org/project/pyshp/) — Reads and writes Shapefiles.
- [Leaflet](https://leafletjs.com/) — Renders a map in JavaScript.
- [Sqlite3](https://sqlite.org) — SQL database.

# Index

- `./app` contains the source files for the Flask webapp.
  - `./app/static` contains static files like CSS, JavaScript, and images.
  - `./app/templates` contains Jinja templates, mostly for HTML pages.
  - `./app/__init__.py` contains the Flask entrypoint and defines the app routes.
- `./data` contains shapefiles.
- `./db` contains the SQLite3 database.
- `./resources` contains unneeded files that were a part of the development of
  the app.
- `./justfile` contains the shell commands needed to run and develop the app.
- `./REQUIREMENTS.txt` contains all the Python dependencies needed by `pip`

# Processes

## Getting data

All of our data was taken from https://websoilsurvey.nrcs.usda.gov/app/WebSoilSurvey.aspx and was intially processed in QGIS. Using QGIS
we created a SQLite table with all the data that we would need for the county we chose. These table records could then be linked to specific surveys
conducted in the county. 

## Farmland Viability Algorithm

For each survery within the givin bounding box, the algorithm checked certain records to see if their values were deternimed to be beneficial and if so, a "viability score"
was attributed to that survery. By looking through multiple records that existed for most surveys, in our initial area, we were able to reduce our initial surverys (about 8400)
down to just 21 surveys. In our criteria for determining if a beneficial score would be gievn to each survey, we used thresholds that were supported by online resources.

### Resources

https://soiltesting.cahnr.uconn.edu/soil-ph-and-management-suggestions/
https://shunpoly.com/article/what-does-a-high-plasticity-index-mean
https://en.wikipedia.org/wiki/Soil

