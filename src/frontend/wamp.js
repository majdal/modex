  global = this;

  //rpcFail is used as the error handler for RPC calls; it is optional.
  function rpcFail(error) {
    console.log("Call failed: " + JSON.stringify(error));
  }

  
$(function() {
 $("#connected").css("color", "red") //mark not connected
 $("#connected").html("Disconnected") 
 
 var connection = new autobahn.Connection({
   url: 'ws://127.0.0.1:8080/wamp',
   realm: 'realm1'});  //FEATURE REQUEST: error handling for autobahn plzkthx

 global.connection = connection; //debug

  connection.onopen = function (session) {
    $("#connected").css("color", "yellow") //mark connecting
    $("#connected").html("Connecting..")
    console.log("opening session " + session.id);
    console.log(connection._websocket.readyState);

  // hook the low-level handlers on the websocket to help debug what Autobahn thinks it is doing
  // it would be nice if Autobahn had error handlers we could hook
  // but it doesn't, not everywhere.
  // these must be done here because _websocket doesn't exist until connection.open()
  connection._websocket.onerror = function(evt) {
    console.log("websocket error: " + evt.reason)
  }

  connection._websocket.onclose = function(evt) { 
    console.log("websocket close: " + evt.reason)
  }
  
  function hookup() {
  session.subscribe("heartbeat", function() {
    console.log("heartbeat");
  })
  session.subscribe("data", function (args, kwargs, evtDetails) {
    console.log("got data: " + "args = " + JSON.stringify(args) +
                 ", kwargs = " + JSON.stringify(kwargs),
                 ", metadata details: " + JSON.stringify(evtDetails));
  });
   
  // RPC is done with session.call(), which returns a Promise/A+ object -- something                                                   
  // with a .then() method that lets you attach callbacks
   

    // RPC the parrot function with varous arguments
    function parrotHandler(r) {
      console.log("this is not a parrot nevermore:", JSON.stringify(r));
    }
    //session.call('start').then(parrotHandler);
    
    $("#connected").css("color", "green") //mark connected
    $("#connected").html("Connected.")

    global.session = session; //stash for debugging
    
    start = $("#controls #start") //ack; my spider sense wants this to be 
    stop = $("#controls #stop")
    start.css("opacity", 1) //mark ready to start (XXX not sync'd with server side _running/not _runningx state)
    //start.click(function() {
    //  start.opacity("
    //})
    global.start = start;
    global.stop = stop;
   }
  setTimeout(hookup, 6000)
  }

 setTimeout(function() {
  connection.open()}, 6000)

}) //end oninit
