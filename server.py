import os, sys, json, threading
import tornado.ioloop
import tornado.web
from wsgiref.simple_server import make_server
from handlers import Client, Consumer, workerConsumer

t = threading.Thread(target=workerConsumer)
t.start()

settings = dict(
    static_path=os.path.join(os.getcwd(), 'static'),
    autoreload=True,
    debug=True,
)

handlers = [
    (r"/client", Client),
    (r"/consumer", Consumer),
]

application = tornado.web.Application(handlers, **settings)

if __name__ == '__main__':
    ip   = 'localhost'
    port = 8888
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()
