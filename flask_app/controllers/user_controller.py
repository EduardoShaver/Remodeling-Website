# from types import MethodDescriptorType
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.quote import Quote
from flask_app import app
# from flask_app.config.mysqlconnection import connectToMySQL

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)




@app.route("/users")
def display_users():
    if "uuid" not in session:
        flash("Must log in!")
        return redirect("/")

    return render_template("users.html", all_users= User.get_all(), user = User.get_by_id({"id": session['uuid']}))




@app.route("/login", methods = ['POST'])
def login():
    print("logging in")
    if not User.login_validate(request.form):
        return redirect("/")

    user = User.get_by_email({"email": request.form['email']})
        #uuid = unique user id
    session['uuid'] = user.id
        
    return redirect('/admin')

@app.route("/logout")
def logout():
    session.clear()

    return redirect("/")

@app.route("/")
def index():

    return render_template("homepage.html")




@app.route("/contact_us")
def contactUs():
    return render_template("contact_us.html")

@app.route("/other_projects")
def otherProjects():
    return render_template("other_projects.html")

