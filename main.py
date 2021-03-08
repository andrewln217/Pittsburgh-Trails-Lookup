from flask import Flask, render_template, request, url_for, redirect, session
from flask_bootstrap import Bootstrap
from errors import bp as errors_bp
from google.cloud import datastore
import json

from user import UserStore, generate_credentials, hash_password


datastore = datastore.Client()
userstore = UserStore(datastore)

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

@app.route("/create", methods=["POST","GET"])
def create():
    session.permanent = False
    if request.method == "GET":
        user = get_user()
        if user:
            return redirect("/home")
        return render_template("create.html")
    else:    
        user = request.form.get("user_email")
        password = request.form.get("password")
        if user_email in userstore.list_existing_users():
            return render_template(url_for("create"), error="User with that email already exists")
        userstore.store_new_credentials(generate_credentials(user_email, password))
        session["user"] = user
        return redirect("/home")

@app.route("/profile")
def profile():
    return render_template("profile.html")

def get_user():
    return session.get("user", None)

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True) 