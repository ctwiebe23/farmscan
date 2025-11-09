from flask import Flask, render_template

app = Flask(__name__)

# html pages
@app.route("/")
def index():
  return render_template("index.html")
  
# json apis
@app.route("/counties/<counties>")
def get_counties(counties: str):
  counties = counties.split(",")
  return counties

# errors
@app.errorhandler(404)
def error_404(error):
  return render_template("404.html"), 404
