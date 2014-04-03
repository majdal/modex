function socket_handler (req, res) {
    console.log(req.url);
    SERVEURL = __dirname + '/test.html';
    fs.readFile(SERVEURL, function (err,data) {
    if (err) {
      res.writeHead(404);
      res.end(JSON.stringify(err));
      return;
    }
    res.writeHead(200);
    res.end(data);
  });
    // this does not really handle much for now.
}
