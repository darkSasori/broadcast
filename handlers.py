import tornado.websocket
from broadcast import SocketManager, logger

class WebSocket(tornado.websocket.WebSocketHandler):
    socketManager = None

    def check_origin(self, origin):
        print(origin)
        return True

    def add(self):
        pass

    def remove(self):
        pass

    def open(self):
        self.socketManager = SocketManager()
        self.add()
        logger()

    def on_message(self, message):
        self.socketManager.addMessage(self, message)

    def on_close(self):
        self.remove()
        logger()

class Client(WebSocket):
    def add(self):
        self.socketManager.addClient(self)

    def remove(self):
        self.socketManager.rmClient(self)

class Consumer(WebSocket):
    queue = None

    def open(self, queue):
        self.queue = queue
        WebSocket.open(self)

    def add(self):
        self.socketManager.addConsumer(self, self.queue)

    def remove(self):
        self.socketManager.rmConsumer(self, self.queue)
