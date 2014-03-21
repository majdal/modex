

URLAbleWebSocket = function(U) {
  /* A simple drop-in wrapper to make WebSocket
   *  agnostic about whether it takes strings or URL objects.
   * 
   */
  if(U.href) U = U.href;
  return new URLAbleWebSocket._WebSocket(U);
}
URLAbleWebSocket._WebSocket = WebSocket; //store the original WebSocket class

WebSocket = URLAbleWebSocket //overwrite WebSocket
