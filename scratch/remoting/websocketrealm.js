
WebSocketRealm = function(realm, _WebSocket) {
  /* *class factory* which creates WebSocket-compatible classes that know about relative URLs.
   * realm is the base URL to build WebSockets onto
   * and _WebSocket is an optional parameter which gives a WebSocket-compatible class (which could be, e.g., another WebSocketRealm) to construct WebSockets out of
   * Usage:
   *   RelativeWebSocket
   * 
   * TODO:
   *  [ ] Figure out how instanceof sees results from this class, and if so what to do about that. Is anyone going to be depending on us?
   */

  if(!(realm instanceof URL)) {
    realm = new URL(realm);
  }
  
  if(realm.toWebSocket) {
    realm = realm.toWebSocket();
  } else {
    console.warn("URL.prototype.toWebSocket is not installed. Make sure '"+realm.href+"' uses the correct websocket scheme.")
  }
  
  if(_WebSocket == null) {
    _WebSocket = WebSocket; //stash original WebSocket class in our closure (if we don't do this, and someone uses WebSocketRealm to overwrite the default WebSocket, infinite loops will happen)
  }
  
  function WebSocketClass(href) { 
     var o = new _WebSocket(realm.join(href)); //since
     if(typeof(o) != "object") { // <- this check ensures that this function behaves itself, despite not being a 'proper' constructor.
                                 // see http://stackoverflow.com/questions/1978049/what-values-can-a-constructor-return-to-avoid-returning-this / http://bclary.com/2004/11/07/#a-13.2.2
       throw new Error("The WebSocket implementation that WebSocketRealm("+realm.href+") is wrapping did not construct an object.")
     }
     return o;
  }

  return WebSocketClass
}


// usage:

WebSocket = new WebSocketRealm(window.location);

//if we DIDN'T stash the original WebSocket, the above would cause an infinite loop
// you can even chain
ControlsWebSocket = new WebSocketRealm("ctls/");
DataWebSocket = new WebSocketRealm("feeds/");
d = new DataWebSocket("tempsensor1");


// Here's the API I want:
// drop-in transparency of websockets understanding their face
site_notices = PubSub(WebSocket("/site_ctl")).onMessage(function(evt) { .... })
tank = new WebSocket("tank23"); //notice: both 'new' and not-'new' forms supported (FF allows not-'new', Chrome is stricter)


// but you aren't limited to the default "realm" (which is window.location)
// suppose reddit gives useful data
RedditSocket = new WebSocketRealm("https://reddit.com/feeds")
datasets = new RedditAPI(new RedditSocket("/r/datasets"))
pretty = new RedditSocket("/r/IAmA");
pretty.onopen = function() { pretty.send("You won't guess who I met today..") }
ping = new RedditSocket("new_users") //-> 'wss://reddit.com/feeds/new_users'

