import os, sys, json, threading
import tornado.ioloop
import tornado.web
from wsgiref.simple_server import make_server
from handlers import Client, Consumer

settings = dict(
    static_path=os.path.join(os.getcwd(), 'static'),
    autoreload=True,
    debug=True,
)

handlers = [
    (r"/client", Client),
    (r"/consumer/(\w+)", Consumer),
]

application = tornado.web.Application(handlers, **settings)

if __name__ == '__main__':
    ip   = '192.168.0.9'
    port = 8888
    print("Listen: %s:%d" %(ip,port))
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()
