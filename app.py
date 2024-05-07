from flask import render_template, redirect, url_for, request
import json
from models import *

DEFAULT_USER = "John Smith"
EMPTY = "".encode()
NO_BOARDS = {"boards" : {}}
SUCCESS = {"complete" : True}
FAILURE = {"complete" : False}

'''
================================================================
                          Page Routes                           
================================================================
'''  

@app.route("/")
def index():
    return redirect(url_for('loginPage'))

@app.route("/loginPage", methods=["GET", "POST"])
def loginPage():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        
        username = request.form.get('username')
        password = request.form.get('password')

        artist = db.session.query(Artist).filter(Artist.username == username).first()

        if artist != None:
            if artist.passwordIsValid(password) == True:
                return redirect(url_for("login", userID = artist.user_id))

    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    elif request.method == "POST":

        username = str(request.form.get('username'))
        name = str(request.form.get('name'))
        password = str(request.form.get('password'))
        confirmationPassword = str(request.form.get('password'))

        usernameStatus = checkUsername(username)

        if usernameStatus == "USERNAME_OK":

            passwordStatus = checkPassword(password, confirmationPassword)

            if passwordStatus == "PASSWORD_OK":

                newUser = Artist(name = name, username = username, password = password)

                db.session.add(newUser)
                db.session.commit()

                return redirect(url_for('home', userID = newUser.user_id))

            else:
                print("ERROR: " + passwordStatus)
        
        else:
            print("ERROR: " + usernameStatus)

    return render_template("signup.html")

@app.route("/home/<userID>")
def home(userID):

    artist = db.session.query(Artist).filter(Artist.user_id == userID).first()
    artistName = artist.name

    return render_template("homeView.html", userID = userID, name = artistName)

@app.route("/board/<userID>/<boardID>")
def board(userID, boardID):
    return render_template("board.html", userID = userID, boardID = boardID)

@app.route("/board")
def boardonly():
    return render_template("board.html")

'''
================================================================
                          Backend Routes                           
================================================================
''' 

@app.route('/login/<userID>')
def login(userID):
    return redirect(url_for('home', userID = userID))

@app.route('/logout/<userID>')
def logout(userID):
    return redirect(url_for('loginPage'))

@app.route('/addArtistToBoard', methods=["POST"])
def addArtistToBoard():
    response = {
        "userExists" : True
    }

    newArtistUsername = json.loads(request.data)["username"]
    artist = db.session.query(Artist).filter(Artist.username == newArtistUsername).first()
    
    if artist != None:
        response["name"] = artist.name
    else:
        response["userExists"] = False
    
    return json.dumps(response)

@app.route('/createBoard', methods=["POST"])
def createBoard():
    requestData = json.loads(request.data)
    boardName = requestData['name']
    boardOwner = db.session.query(Artist).filter(Artist.user_id == requestData['ownerID']).first()
    
    newBoard = Board(name = boardName, boardData = EMPTY, owner = boardOwner)  
    db.session.add(newBoard)
    db.session.commit()

    link = UserBoardAssociation(user = boardOwner, board = newBoard)
    db.session.add(link)
    db.session.commit()

    collaboratorUsernames = requestData['artistUsernames']
    for username in collaboratorUsernames.values():
        collaborator = db.session.query(Artist).filter(Artist.username == username).first()
        
        link = UserBoardAssociation(user = collaborator, board = newBoard)
        db.session.add(link)
        db.session.commit()

    responseBody = {
        "userID" : boardOwner.user_id,
        "boardID" : newBoard.board_id
    }

    responseBody = json.dumps(responseBody)

    return responseBody

@app.route('/joinBoard/<userID>', methods=["POST"])
def joinBoard(userID):
    boardID = request.form.get('boardID')

    artist = db.session.query(Artist).filter(Artist.user_id == userID).first()
    board = db.session.query(Board).filter(Board.board_id == boardID).first()

    if artist == None or board == None:
        return redirect(url_for('home', userID = userID))
    
    else:
        association = UserBoardAssociation(user = artist, board = board)
        db.session.add(association)
        db.session.commit()

        return redirect(url_for('board', userID = userID, boardID = boardID))

