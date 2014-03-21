//the only change needed 

// this

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
    // implement http://www.ietf.org/rfc/rfc1808.txt
    // which says, in BNF, that:
    // an absolute URL is just something prefixed by "scheme:" where 'scheme' is actually http or https or ftp or ws or data or whatever; in particular, an absolute URL can be scheme:relativeURL
    
    // so relative URLs are king
    // an a relative URL is either an absolute path (which is identified simply by the fact that it starts with a /) a net_path URL (those funny //google.com/site URLs) which is identified by it starting with two slashes, and everything else is relative
    // a URL can come in absolute and relative flavoures
    
    
    //experimentally, site == this.origin EXCEPT if this.protocol is unknown to the browser.
    // and "file:" counts as unknown for some reason.
    // so instead, a workaround:
    site = this.protocol + "//" + this.hostname;
    
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
        if(path[0] != "") throw new Error("API inconsistency: URL.pathname should be absolute, so first component of path should be empty, but instead it is `" + this.pathname.toString() + "`")
        
        
        path.pop() //remove final component (possibly empty, if this URL represents a folder path)
        // XXX corner-case: http://site.com/folder vs http://site.com/folder/ do relative hrefs from  know that folder is a folder? testing this will require writing a server that fakes URL
        // aha, thank you IIS and your durpiness:
        // this site provides a test platform:
        // http://weblogs.asp.net/durp.jpg/
        //try running location.assign("hello/") a few times, then
        //            location.assign("hello2") and location.assign("hello3"); observe that hello/ keeps ~appending~, but hello3 replaces hello2 because hello2 didn't end with a /
        //so indeed, RELATIVE URLS MAY DIFFER. SO http://site.com/topiclist is a DIFFERENT page than http://site.com/topiclist/
        path.push(href)
        
        return new URL(site + path.join("/"));
      }
    }
    
}

// tests:
function test() {
var Ru = new URL(window.location.href)
console.log(Ru.href)
console.log(Ru.join("tackthison_relatively/p?zlease").href)
console.log(Ru.join("/absolute_path").href)
console.log(Ru.join("//newsite.com/otherpath").href) //a quirk: if you run this code locally (under a file:// URL) then this line misbehaves: the browser intentionally drops the hostname part
}

function websockethref(href) {
    /* using the above, get a websocket URL
     */
	U = new URL(window.location.href).join(href)	
    // now, map it to a websocket
    if(U.protocol == "https:") { U.protocol = "wss" }
    else if(U.protocol == "http:") { U.protocol = "ws"}
    else { throw new URIError(U.href + " is not an HTTP URL") }
    //case III should be impossible because if window.location exists we're running in a browser, and if we're running in a browser we're over HTTP
    //but better safe-than-sorry
}
