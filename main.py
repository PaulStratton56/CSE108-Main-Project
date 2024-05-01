from flask import Flask, render_template, request, redirect, url_for
from models import *
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Players.query.get(user_id)


@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("Login.html")

@app.route("/signup")
def signup():
    return render_template("signUp.html")

@app.route("/home/<userID>")
def home(userID):
    return render_template("homeView.html", username = DEFAULT_USER)

@app.route("/myboards/<userID>")
def myboards(userID):
    return render_template("myboards.html", username = DEFAULT_USER)

@app.route("/join/<userID>")
def join(userID):
    return render_template("join.html", username = DEFAULT_USER)

@app.route("/create/<userID>")
def create(userID):
    return render_template("create.html", username = DEFAULT_USER)

@app.route("/board/<userID>/<boardID>")
def board(userID, boardID):
    return render_template("board.html", username = DEFAULT_USER, boardname = "DefaultBoard")
    
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run()