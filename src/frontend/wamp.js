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
  //hook up event handlers
  //in a subroutine so that it can be sloweeeeed dooowwwwn

  session.subscribe("heartbeat", function() {
    console.log("heartbeat");
  })

  session.subscribe("data", function (args, kwargs, evtDetails) {
    console.log("got data: " + "args = " + JSON.stringify(args) +
                 ", kwargs = " + JSON.stringify(kwargs),
                 ", metadata details: " + JSON.stringify(evtDetails));
    $("h2").width((10000*args[0])+"px") //in lieu of having a nice d3 graph to plot the results of the simulation, just have them resize the title
  });

    
    $("#connected").css("color", "green") //mark connected
    $("#connected").html("Connected.")

    global.session = session; //stash for debugging


    start = $("#controls #start")
    stop = $("#controls #stop")
    
    function doStart() {
        session.call('start').then(function() { //this stuff has to happen after the call succeeds
           start.css("opacity", .1)
           stop.css("opacity", 1)
           stop.attr("href","#"); start.attr("href",null);
           stop.click(doStop)
           start.unbind()   //especially this; we want to be able to click *until*
        })
        return false; //kill the href
    }
    function doStop() {
        session.call('stop').then(function() { //this stuff has to happen after the call succeeds
           start.css("opacity", 1)
           stop.css("opacity", .1)
           start.attr("href","#"); stop.attr("href",null)
           start.click(doStart)
           stop.unbind()   //especially this; we want to be able to click *until*
        })
        return false; //kill the href
    }
    
    start.css("opacity", 1) //mark ready to start (XXX not sync'd with server side _running/not _runningx state)
    start.click(doStart);
    
    global.start = start;
    global.stop = stop;


   }  //end deferred
  setTimeout(hookup, 3000)
   
  }
 
 //connection.open()
 setTimeout(function() { connection.open() }, 2000) //must be wrapped; see https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/this#Method_binding
                                                    //                     https://developer.mozilla.org/en-US/docs/Web/API/window.setTimeout?redirectlocale=en-US&redirectslug=DOM%2Fwindow.setTimeout#The_.22this.22_problem
}) //end oninit
