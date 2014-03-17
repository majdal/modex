function Promise() {
    /* DEMO:
    var q = new Promise().then(function(alphabet) { console.log("alpohaahahaha", alphabet) })
    q.error(function(e) { console.error("ERRORR"); })
    q.error_out(5); //trigger the error handlers
    q.resolve("zurp"); //trigger the then() handlers
    */
    /* todo: scrap this and use A+, when my net comes back
     */
    
    var handlers = []
    var error_handlers = []
    
    return {
        resolve: function(result) {
            handlers.forEach(function(h) {
                h(result);
            })
           },

        error_out: function(result) {
            error_handlers.forEach(function(h) {
                h(result);
            })
          },
        
        then: function(f) {
            handlers.push(f);
            return this;
        }    ,
        error: function(f) {
            error_handlers.push(f);
            return this;
        }    ,
    }
	
}

module.exports = Promise
