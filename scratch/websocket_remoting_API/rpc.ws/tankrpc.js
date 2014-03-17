

RPC = require("./rpcws.js")

var tank = new RPC.RemoteObject("ws://localhost:8080/sprites/tank2", ["HP", "turn", "shoot"])

tank.ready(function() {
  console.log("tank sockets opened; calling");
  tank.HP().then(function(h) {
     console.log("1st call: Tank2's hp:", h.current, "/", h.total)
  });

  tank.HP().then(function(h) {
     console.log("2nd: Tank2's hp:", h.current, "/", h.total)
     console.log("Shutting down Tank connections");
     tank.close();
  });
  
  tank.turn().error(function(e) {
    console.log("tank.turn() failed:", e)
  })

  tank.HP().then(function(h) {   
     console.log("3rd: Tank2's hp:", h.current, "/", h.total)
  })
});

tank.error(function(e){
  console.log(e.target.url, "failed because", e.message);
})

console.log("done Tank demo initialization;")
