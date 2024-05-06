from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///playersviewer.db'
DEFAULT_USER = "Paul"

db = SQLAlchemy(app)
app.secret_key = 'secreteKey'
class User(UserMixin, db.Model):
    __tablename__ = "User"
    id          = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name        = db.Column(db.String, nullable=False)
    username    = db.Column(db.String, nullable=False)
    password    = db.Column(db.String, nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Board(db.Model):
    __tablename__ = "Board"
    id          = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name        = db.Column(db.String, nullable=False)
    data        = db.Column(db.String, nullable=False)
    owner_id    = db.Column(db.String, db.ForeignKey("User.id"))
    owner        = db.relationship("User", backref=db.backref("boards", lazy=True))

class UserBoardAssociation(db.Model):
    __tablename__ = "UserBoardAssociation"
    id          = db.Column(db.Integer, primary_key = True, autoincrement=True)
    board_id    = db.Column(db.ForeignKey("Board.id"))
    board        = db.relationship("Board", backref=db.backref("userboardassociation", lazy=True))
    user_id    = db.Column(db.String, db.ForeignKey("User.id"))
    user        = db.relationship("User", backref=db.backref("userboardassociation", lazy=True))


'''
================================================================
                          Page Routes                           
================================================================
'''  

# @app.route("/")
# def index():
#     return redirect(url_for("login"))

# @app.route("/login")
# def login():
#     return render_template("Login.html")

# @app.route("/signup")
# def signup():
#     return render_template("signUp.html")

# @app.route("/home/<userID>")
# def home(userID):
#     return render_template("homeView.html", username = DEFAULT_USER)

# @app.route("/myboards/<userID>")
# def myboards(userID):
#     return render_template("myboards.html", username = DEFAULT_USER)

# @app.route("/join/<userID>")
# def join(userID):
#     return render_template("join.html", username = DEFAULT_USER)

# @app.route("/create/<userID>")
# def create(userID):
#     return render_template("create.html", username = DEFAULT_USER)

# @app.route("/board/<userID>/<boardID>")
# def board(userID, boardID):
#     return render_template("board.html", username = DEFAULT_USER, boardname = "DefaultBoard")

'''
================================================================
                          Backend Routes                           
================================================================
''' 



if __name__ == "__main__":
    print("Wrong file! Please run 'main.py'.")