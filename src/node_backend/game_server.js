var http = require('http'),
    path = require('path'),
    fs = require('fs'),
    util = require('util');
    
function get_root() {
    /*
     * Returns the root directory for modex.
     * */
    var launch_dir = __dirname;
    var directory_names = __dirname.split('/').slice(0, -2);
    return directory_names.join('/');
}

var PROJECT_ROOT = get_root();

var server = http.createServer(function (req, res) {
    var SERVEDIR = path.join(PROJECT_ROOT, 'src', 'frontend');
    var SERVEURL = SERVEDIR;
    var TOPDIR = req.url.split('/')[1];

    if(TOPDIR == 'assets') {
        SERVEURL = PROJECT_ROOT  + req.url; // overrides and goes to /assets since that's req.url
    }
    
    else if(req.url == '/') {
        SERVEURL = SERVEDIR + '/index.html';
    }
    
    else {
        SERVEURL = SERVEDIR + req.url;
    }
    
    fs.readFile(SERVEURL, function (err,data) {
    if (err) {
      res.writeHead(404);
      res.end(JSON.stringify(err));
      return;
    }
    res.writeHead(200);
    res.end(data);
  });
})

server.listen(8080);

