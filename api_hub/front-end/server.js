'use strict';

//Set up express
const express = require('express');
const app = express();

// Setup request
const request = require("request");

//Setup socket.io
const server = require('http').Server(app);
const io = require('socket.io')(server);

//Setup static page handling
app.set('view engine', 'ejs');
app.use('/static', express.static('public'));

//Handle client interface on /
app.get('/', (req, res) => {
  res.render('client');
});

let socketInfo ={};
let azureKey = "?code=9xUsI5p_jifbfrQD9-eV8dRmNoR0i3jYcnIu-poWtposAzFuclLXkw==";

// URL of the backend API
const BACKEND_ENDPOINT = 'https://apihub-et2g21.azurewebsites.net'; // 'http://localhost:7071';

//Start the server
function startServer() {
    const PORT = process.env.PORT || 8080;
    server.listen(PORT, () => {
        console.log(`Server listening on port ${PORT}`);
    });
}

function handleRegister(socket, registerJSON){

    //Backend Register Call
    azurePOST("/api/userRegister", registerJSON).then(
        function(response) {
            console.log("Success:");
            console.log(response);
            if (response["result"]) {
                socket.emit("confirm_register", registerJSON)
                handleLogin(socket, registerJSON)
            }
            else {
                socket.emit("error", response["msg"])
            }
        },
        function (error) {
            console.error("Error:");
            console.error(error);
        }
    );
}

function handleLogin(socket, loginJSON){

    //Backend Register Call
    azurePOST("/api/userLogin", loginJSON).then(
        function(response) {
            console.log("Success:");
            console.log(response);
            if (response["result"]) {
                socket.emit("confirm_login", loginJSON)
            }
            else {
                socket.emit("error", response["msg"])
            }
        },
        function (error) {
            console.error("Error:");
            console.error(error);
        }
    );
}

function azurePOST(path,body){
    return new Promise((success, failure) => {
		request.post(BACKEND_ENDPOINT + path + azureKey, {
			json: true,
			body: body
		}, function(err, response, body) {
            if (err) {
                failure(err);
            } else {
			    success(body);
            }
		});
	});
}

function azureDELETE(path, body) {
    console.log(BACKEND_ENDPOINT + path);
    return new Promise((success, failure) => {
        request.delete(BACKEND_ENDPOINT + path, {
            json: true,
            body: body
        }, function(err, response, body) {
            if (err) {
                failure(err);
            } else {
                success(body);
            }
        });
    });
}

//Handle new connection
io.on('connection', socket => {
  console.log('New connection');

  socket.on('register', (registerJSON) => {
      console.log("User trying to register")
      handleRegister(socket,registerJSON);
  });

    socket.on('login', (loginJSON) => {
      console.log("User trying to login")
      handleLogin(socket,loginJSON);
  })

  //Handle disconnection
  socket.on('disconnect', () => {
    console.log('Dropped connection');
  });
});

//Start server
if (module === require.main) {
  startServer();
}

module.exports = server;
