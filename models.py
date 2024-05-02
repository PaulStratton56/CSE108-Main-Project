from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, BLOB, ForeignKey, Integer
from sqlalchemy.orm import relationship


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///boards.db'
db = SQLAlchemy(app)

class Artist(db.Model):
    __tablename__ = 'Artist'
    user_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    
    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password

class Board(db.Model):
    __tablename__ = 'Board'
    board_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    boardValues = Column(BLOB, nullable=False)
    owner_id = Column(Integer, ForeignKey('Artist.user_id'), nullable=False)
    owner = relationship(Artist, backref=db.backref('Boards', lazy=True))

    def __init__(self, name, boardValues, owner):
        self.name = name
        self.boardValues = boardValues
        self.owner_id = owner.user_id
        self.owner = owner

class UserBoardAssociation(db.Model):
    __tablename__ = 'UserBoardAssociation'
    association_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Artist.user_id'), nullable=False)
    board_id = Column(Integer, ForeignKey('Board.board_id'), nullable=False)
    user = relationship(Artist)
    board = relationship(Board)

    def __init__(self, user, board):
        self.user_id = user.user_id
        self.board_id = board.board_id
        self.user = user
        self.board = board
