
global = this;

WebSocketRealm = function(realm) {
  /* *class factory* which creates WebSocket-compatible classes that know about relative URLs.
   *
   * Usage:
   *   RelativeWebSocket
   */

  if(!(realm instanceof URL)) {
    realm = new URL(realm);
  }
  
  realm = realm.toWebSocket();

  return {
     // something someting
     function constructor(href) { //this isn't quite right; it won't get along with 'new' and 'this'
       return new WebSocketRealm._WebSocket(realm.join(href));
     }
      
  }

}
WebSocketRealm._WebSocket = WebSocket; // stash original WebSocket implementation:
                                       // we always use this version, no matter what overwrites later may be done
                                       // because there's no way to be general about that without getting terrible dependency loops.






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


// to accomplish these features, overwrite built in WebSocket like so:
WebSocket = new WebSocketRealm(window.location);
