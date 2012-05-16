
var SERVER_IP = "172.17.22.154";

var http = require('http')
    , fs = require('fs')
    , WebSocketServer = require('ws').Server
    , sourceID="nodeServer"
    , timeID=0
    , net = require('net')
    , netstream = {};

netstream.constants = require("../netstream_constants").netstream.constants;



//
// Classical Http server to serve the files...
//
http.createServer(function (request, response) {
 
    console.log('request starting... '+request.url);
     
    fs.readFile('./'+request.url, function(error, content) {
        if (error) {
            response.writeHead(500);
            response.end();
            //console.log(error);
        }
        else {
            response.writeHead(200, { 'Content-Type': 'text/html' });
            response.end(content, 'utf-8');
        }
    });
     
}).listen(8080);
 
console.log('Http Server running at http://127.0.0.1:8080/');









var wss = new WebSocketServer({port: 2003, host:SERVER_IP});
wss.on('error', function(){
    console.log('WS error....');
});
wss.on('connection', function(ws) {
    
    console.log("WS Client connected to node");
    
    
    
    
    
    
    
    
    // create a response server for gs. Random (free) port
    // let's get a graph...
     var events_server = net.createServer(function(c) { 
       console.log('events_server connected');
       c.on('end', function() {
         console.log('events_server disconnected');
       });
       c.on("data", function (data) {
           ws.send(data);
         });
     });
     events_server.listen(function() { //'listening' listener
       console.log('events_server bound');
     });
     var events_server_port = events_server.address().port;
     
    
    // ask GS
    var gs_client = net.connect(2001, function() { //'connect' listener
      console.log('gs_client connected');
      gs_client.write(""+events_server_port);
      gs_client.end();
    });
    gs_client.on('end', function() {
      console.log('gs_client disconnected');
    });
    
    
    
    
    // this client closes the connection
    ws.on('close', function(){
       console.log("WS client closed it.")
    });
        
    
    // this client sends somthing to GS
    ws.on('message', function(message) {
        //console.log('received: %s', message);
        // if (message === "Heartbeat"){
        //             console.log('Heartbeating...');
        //             
        //         }  
    });
});



