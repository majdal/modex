
URL.prototype.toWebSocket = function() {
    /* Coerce a URL to the corresponding WebSocket URL.
     *  That is:
     *    - map http: -> ws:  and  https: -> wss:
     *    - leave things unchanged if it's already ws: or wss:
     *    - give an error otherwise, because WebSockets do not make sense off "the web"
     *         (if you really need non-http-related WebSocket URLs, think carefully about
     *         what you're doing, then explicity change your URL's protocol).
     *  The goal is to make it easy to keep all endpoints--HTTP, WebSocket, and otherwise
     *         --consistent in their use/not use of TLS.
     *
     *
     * Returns: a new URL object -- (not a string!)
     *   does NOT create a WebSocket -- you have to do that yourselv
     *
     *
     * Usage (assuming you have URLAbleWebSocket installed):
     *
     *  var control = new WebSocket(new URL(window.location).join("/ctl").toWebSocket())
     *  control.onopen = function(evt) { console.log("Successfully connected to", control.url); }
     *
     * TODO:
     *  [ ] Do we really need to be strict about URLs? What if you really do want to make a WebSocket connection to an ftp site?
     */

    // make a copy of ourselves
    var U = new URL(this.href)
    
    // now, map it to a websocket url
    if(U.protocol == "https:" || U.protocol == "wss:") { U.protocol = "wss:" }
    else if(U.protocol == "http:" || U.protocol == "ws:" ) { U.protocol = "ws:"}
    else { throw new URIError(U.href + " is not an HTTP URL") }
    
    return U;
}
function test_towebsocket() {
  // TODO
  Ru = new URL("http://sallysureisgreat.com/updates")
  console.log("toWebSocket() result", Ru.toWebSocket().href, "Expected:", "ws://sallysureisgreat.com/updates")

  Ru = new URL("https://fsdfds")
  console.log("secure sockets edition", Ru.toWebSocket().href, "Expected:", "wss://fsdfds")

  Ru = new URL("https://thiswillbreak/because/it/is/too/bad")
  Ru = Ru.toWebSocket()
  console.log("secure sockets edition", Ru.toWebSocket().href, "Expected:", "wss://fsdfds")
}

//test_towebsocket()
