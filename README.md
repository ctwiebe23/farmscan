# FarmScan

Web application that identifies ideal plots of farmland within a given area
inside the continental United States.

Created by Carston Wiebe and Cale Sigerson for Cornhacks 2025 2: Bananahacks.

# Running FarmScan

To install everything needed to run FarmScan, clone this git repo and navigate
to the directory that contains this README.  From that directory, run:

```
pip install -r ./REQUIREMENTS.txt
```

to gather all Python dependencies.  To serve the website, then run:

```
flask run
```

To develop the website, you will also need to install the NPM dependencies:

```
npm install
```

# Dependencies

- [Flask](https://flask.palletsprojects.com) — Python webapp framework.
- [Watchdog](https://pythonhosted.org/watchdog/) — Enables hot reloading of the
  page during development.
- [PyShp](https://pypi.org/project/pyshp/) — Reads and writes Shapefiles.
- [Leaflet](https://leafletjs.com/) — Renders a map in JavaScript.
- [Sqlite3](https://sqlite.org) — SQL database.

# Developer Dependencies

- [Webpack](https://webpack.js.org/) — Packs JavaScript modules into single
  files.

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