@app.route('/myBoards/<userID>')
def myBoards(userID):
    artist = db.session.query(Artist).filter(Artist.user_id == userID).first()

    if artist != None:
        myBoards = db.session.query(Board).join(UserBoardAssociation).filter(UserBoardAssociation.user_id == userID).all()

        responseBody = {}

        for boardIndex,board in enumerate(myBoards):
            boardInfo = {}
            
            boardInfo["name"] = board.name
            
            if board.owner == artist:
                boardInfo["owned"] = True
            else:
                boardInfo["owned"] = False
            
            boardInfo["boardID"] = board.board_id

            collaborators = db.session.query(Artist).join(UserBoardAssociation).filter(UserBoardAssociation.board == board).all()
            collaboratorInfo = {}
            for collaboratorIndex, collaborator in enumerate(collaborators):
                if collaborator != artist:
                    collaboratorInfo[collaboratorIndex] = collaborator.name
            boardInfo["collaborators"] = collaboratorInfo

            responseBody[boardIndex] = boardInfo            

            
        return responseBody

    else:
        print("Could find this user! Something went wrong.")
        return json.dumps(NO_BOARDS)

@app.route('/deleteBoard/<boardID>', methods=["DELETE"])
def deleteBoard(boardID):
    responseBody = {
        "refreshList" : False
    }

    board = db.session.query(Board).filter(Board.board_id == boardID).first()
    if board != None:
        associations = db.session.query(UserBoardAssociation).filter(UserBoardAssociation.board == board).all()
        for association in associations:
            db.session.delete(association)
        db.session.delete(board)
        db.session.commit()
        responseBody["refreshList"] = True
    
    return responseBody

@app.route('/leaveBoard/<boardID>/<userID>', methods=["DELETE"])
def leaveBoard(boardID, userID):
    responseBody = {
        "refreshList" : False
    }

    board = db.session.query(Board).filter(Board.board_id == boardID).first()
    user = db.session.query(Artist).filter(Artist.user_id == userID).first()

    if board != None and user != None:
        association = db.session.query(UserBoardAssociation).filter(UserBoardAssociation.board == board, UserBoardAssociation.user == user).first()
        if association != None:
            db.session.delete(association)
            db.session.commit()
            responseBody["refreshList"] = True

    return responseBody

@app.route('/saveBoard', methods=["POST"])
def saveBoard():
    requestData = json.loads(request.data)
    
    board = db.session.query(Board).filter(Board.board_id == requestData["boardID"]).first()
    if board != None:
        boardData = requestData["boardData"]

        board.boardData = boardData.encode()
        db.session.commit()

        return SUCCESS
    else:
        return FAILURE

@app.route('/loadBoard/<boardID>', methods=["GET"])
def loadBoard(boardID):
    responseBody = {
        "boardData" : None
    }
    
    board = db.session.query(Board).filter(Board.board_id == boardID).first()
    if board != None:
        boardData = board.boardData.decode()
        responseBody["boardData"] = boardData

    return responseBody

@app.route('/debug')
def debug():
    
    print("Debug Complete.")
    return redirect(url_for('index'))

'''
================================================================
                          Other Functions                           
================================================================
''' 

def checkUsername(username):
    returnCode = "USERNAME_OK"
    artists = db.session.query(Artist).all()
    for artist in artists:
        if artist.username == username:
            returnCode = "USERNAME_DUPLICATE"
    
    return returnCode

def checkPassword(password, confirmationPassword):
    returnCode = "PASSWORD_OK"

    #Must be more than 5 characters.
    if len(password) <= 5:
        returnCode = "PASSWORD_TOO_SHORT"

    #Cannot contain spaces.
    elif " " in password:
        returnCode = "PASSWORD_HAS_SPACE"

    #Must contain a special character.
    elif password.isalnum():
        returnCode = "PASSWORD_MISSING_CHARACTER"

    #Must match the confirmation password.
    elif password != confirmationPassword:
        returnCode = "PASSWORD_NOT_MATCHING"

    return returnCode

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run()