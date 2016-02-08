import serial, threading, time, binascii, json
from ws4py.client.threadedclient import WebSocketClient

ser = serial.Serial('/dev/ttyACM0')

class ClientWS(WebSocketClient):
    def opened(self):
        print('Connected')

    def closed(self, code, reason):
        print('Closed [%d] %s' %(code, reason))

    def received_message(self, msg):
        msg = str(msg)
        obj = json.loads(msg)
        sendRGB(obj)

def worker():
    while True:
        value = ser.readline()
        print(value)

def sendBinary(value):
    print("Sending %s" %value)
    for i in value:
        ser.write(binascii.a2b_qp(i))

def sendRGB(data):
    msg = "%s%s;" %(data['target'],data['value'])
    print(msg)
    sendBinary(msg)

t = threading.Thread(target=worker)
t.start()

if __name__ == '__main__':
    print("Arduino Serial WebSocket Client")
    try:
        ws = ClientWS('ws://192.168.0.9:8888/consumer/color')
        ws.connect()
    except:
        print('tchau')
        ws.close()
