from flask import Flask, render_template, request

app = Flask(__name__)

# html pages
@app.route("/")
def index():
  return render_template("index.html")

@app.route("/bbox")
def bbox_form():
  return render_template("bbox.html")

@app.route("/result")
def result():
  minlat = request.args.get("minlat", float)
  maxlat = request.args.get("maxlat", float)
  minlon = request.args.get("minlon", float)
  maxlon = request.args.get("maxlon", float)
  return render_template("result.html", minlat=minlat, maxlat=maxlat, maxlon=maxlon, minlon=minlon)

# error handling
@app.errorhandler(404)
def error_404(error):
  return render_template("404.html"), 404
