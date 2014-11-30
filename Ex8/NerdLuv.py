import os.path
import re
# import locale
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)

class RegisterHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class ResultHandler(tornado.web.RequestHandler):
    def post(self):
        name = self.get_argument("Name")
        gender = self.get_argument("Gender")
        age = self.get_argument("Age")
        perType = self.get_argument("Personality_Type")
        favoriteOS = self.get_argument("Favorite_OS")
        Seeking_Male = self.get_argument("Seeking_Male", None)
        Seeking_Female = self.get_argument("Seeking_Female", None)
        minAge = self.get_argument("Min_Age")
        maxAge = self.get_argument("Max_Age")
        seeking = [Seeking_Male, Seeking_Female]
        print seeking
        print type(seeking)

        isError = isValid(name, gender, age, perType, favoriteOS, seeking, minAge, maxAge) 
    	if isError:
    		self.render("error.html", errorReason=isError)
    	else:
    		pass

# if valid, it returns a empty string; if not, it returns a string having the error message.
def isValid(name, gender, age, perType, favoriteOS, seeking, minAge, maxAge):
	# Judge whether the name contains merely blank characters.
	pattern = re.compile(r'\S')
	match = pattern.match(name)
	if not match:
		return "The name can not be blank. "

	pattern = re.compile(r'\d+$')
	match = pattern.match(age)
	if not match:
		return "The age must be integer between 0 and 99. "

	pattern = re.compile(r'[IE][NS][FT][JP]')
	match = pattern.match(perType)
	if not match:
		return "The personality type is not in correct formula. The first letter should be \
		I or E, the second N or S, the third F or T, the fourth J or P. For example, it shoule \
		be INFJ or ESTP. "

if __name__ == "__main__":
    tornado.options.parse_command_line()
    application = tornado.web.Application(
    [(r"/", RegisterHandler), (r"/result", ResultHandler)],
    template_path = os.path.join(os.path.dirname(__file__), "templates"),
    static_path = os.path.join(os.path.dirname(__file__), "static"),
    debug = True
    )
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()