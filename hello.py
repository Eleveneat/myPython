import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self, usrid):
    	k = self.get_argument("key")
        self.write("Hello, world: " + usrid + "key = " + k)

application = tornado.web.Application([
    (r"/u/([a-zA-Z0-9]+)", MainHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()