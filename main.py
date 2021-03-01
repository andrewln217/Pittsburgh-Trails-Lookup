from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from errors import bp as errors_bp

app = Flask(__name__)

bootstrap = Bootstrap(app)
app.register_blueprint(errors_bp)

@app.route("/")
def home():
    """ Landing Page"""
    return render_template("home.html")

@app.route("/trails")
def trails():
    """ For right now this just loads Andrew's html file """
    return render_template("fetch_trails_data.html")

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True) 
