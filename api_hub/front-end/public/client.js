var socket = null;

//Prepare game
var app = new Vue({
    el: '#app',
    data: {
        connected: false,
        user:{
            username:null,
            password:null,
            isLoggedIn:false,
        },
        page:"home"
    },
    mounted: function() {
        connect();
    },
    methods: {
        register(username, password) {
            socket.emit('register', {"username": username, "password": password});
        },
        login(username, password) {
            socket.emit('login', {"username": username, "password": password});
        },
    }
});

function connect() {
    //Prepare web socket
    socket = io();

    //Connect
    socket.on('connect', function() {
        //Set connected state to true
        app.connected = true;
    });

    //Handle connection error
    socket.on('connect_error', function(message) {
        alert('Unable to connect: ' + message);
    });

    //Handle disconnection
    socket.on('disconnect', function() {
        alert('Disconnected');
        app.connected = false;
    });

    socket.on('confirm_register', function (info){
        alert(`Registered User: ${info.username}`);
    });

    socket.on('confirm_login', function (info){
        alert(`User ${info.username} logged in`);
        app.user.isLoggedIn=true;
        app.user = {info}
        alert(app.user)
    });

    socket.on('error', function (info){
        alert(`error:${info}`);
    });

}
