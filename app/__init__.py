import os
import sqlite3
from flask import Flask, render_template, request, g, abort
import shapefile

app = Flask(__name__)

#=============================================================================#
# HTML pages
#=============================================================================#
@app.route("/")
def index():
  "The landing page."
  return render_template("index.html")

@app.route("/bbox")
def bbox_form():
  "Input form that prompts the user for coordinates."
  return render_template("bbox.html", subtitle="Lat & Lon")

@app.route("/map")
def map_form():
  "Interactive map to select coordinates."
  return render_template("map.html", subtitle="Map")

@app.route("/result")
def result():
  "The results of searching a given bounding box."
  minlon = get_search_param("minlon", float)
  minlat = get_search_param("minlat", float)
  maxlon = get_search_param("maxlon", float)
  maxlat = get_search_param("maxlat", float)

  if any(map(lambda x: x is None, [minlat, maxlat, minlon, maxlon])):
    abort(400)
  
  return render_template("result.html", subtitle="Results")

#=============================================================================#
# JSON API
#=============================================================================#
@app.route("/api/find-best/<bbox>")
def find_best_api(bbox: str):
  "Finds the best farmland within the given bounding box."
  bbox = bbox.split(",")
  
  if len(bbox) != 4:
    return { "error": f"Bad request: {len(bbox)} coords received" }
  
  try:
    bbox = list(map(float, bbox))
  except:
    return { "error": "Bad request: coords are not floats" }
  
  viable_shapes = find_best_viable_shapes(bbox)
  
  if len(viable_shapes) == 0:
    return { "polygons": [] }
  
  viable_bbox = get_bbox_from_shape_records(viable_shapes)

  return {
    "polygons": list(map(shape_record_to_leaflet_polygon, viable_shapes)),
    "maxlon": viable_bbox[0],
    "minlat": viable_bbox[1],
    "minlon": viable_bbox[2],
    "maxlat": viable_bbox[3],
  }

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
def debug(msg: str):
  "Print a debug message to the console."
  app.logger.debug(msg)

def get_search_param(name: str, type: type):
  "Gets a URL search parameter with a given name and type."
  return request.args.get(name, None, type=type)

def get_db() -> sqlite3.Connection:
  "Returns the database."
  # g contains global variables.  We will store the db connection there, and
  # then retrieve it on subsequent calls.
  if "db" not in g:
    g.db = sqlite3.connect(os.getcwd() + "/db/soil_data.sqlite")
  return g.db

def close_db():
  "Closes the database."
  db = g.pop("db", None)
  if db is not None:
    db.close()
    
def shape_record_to_leaflet_polygon(shape_record: shapefile.ShapeRecord) -> list[list[str]]:
  "Converts a shape record from PyShp to a polygon usable by leaflet."
  points = []
  for point in shape_record.shape.points:
    points.append(list(reversed(list(map(str, point)))))
  return points
    
def get_bbox_from_shape_records(shape_records: shapefile.ShapeRecords) -> shapefile.BBox:
  "Returns a bounding box that contains all the given shape records."
  minlon = -180
  minlat = -90
  maxlon = 180
  maxlat = 90
  
  for shape_record in shape_records:
    bbox = shape_record.shape.bbox
    if bbox[0] > minlon:
      minlon = bbox[0]
    if bbox[1] > minlat:
      minlat = bbox[1]
    if bbox[2] < maxlon:
      maxlon = bbox[2]
    if bbox[3] < maxlat:
      maxlat = bbox[3]
      
  return (minlon, minlat, maxlon, maxlat)
    
def find_best_viable_shapes(bbox: shapefile.BBox) -> dict[float: shapefile.ShapeRecords]:
  "Finds the best viables shapes within the bounding box."
  shape_file = shapefile.Reader(os.getcwd() + "/data/soilmu_a_ne175")
  conn = get_db()
  cursor = conn.cursor()
  shape_records = shape_file.shapeRecords()
  enclosed_shapes = shapefile.ShapeRecords([])

  for shape_record in shape_records:
    if shapefile.bbox_contains(bbox, shape_record.shape.bbox):
      enclosed_shapes.append(shape_record)
        
  max_viability_score = 0
  viable_shape_records = shapefile.ShapeRecords([])
  scored_shape_records = {float: shapefile.ShapeRecords([])}
  for shape_record in enclosed_shapes:
    viability_score = 0
    query = "select tfact,flodfreqdcd,iccdcdpct,ph1to1h2o_r,pi_r,om_r from joined_layer where mukey = ?"
    mukey = shape_record.record[3]
    
    if mukey is None:
      debug("no mukey found")
    else:
      q_result = cursor.execute(query, (mukey,))
      result = q_result.fetchone()
      tfact = result[0]
      flood_freq = result[1]
      soil_capability = result[2]
      ph_level = result[3]
      p_index = result[4]
      organic_matter = result[5]
      
      if result is None:
        debug("invalid query")
      elif (tfact is None):
        debug(mukey)
      elif (tfact):
        if int(tfact) > 4:
            viability_score += 1
      
      if isinstance(flood_freq, str):
        if flood_freq == "None" or flood_freq == "Occasional":
            viability_score += 1
              
      if isinstance(soil_capability, int):
        viability_score -= int(soil_capability) / 100
      
      if (ph_level is not None and ph_level):
        if isinstance(float(ph_level), float):
          if (float(ph_level) > 6 and float(ph_level) < 7.5):
            if (float(ph_level) <= 6.8):
              viability_score += 1
            viability_score += 1
      
      if (p_index is not None and p_index):
        if isinstance(float(p_index), float):
          if (float(p_index) > 15 and float(p_index) < 35):
            viability_score += 1
      
      if (organic_matter is not None and organic_matter):
        if isinstance(float(organic_matter), float):
          if (float(organic_matter) >= 3 and float(organic_matter) <= 6):
            viability_score += 1
      
      if viability_score < 0:
        viability_score = 0
      if viability_score > max_viability_score:
        max_viability_score = viability_score
        scored_shape_records[viability_score] = viable_shape_records
        viable_shape_records.clear()
        viable_shape_records.append(shape_record)
      elif viability_score == max_viability_score:
        viable_shape_records.append(shape_record)

  close_db()
  return viable_shape_records
