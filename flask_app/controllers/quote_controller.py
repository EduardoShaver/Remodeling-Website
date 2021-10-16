from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.quote import Quote
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route("/request_a_quote")
def RequestQuote():
    return render_template("request_a_quote.html")

@app.route("/new_quote", methods = ['POST'])
def createQuote():
    print(request.form)
    Quote.create(request.form)
    return redirect("/")

@app.route("/quotes/<int:id>/delete")
def deleteQuote(id):
    quote = Quote.get_one({"id": id})
    
    Quote.delete({"id": id})
    return redirect("/admin")




@app.route("/admin")
def admin():
    if "uuid" not in session:
        return redirect("/")
    
    return render_template(
        "admin.html",
        logged_in_user = User.get_by_id({"id": session['uuid']}),
        all_quotes = Quote.get_all()
        )

