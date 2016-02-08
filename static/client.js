var queue = "color";

function payload(value, color){
    return JSON.stringify({
        "target": color,
        "value": value,
        "queue": queue
    })
}

function addLogger(msg){
    document.getElementById('lstMsg').innerHTML += '<br />' + msg ;
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

function changeStatu(obj, color){
    console.log(obj.checked);
    if( obj.checked )
        ws.send(payload(255, color));
    else
        ws.send(payload(0, color));
}
