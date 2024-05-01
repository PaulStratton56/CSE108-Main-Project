from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DEFAULT_USER = "Paul"

'''
================================================================
                          Page Routes                           
================================================================
'''  

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login")
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

'''
================================================================
                          Backend Routes                           
================================================================
''' 



if __name__ == "__main__":
    app.run()