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
            explored:false,
            currentapiname:null,
            currentapifunctions:[],
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
        setPage(page){
            this.page = page;
        },
        submitURL(url){
            alert("Exploring API, this may take a few seconds!")
            socket.emit('exploreAPI', {"url": url});
        },
        resetAPI(){
            this.user.explored=false;
            this.user.currentapiname = null;
            this.user.currentapifunctions = [];
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
        app.user.username = info.username
        app.user.password = info.password
    });

    socket.on('confirm_explore', function(info){
        alert(`Successfully explored API: ${info.apiname}`);
        app.user.currentapiname = info.apiname;
        app.user.currentapifunctions = JSON.parse(info.functions);
        app.user.explored = true;

    });

    socket.on('error', function (info){
        alert(`error:${info}`);
    });

}
