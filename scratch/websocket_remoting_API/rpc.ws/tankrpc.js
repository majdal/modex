

RPC = require("./rpc.ws.js")

ObjectRPC = RPC.ObjectRPC
RPC = RPC.RPC

var tank = new ObjectRPC("ws://localhost:8080/sprites/tank2", ["HP", "turn", "shoot"])

tank.ready(function() {
  console.log("tank sockets opened; calling");
  tank.HP().then(function(h) {
     console.log("Tank2's hp:", h.current, "/", h.total)
  });  tank.HP().then(function(h) {
     console.log("Tank2's hp:", h.current, "/", h.total)
  });  tank.HP().then(function(h) {   
     console.log("Tank2's hp:", h.current, "/", h.total)
  })
});

tank.error(function(e){
  console.log(e.target.url, "failed because", e.message);
})
