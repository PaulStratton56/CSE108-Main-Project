from flask import Flask, render_template, request, redirect, url_for
from models import *
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

CONFIRM_COLOR = "green"
ERROR_COLOR = "red"
NONE_COLOR = "black"

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
    if request.method == "GET":
        return render_template("Login.html")
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        user = Players.query.filter_by(playerName=username).first()

        if user and user.check_password(password):
            login_user(user)
            message = None
            messageColor = NONE_COLOR
            if isinstance(user, Players):
                message="Welcome, player " + user.playerName + "!"
                messageColor = CONFIRM_COLOR
                return redirect(url_for('home', userID=user.id))
            else:
                message = "ERROR: Incorrect username or password. Please try again."
                messageColor = ERROR_COLOR
        else:
            message="ERROR: No user found by the name of " + username + ". Please try again."
            messageColor = ERROR_COLOR
        return render_template("Login.html", message = message, messageColor = messageColor)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signUp.html")
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        new_player = Players(playerName=username, boardName=DEFAULT_USER)
        
        
        new_player.set_password(password)

        db.session.add(new_player)
        db.session.commit()

        login_user(new_player)
        
        return redirect(url_for("home", userID=new_player.id))
        

@app.route("/home/<userID>")
def home(userID):
    return render_template("homeView.html", username = "test boy")
    
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