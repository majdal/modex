/* urljoin.js
 *  Extend the URL prototype with a "join" method that
    behaves the same as html links: http://www.ietf.org/rfc/rfc1808.txt
   
    In particular, this understands
      * absolute URLs ("://")
      * net path URLs ("//")
      * absolute path URLs ("/")
      * relative path URLs ("")
    XXX are these def'ns clear enough?
 
 
 * There might be some edge cases not handled. Please report bugs you find with a short test case attached. For one thing,
 * Doesn't handle ".." which is really just convention but was written into the spec; the browser can deal with that.
 
 TODO:
* [ ] check if rfc1808 has been overridden at all
* [x-ish] write tests
* [ ] For spec compliance (but not for functionality):
      parse relative hrefs and do the spec'd pruning of '..' and '.' components.
      
*/

// this only runs on browsers -- node's url.Url is different
// nodejs's url includes a "resolve" function
//  but it doesn't have the same behaviour; it assumes all second URLs are relative: relative to the site root
// also, node's url.Url doesn't use getters and setters and its constructor ignores its argument (they expect you to use url.parse (and url.parse NEVER complains--the in-browser URL object will throw an exception on malformed URLs)); so you can do
// URL.href ~= url.Url.format(); and under Node if you try to access the URL you get inconsistent results (!!!!!!)
/*
 u = url.parse("http://site.com");
 u.protocol == "http:"
 u.href   //so far so good
 u.protocol = "bnackwards\"
 u.protocol == "bnackwards\:" //URL force-adds a : to every protocol and rejects malformed protocols (though, silently, not with an exception); Url does no such thing
 u.href   //inconsistent!! still shows "http://site.com"
 */

URL.prototype.join = function(href) {
    /* Returns a new URL object representing
     *
     */
    
    if(href instanceof URL) href = href.href; // cast URL objects into absolute-URL strings
                    // this could be shortcircuited by performing the absolute-URL case here
                    // but I'm scared of missing a corner case that way. 
    
    /*
    RFC1808 says, in BNF, that:
      an absolute URL is just /something/ prefixed by "scheme:",
      with the something usually being a relative URL. 
     So relative URLs are king, and they are defined as any of:
        - a net_path (those funny //google.com/site URLs) which is identified by it starting with //)
        - an abs_path (which is identified simply by the fact that it starts with a /)
        - a rel_path (ie. everything else so long as it is made of unreserved characters)
    
     We offload all the validity checking whether a path as the right characters
        or not or whatever to the browser's internal parser by
        calling 'new URL()' once we have done our tweaks.
      */
    
    //experimentally, site == this.origin EXCEPT if this.protocol is unknown to the browser.
    // and "file:" counts as unknown for some reason.
    // so instead, a workaround:
    site = this.protocol + "//" + this.hostname;
    
    
    if(href=="") { // section 5.2: "An empty reference resolves to the complete base URL:"
        return new URL(this.href);
    }
    if (href.startsWith("//")) { //net_path, section 2.4.3
       return new URL(this.protocol + href); //notice how the spec writers cleverly made href already contain the two needed slashes here
    } 
    if(href.startsWith("/")) { //absolute path
        return new URL(site + href);
    } else { //absolute and relative URLs
     //the URL class demands an absolute URL, so if it crashes we know the URL is relative
     // this (ab)uses exceptions-as-messaging, but it's the only API we have exposed to us.
      try {           //absolute URL
      	return new URL(href);
      } catch (err) { //relative URL
        //section "4. Resolving Relative URLS"
        // ...huh. accroding to rfc1808, a relative URL is supposed to inherit the query string if it doesn't provide one
        //and same for query params... tho
        //but by experimenting with what seems the be this algorithm in browsers, via location.assign, the params and querystring in the original URL are totally ignored
        
        var path = this.pathname.split("/");
        // sanity check (comment out at discretion)
        if(path[0] != "") throw new Error("API inconsistency: URL.pathname should be absolute, so first component of path should be empty, but instead it is `" + this.pathname.toString() + "`");
        
        // replace final component with the relative component. 
        path.pop();
        path.push(href);
        
        return new URL(site + path.join("/"));
      }
    }
    
}




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


URLAbleWebSocket = function(U) {
  /* A simple drop-in wrapper to make WebSocket understand URL objects.
   * 
   * 
   */
  if(U.href) U = U.href;
  return new URLAbleWebSocket.WebSocket(U);
}
URLAbleWebSocket.WebSocket = WebSocket; //store the original websocket
WebSocket = URLAbleWebSocket


///////////////////////////////////////////////
// tests:

function test_hrefjoin() {
var Ru = new URL("https://myawesomesite.net/zing/zang/zong.pdf")
console.log("Relative Path: ", Ru.join("tackthison_relatively/p?zlease").href, "Expected:", "https://myawesomesite.net/zing/zang/tackthison_relatively/p?zlease")
console.log("Absolute Path:", Ru.join("/absolute_path").href, "Expected:", "https://myawesomesite.com/absolute_path")
console.log("Net Path", Ru.join("//newsite.com/otherpath").href, "Expected:", "https://newsite.com/otherpath") 
console.log(Ru.join("ws://zanga.internet/woahnelly").href, "Expected:", "ws://zanga.internet/woahnelly") 
console.log(Ru.join("").href, "Expected:", "https://myawesomesite.net/zing/zang/zong.pdf") 
  //a quirk: if you run this code locally (under a file:// URL) then this line misbehaves: the browser intentionally drops the hostname part


// ensure corner case works:
// IIS's durpiness provides a test platform:
//    http://weblogs.asp.net/durp.jpg/
//try going there and running location.assign("hello/") a few times, then
//            location.assign("hello2") and location.assign("hello3"); observe that hello/ keeps ~appending~, but hello3 replaces hello2 because hello2 didn't end with a /
        //so indeed, RELATIVE URLS MAY DIFFER. SO http://site.com/topiclist is a DIFFERENT page than http://site.com/topiclist/
var folder = new URL("http://site.com/one/two/")
var file = new URL("http://site.com/one/two")

console.log(folder.join("addendum").href, "Expected:", "http://site.com/one/two/addendum")
console.log(file.join("addendum").href, "Expected", "http://site.com/one/addendum")



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

test_hrefjoin()
test_towebsocket()
