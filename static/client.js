$(function(){
    function payload(target, value){
        return JSON.stringify({
            "target": target,
            "rgb": value,
            "queue": "color"
        })
    }

  function addLogger(msg){
      $('#lstMsg').html( $('#lstMsg').html() + '<br />' + msg );
  }

  var ws = undefined;
  function connect(){
    ws = new WebSocket('ws://192.168.0.9:8888/client');
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


  var wsConsumer = undefined;
  function connectConsumer(){
    wsConsumer = new WebSocket('ws://192.168.0.9:8888/consumer/color');
    wsConsumer.onmessage = function(data){
      var obj = JSON.parse(data.data);
      $('body').css('background-color', obj.target);
      addLogger(data.data);
    }

    wsConsumer.onerror = function(error){
      console.log(error);
    }
    wsConsumer.onclose = function(msg){
      console.log('WebSocket Closed');
      connectConsumer();
    }
  }
  connectConsumer();

  $(".chsend").click(function(){
    ws.send(payload($(this).val(), 2));
  });

  $('#colorPicker').ColorPicker({
      flat: true,
      onChange: function(hsb, hex, rgb){
          //addLogger('HSB: '+hsb);
          //addLogger('HEX: '+hex);
          //addLogger('RGB: '+rgb);
          ws.send(payload('#'+hex, rgb));
      }
  });
});
