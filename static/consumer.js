$(function(){
  function payload(target, value){
    return JSON.stringify({
      "target": target,
      "value": value
    })
  }

  var ws = undefined;
  function connect(){
    ws = new WebSocket('ws://localhost:8888/consumer');
    ws.onmessage = function(data){
      var obj = JSON.parse(data.data);
      $('body').css('background-color', obj.target);
      $('#lstMsg').html( $('#lstMsg').html() + '<br />' + data.data );
    }

    ws.onerror = function(error){
      console.log(error);
    }
    ws.onclose = function(msg){
      console.log('WebSocket Closed');
      //connect();
    }
  }
  connect();
});
