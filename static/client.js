$(function(){
  function payload(target, value){
    return JSON.stringify({
      "target": target,
      "value": value
    })
  }

  var ws = undefined;
  function connect(){
    ws = new WebSocket('ws://localhost:8888/client');
    ws.onmessage = function(data){
      var obj = JSON.parse(data.data);
      console.log(data);
      console.log(obj);
    }

    ws.onerror = function(error){
      console.log(error);
    }
    ws.onclose = function(msg){
      console.log('WebSocket Closed');
      connect();
    }
  }
  connect();


  $(".chsend").click(function(){
    ws.send(payload($(this).val(), 2));
  });
});
