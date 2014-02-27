

state.ws
========

state.ws comes in two components: state.ws.js and statews.py

It lets you do this:
```
s = state(WebSocket("ws://example.com/spreadsheets/debts"))

setInterval(function() { console.log(s.data()) }, 31415)
```

When the object at ws://example.com/spreadsheets/debts is updated, state.ws computes a delta 

Updates can happen server side (e.g. by the database getting updated, by another user editing the object, etc) or by you editing s.data.

```
s.['col1'][0] += 42)
s.commit()
```

state.ws supports [ACID](https://en.wikipedia.org/wiki/ACID) transparently.


state.ws is very similar to [Dropbox's Datastore API](https://www.dropbox.com/developers/datastore/docs/js#Dropbox.Datastore), but open source, frontend and backend. Drop it into your application today and do away with kludgy event handlers!


state.ws allows you to hook the deltas so that you can keep your UI in sync with your state (which is the same functionality as [this Dropbox API](https://www.dropbox.com/developers/datastore/docs/js#Dropbox.Datastore.RecordsChanged), but hopefully cleaner).
```
s.watch(function(delta){ //.watch()? maybe we should use whenjs for this?
  //updating the elements are not really like this; i don't know jquery enough and haven't thought through what deltas look like yet
  $("#table1").select(delta['column'], delta['row']).contents = delta['value']
})
```

state.ws does not yet but will soon support [delta compression](https://en.wikipedia.org/wiki/Delta_encoding).
