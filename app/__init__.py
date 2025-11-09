from flask import Flask, render_template, request, g, abort
import sqlite3

app = Flask(__name__)

#=============================================================================#
# HTML pages
#=============================================================================#
@app.route("/")
def index():
  return render_template("index.html")

@app.route("/bbox")
def bbox_form():
  return render_template("bbox.html", subtitle="Lat & Lon")

@app.route("/map")
def map_form():
  return render_template("map.html", subtitle="Map")

@app.route("/result")
def result():
  minlat = get_search_param("minlat", float)
  maxlat = get_search_param("maxlat", float)
  minlon = get_search_param("minlon", float)
  maxlon = get_search_param("maxlon", float)
  
  if any(map(lambda x: x is None, [minlat, maxlat, minlon, maxlon])):
    abort(400)
  
  return render_template("result.html", subtitle="Results", minlat=minlat, maxlat=maxlat, maxlon=maxlon, minlon=minlon)

#=============================================================================#
# Error handling
#=============================================================================#
@app.errorhandler(404)
def error_404(error):
  return render_template("error.html", error_code=404, error_message="Page not found"), 404

@app.errorhandler(400)
def error_404(error):
  return render_template("error.html", error_code=400, error_message="Bad request"), 400

#=============================================================================#
# Helper functions
#=============================================================================#
def get_search_param(name: str, type: type):
  "Gets a URL search parameter with a given name and type."
  return request.args.get(name, None, type=type)

def get_db():
  "Returns the database."
  # g contains global variables.  We will store the db connection there, and
  # then retrieve it on subsequent calls.
  if "db" not in g:
    g.db = sqlite3.connect("./db/soil_data.sqlite")
  return g.db

def close_db():
  "Closes the database."
  db = g.pop("db", None)
  if db is not None:
    db.close()