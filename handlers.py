import tornado.websocket
from broadcast import SocketManager, logger

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
