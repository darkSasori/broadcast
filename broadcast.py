import queue, json, time, arduino

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
            arduino.sendRGB(msg['rgb'])

    print("End Thread")

def logger():
    sockets = SocketManager()
    qmsg = QueueManager()
    #print("LOGGER")
    print("Clients: %d\tConsumers: %d\tMessages: %d" % (len(sockets.getClients()), len(sockets.getConsumers()), qmsg.qsize()))

class QueueManager(metaclass=Singleton):
    qMessage = queue.Queue()

    def add(self, message):
        sockets = SocketManager()
        try:
            obj = json.loads(message)
            self.qMessage.put(obj)
            logger()
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
        self.consumers.remove(consumer)

    def getConsumers(self):
        return self.consumers

    def getClients(self):
        return self.clients

    def addMessage(self, message):
        self.queue.add(message)

