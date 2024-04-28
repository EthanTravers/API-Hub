'use strict';

//Set up express
const express = require('express');
const app = express();

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


// URL of the backend API
const BACKEND_ENDPOINT = 'https://apihub-et2g21.azurewebsites.net' || 'http://localhost:7071';

//Start the server
function startServer() {
    const PORT = process.env.PORT || 8080;
    server.listen(PORT, () => {
        console.log(`Server listening on port ${PORT}`);
    });
}

function handleRegister(registerJSON){
    //Backend Register Call
    //Alert user if it can't create the account
    //Send successful register and then proceed to log in with those credentials with handleLogin
}


//Handle new connection
io.on('connection', socket => {
  console.log('New connection');

  socket.on('register', (registerJSON) => {
      handleRegister(registerJSON);
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
