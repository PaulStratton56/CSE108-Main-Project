from flask import render_template, redirect, url_for
from models import *

DEFAULT_USER = "John Smith"

'''
================================================================
                          Page Routes                           
================================================================
'''  

@app.route("/")
def index():
    return render_template("homeView.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/home/<userID>")
def home(userID):
    return render_template("home.html", username = DEFAULT_USER)

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

@app.route('/debug')
def debug():
    
    print("Debug Complete.")
    return redirect(url_for('index'))


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run()