function toggle(selectedPage) {
    const contents = document.querySelectorAll('.tabcontent');
    contents.forEach(content => content.style.display = 'none');
    const links = document.querySelectorAll('.tablink');
    links.forEach(link => link.classList.remove('active'));
    document.getElementById(selectedPage).style.display = 'block';
    event.currentTarget.classList.add('active');
}
document.querySelector('#defaultOpen').click();


function addCollaborator() {
    let username = document.getElementById('collaborator').value;
    
    let addUserRequest = new XMLHttpRequest();
    addUserRequest.open("POST", '/addArtistToBoard', true)
    addUserRequest.setRequestHeader('Content-Type', 'application/json');

    let requestBody = {
        "username" : username
    }
    requestBody = JSON.stringify(requestBody);

    addUserRequest.send(requestBody);

    addUserRequest.onload = function(){
        let response = JSON.parse(this.responseText);

        if(response["userExists"] === true){
            let list = document.getElementById('collaboratorsList');
            
            let newRow = document.createElement('tr');
            let newUsername = document.createElement('td');
            newUsername.innerText = username;
            let newName = document.createElement('td');
            newName.innerText = response["name"];
            
            newRow.appendChild(newUsername);
            newRow.appendChild(newName);
            list.appendChild(newRow);
        }
        else{
            alert("Couldn't find that person. Double check the username!")
        }


    }

}

function createBoard(ownerID) {

    let createBoardRequest = new XMLHttpRequest();
    createBoardRequest.open("POST", '/createBoard', true);
    createBoardRequest.setRequestHeader('Content-Type', 'application/json');

    let requestBody = {
        "ownerID" : Number(ownerID),
        "name" : "",
        "artistUsernames" : {}
    };
    
    let boardName = document.getElementById('boardName').value;
    if(boardName == ""){
        alert("Give your board a name first!");
        return;
    }
    requestBody["name"] = boardName;

    let collaboratorTable = document.getElementById('collaboratorsList');
    for (var i = 1, row; row = collaboratorTable.rows[i]; i++) {
        requestBody["artistUsernames"][i] = row.cells[0].innerText;
    }

    console.log(requestBody);

    requestBody = JSON.stringify(requestBody);

    createBoardRequest.send(requestBody);

    createBoardRequest.onload = function(){
        let response = JSON.parse(this.responseText);

        let boardURL = "/board/" + response["userID"] + '/' + response["boardID"];

        window.location.assign(boardURL);
    }

}