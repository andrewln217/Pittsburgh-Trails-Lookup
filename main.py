from flask import Flask, render_template, request, url_for, redirect, session
from flask_bootstrap import Bootstrap
from errors import bp as errors_bp

app = Flask(__name__)
app.secret_key = "hello"
bootstrap = Bootstrap(app)
app.register_blueprint(errors_bp)

@app.route("/home")
def home():
    if "user" in session:
        user = session["user"]
        return render_template("home.html")
    else:
        return redirect(url_for("login"))
    return render_template("home.html")

@app.route("/trails")  
def trails():
    """ loads map_page.html """
    return render_template("map_page.html")

@app.route('/search', methods=['GET', 'POST'])
def search():
  form = SearchForm()
  if not form.validate_on_submit():
    return redirect(url_for('home'))
  return redirect((url_for('search_results', query=form.search.data)))

@app.route('/', methods=["POST","GET"])
def login():
    session.permanent = False
    if request.method == "POST":
        user = request.form['email']
        password = request.form['password']
        session["user"] = user
        return redirect(url_for("home"))
    else:
        if "user" in session:
            return redirect(url_for("home"))
        return render_template("login.html")
        
@app.route("/profile")
def profile():
    return render_template("profile.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True) 
