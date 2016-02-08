import queue, json, time, threading

class Singleton(type):
    _instances = {}
    def __call__(cls, *arg, **kargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*arg, **kargs)
        return cls._instances[cls]

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

        print("End Thread")

def logger():
    sockets = SocketManager()
    qmsg = QueueManager()
    queues = qmsg.getAll()
    print("---"*10)
    print("Clients: %d\tQueues: %d\t" % (len(sockets.getClients()), len(queues)))

    for k in queues:
        print("Queue: %s" % k)
        print("\tConsumers: %d\tMessages: %d" %(len(sockets.getConsumers(k)), qmsg.getQueue(k).qsize()))

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

            logger()
        except Exception as err:
            print("Error: %s" % err)

    def get(self, queueName):
        try:
            obj = self.queues[queueName].get()
            return obj
        except Exception as err:
            print(err)
            return {'queue': 'fail', 'content': str(err), 'msg': msg}

    def getAll(self):
        return self.queues

    def getQueue(self, queue):
        return self.queues[queue]

class SocketManager(metaclass=Singleton):
    clients = []
    consumers = {}
    queue = QueueManager()

    def addClient(self, client):
        self.clients.append(client)
        logger()

    def rmClient(self, client):
        self.clients.remove(client)
        logger()

    def addConsumer(self, consumer, queue):
        try:
            self.consumers[queue].append(consumer)
        except:
            self.consumers[queue] = []
            self.consumers[queue].append(consumer)
        logger()

    def rmConsumer(self, consumer, queue):
        try:
            self.consumers[queue].remove(consumer)
        except Exception as err:
            print("Error: %s" % str(err))
        logger()

    def getConsumers(self, queue):
        try:
            return self.consumers[queue]
        except Exception as err:
            return []

    def getAllConsumers(self):
        return self.consumers

    def getClients(self):
        return self.clients

    def addMessage(self, ws, message):
        try:
            obj = json.loads(message)
            try:
                newQueue = obj['change_queue']
                self.rmConsumer(ws, ws.queue)
                ws.queue = newQueue
                self.addConsumer(ws, ws.queue)
                ws.write_message({"message": "changed queue"})
            except:
                self.queue.add(obj)
        except Exception as err:
            ws.write_message({"error": str(err)})
            print(err)
