import queue, json, time, threading
#import arduino

class Singleton(type):
    _instances = {}
    def __call__(cls, *arg, **kargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*arg, **kargs)
        return cls._instances[cls]

#def workerConsumer(queueName):
class ConsumerThread(threading.Thread):
    def __init__(self, queueName):
        threading.Thread.__init__(self)
        self.queue = queueName

    def run(self):
        qmsg = QueueManager()
        sockets = SocketManager()
        print("Start Thread")

        while True:
            consumers = sockets.getConsumers(self.queue)
            if len(consumers) > 0:
                msg = qmsg.get(self.queue)
                if msg is None:
                    continue

                for c in consumers:
                    c.write_message(msg)
                    logger()
                #arduino.sendRGB(msg['rgb'])

        print("End Thread")

def logger():
    sockets = SocketManager()
    qmsg = QueueManager()
    print("Clients: %d\tQueues: %d\t" % (len(sockets.getClients()), len(sockets.getAllConsumers())))

class QueueManager(metaclass=Singleton):
    queues = {}
    threads = {}

    def add(self, obj):
        try:
            queueName = obj['queue']
            try:
                self.queues[queueName].put(obj)
            except KeyError:
                self.queues[queueName] = queue.Queue()
                self.queues[queueName].put(obj)
                self.threads[queueName] = ConsumerThread(queueName)
                self.threads[queueName].start()

            #self.qMessage.put(obj)
            logger()
        except Exception as err:
            print("Error: %s" % err)

    def get(self, queueName):
        try:
            obj = self.queues[queueName].get()
            return obj
        except Exception as err:
            print(type(msg))
            print(err)
            return {'queue': 'fail', 'content': str(err), 'msg': msg}

class SocketManager(metaclass=Singleton):
    clients = []
    consumers = {}
    queue = QueueManager()

    def addClient(self, client):
        self.clients.append(client)

    def rmClient(self, client):
        self.clients.remove(client)

    def addConsumer(self, consumer, queue):
        try:
            self.consumers[queue].append(consumer)
        except:
            self.consumers[queue] = []
            self.consumers[queue].append(consumer)

    def rmConsumer(self, consumer, queue):
        try:
            self.consumers[queue].remove(consumer)
        except Exception as err:
            print("Error: %s" % str(err))

    def getConsumers(self, queue):
        try:
            return self.consumers[queue]
        except Exception as err:
            print("Error: %s" % str(err))

    def getAllConsumers(self):
        return self.consumers

    def getClients(self):
        return self.clients

    def addMessage(self, message):
        obj = json.loads(message)
        self.queue.add(obj)
