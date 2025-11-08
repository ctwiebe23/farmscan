# FarmScan

Web application that identifies ideal plots of farmland within a given area
inside the continental United States.

# Dependencies

- [Flask](https://flask.palletsprojects.com) — Python webapp framework.
- [Watchdog](https://pythonhosted.org/watchdog/) — Enables hot reloading of the
  page during development.
- [PyShp](https://pypi.org/project/pyshp/) — Reads and writes Shapefiles.

# Index

- `./app` contains the source files for the Flask webapp.
  - `./app/static` contains static files like CSS, JavaScript, and images.
  - `./app/templates` contains Jinja templates, mostly for HTML pages.
  - `./app/__init__.py` contains the Flask entrypoint and defines the app routes.
- `./justfile` contains the shell commands needed to run and develop the app.
- `./REQUIREMENTS.txt` contains all the Python dependencies needed by `pip`
