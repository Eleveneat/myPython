import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
    	tl = "book list"
    	hd = "classic book"
    	bks = ["okl", "asd", "ppp"]
        self.render("index.html", title = tl, header = hd, books = bks)

application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()