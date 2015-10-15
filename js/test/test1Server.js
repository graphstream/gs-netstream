var SERVER_IP = "127.0.0.1";

var http = require('http')
    , express = require('express')
    , app = express()
    , fs = require('fs')
    , WebSocketServer = require('ws').Server
    , WebSocket = require('ws')
    , sourceID = "nodeServer"
    , timeID = 0
    , net = require('net')
    , url = require('url')
    , netstream = {};

netstream.constants = require("../netstream_constants").netstream.constants;




//
// Classical Http server to serve the files...
//
app.use(express.static('.'));
app.use(express.static('../'));
app.listen(8080, function(){console.log('Http Server running. go to http://127.0.0.1:8080/test1.html')});



var wss = new WebSocketServer({
  port: 2003,
  host: SERVER_IP});


wss.on('error',
function() {
  console.log('WS error....');
});
wss.on('connection', function(ws) {

  console.log("WS Client connected to node");
  var location = url.parse(ws.upgradeReq.url, true);
  console.log(location);

  // create a response server for gs. Random (free) port
  // let's get a graph...
  var events_server = net.createServer(function(c) {
    console.log('events_server connected');
    c.on('end',
    function() {
      console.log('events_server disconnected');
    });
    c.on("data",
    function(data) {
      if (ws.readyState === WebSocket.OPEN) {
        console.log(data);
        ws.send(data);
      }
    });
  });
  events_server.listen(function() {
    //'listening' listener
    console.log('events_server bound');
  });
  var events_server_port = events_server.address().port;


  // ask GS
  var gs_client = net.connect(2001,
  function() {
    //'connect' listener
    console.log('gs_client connected');
    gs_client.write("" + events_server_port);
    gs_client.end();
  });
  gs_client.on('end',
  function() {
    console.log('gs_client disconnected');
  });




  // this client closes the connection
  ws.on('close',
  function() {
    console.log("WS client closed it.")
  });


  // this client sends somthing to GS
  ws.on('message',
  function(message) {
    //console.log('received: %s', message);
    if (message !== "Heartbeat"){
              console.log('received: %s', message);
              ws.send("ok");
      }
    });
});
