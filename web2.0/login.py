import tornado.ioloop
import tornado.web
class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class MainHandler(BaseHandler):
    # @tornado.web.authenticated
    def get(self):
        if not self.current_user:
            self.redirect("/login")
            return
        name = tornado.escape.xhtml_escape(self.current_user)
        self.write("Hello, " + name)

class LoginHandler(BaseHandler): 
    def get(self):
        self.write('<html><body><form action="/login" method="post">'
                   'Name: <input type="text" name="name">'
                   'password: <input type="text" name="password">'
                   '<input type="submit" value="Sign in">'
                   '</form></body></html>')

    def post(self):
        name_= self.get_argument("name")
        password_= self.get_argument("password")
        # print name_
        # print password_
        # print name_.strip()
        # print password_.strip()
        if isRight(name_.strip(), password_.strip()):
            self.set_secure_cookie("user", self.get_argument("name"))
            self.redirect("/")
        else:
            self.redirect("/login")

def isRight(n, p):
    fs = open("userprofile.txt", "r")
    for item in fs.readlines():
        # print item[:item.find(":")]
        # print item[item.find(":")+1:-1].strip("\r")
        if (n == item[:item.find(":")]):
            if (p == item[item.find(":")+1:-1]):
                return True
    return False
application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/login", LoginHandler),
], cookie_secret="61oETzKXQAGaYdkL5gEmGeJJuYh7EQnp2XdTP1o/Vo=")

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

##