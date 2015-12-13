import tornado.websocket
import queue, json, time


class Singleton(type):
    _instances = {}
    def __call__(cls, *arg, **kargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*arg, **kargs)
        return cls._instances[cls]

def workerConsumer():
    qmsg = QueueManager()
    sockets = SocketManager()
    print("Start Thread")

    while True:
        consumers = sockets.getConsumers()
        if len(consumers) > 0:
            msg = qmsg.get()
            if msg is None:
                break
            logger()
            for c in consumers:
                c.write_message(msg)

    print("End Thread")

def logger():
    sockets = SocketManager()
    qmsg = QueueManager()
    print("Clients: %d\tConsumers: %d\tMessages: %d" % (len(sockets.getClients()), len(sockets.getConsumers()), qmsg.qsize()))

class QueueManager(metaclass=Singleton):
    qMessage = queue.Queue()

    def add(self, message):
        sockets = SocketManager()
        logger()
        try:
            obj = json.loads(message)
            self.qMessage.put(obj)

            for c in sockets.getClients():
                c.write_message(obj)

            #print("Fila(%d): %s" % (self.qMessage.qsize(), obj))
        except Exception as err:
            print("Error: %s" % err)

    def get(self):
        return self.qMessage.get()

    def qsize(self):
        return self.qMessage.qsize()

class SocketManager(metaclass=Singleton):
    clients = []
    consumers = []
    queue = QueueManager()

    def addClient(self, client):
        self.clients.append(client)

    def rmClient(self, client):
        self.clients.remove(client)

    def addConsumer(self, consumer):
        self.consumers.append(consumer)

    def rmConsumer(self, consumer):
        self.consumer.remove(consumer)

    def getConsumers(self):
        return self.consumers

    def getClients(self):
        return self.clients

    def addMessage(self, message):
        self.queue.add(message)

class WebSocket(tornado.websocket.WebSocketHandler):
    socketManager = None

    def add(self):
        pass

    def remove(self):
        pass

    def open(self):
        self.socketManager = SocketManager()
        self.add()
        logger()

    def on_message(self, message):
        self.socketManager.addMessage(message)

    def on_close(self):
        self.remove()
        logger()

class Client(WebSocket):
    def add(self):
        self.socketManager.addClient(self)

    def remove(self):
        self.socketManager.rmClient(self)

class Consumer(WebSocket):
    def add(self):
        self.socketManager.addConsumer(self)

    def remove(self):
        self.socketManager.rmConsumer(self)
