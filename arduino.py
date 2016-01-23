import serial, threading, time, binascii
ser = serial.Serial('/dev/ttyACM0')

def worker():
    while True:
        value = ser.readline()
        print(value)

def sendBinary(value):
    print("Sending %s" %value)
    for i in value:
        ser.write(binascii.a2b_qp(i))
    #ser.write(struct.pack(text))

def sendRGB(data):
    msg = "r%s;g%s;b%s;" %(data['r'],data['g'],data['b'])
    sendBinary(msg)

t = threading.Thread(target=worker)
t.start()

if __name__ == '__main__':
    print("Serial")
    time.sleep(5)
    sendBinary('r255;')
    time.sleep(5)
    ser.write(b'r')
    ser.write(b'0')
    ser.write(b';')
