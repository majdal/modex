function hrefjoin(href) {
    // implement http://www.ietf.org/rfc/rfc1808.txt
    // which says, in BNF, that:
    // an absolute URL is just something prefixed by "scheme:" where 'scheme' is actually http or https or ftp or ws or data or whatever; in particular, an absolute URL can be scheme:relativeURL
    
    // so relative URLs are king
    // an a relative URL is either an absolute path (which is identified simply by the fact that it starts with a /) a net_path URL (those funny //google.com/site URLs) which is identified by it starting with two slashes, and everything else is relative
    // a URL can come in absolute and relative flavoures
    if (href.startsWith("//")) { //net_path, section 2.4.3
        return location.protocol + href;
    } 
    if(href.startsWith("/")) { //absolute path
        return window.location.origin + href;
    } else if(href ~= "^.+://.*") { //absolute URL 
        return href;
    } else { //relative path. 
        //section "4. Resolving Relative URLS"
        // ...huh. accroding to rfc1808, a relative URL is supposed to inherit the query string if it doesn't provide one
        //and same for query params... tho
        //but by experimenting with what seems the be this algorithm in browsers, via location.assign, the params and querystring in the original URL are totally ignored
        
        path = window.location.pathname.split("/");
        path.pop() //remove final component (possibly empty)
        // XXX corner-case: http://site.com/folder vs http://site.com/folder/ do relative hrefs from  know that folder is a folder? testing this will require writing a server that fakes URL
        // aha, thank you IIS and your durpiness:
        // this site provides a test platform:
        // http://weblogs.asp.net/durp.jpg/
        //try running location.assign("hello/") a few times, then
        //            location.assign("hello2") and location.assign("hello3"); observe that hello/ keeps ~appending~, but hello3 replaces hello2 because hello2 didn't end with a /
        return location.pathname + href;
    }
    
}
