#
#   Filename: NerdLuv.py
#    Description: 
#    Last modified: 2014-12-01 22:55
#
#    Created by Eleven on 2014-12-01
#    Email: eleveneat@gmail.com
#    Copyright (C) 2014 Eleven. All rights reserved.
#

import os.path
import re
import locale
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)

def matchAllUsers(name, gender, age, perType, favoriteOS, seeking, minAge, maxAge):
	matchUsers = []
	fs = open("static/txt/singles.txt", "r")
	for i in fs.readlines():
		i = i.strip()
		userInfo = (x for x in i.split(","))
		_name = userInfo.next()
		_gender = userInfo.next()
		_age = locale.atoi(userInfo.next())
		_perType = userInfo.next()
		_favoriteOS = userInfo.next()
		_seeking = userInfo.next()
		_minAge = locale.atoi(userInfo.next())
		_maxAge = locale.atoi(userInfo.next())
		if name == _name:
			continue
		# Judge whether they are of compatible gender and "seeking" value.
		if seeking.find(_gender) == -1 or _seeking.find(gender) == -1:
			continue
		point = 0
		# +1 point if the users are of compatible ages
		if age >= _minAge and age <= _maxAge and _age >= minAge and _age <= maxAge:
			point += 1
		# +2 points for having the same favorite operating system.
		if _favoriteOS == favoriteOS:
			point += 2
		# +1 point for having a dimension of personality type that matches the same dimension.
		for i in xrange(len(perType)):
			if _perType[i] == perType[i]:
				point += 1
		if point >= 3:
			_imageName = getImageName(_name)
			infoMap = {"Name":_name, "ImageName":_imageName, "Gender":_gender, "Age":_age,"Type":_perType,\
			"OS":_favoriteOS, "Rating":point,}
			matchUsers.append(infoMap)
	fs.close()
	return matchUsers

def getImageName(name):
	name = name.replace(' ', '_').lower()
	allUsers = os.listdir("static/images")
	for i in allUsers:
		i = i.replace('.jpg', "")
		if i == name:
			return name + ".jpg"
	return "default_user.jpg"

# If the user exists, return a string line containing its information, else return a empty string.
def isUserExist(name):
	fs = open("static/txt/singles.txt", "r")
	for i in fs.readlines():
		pattern = re.compile(name + ",")
		match = pattern.match(i)
		if match:
			return i.strip()
	return ""

# if valid, it returns a empty string; if not, it returns a string having the error message.
def isValid(name, gender, age, perType, favoriteOS, seeking, minAge, maxAge):
	# Judge whether the name contains merely blank characters.
	pattern = re.compile(r'\S')
	match = pattern.match(name)
	if not match:
		return "The name can not be blank. "
	# Judge whether the age is an integer between 0 and 99.
	pattern = re.compile(r'\d+$')
	match = pattern.match(age)
	if not match:
		return "The age must be integer between 0 and 99. "
	# Judge whether the personality type is in correct formula.
	pattern = re.compile(r'[IE][NS][FT][JP]')
	match = pattern.match(perType)
	if not match:
		return "The personality type is not in correct formula. The first letter should be \
		I or E, the second N or S, the third F or T, the fourth J or P. For example, it shoule \
		be INFJ or ESTP. "
	# Judge whether the seeking is chosen.
	if not seeking:
		return "The seeking should not be empty, you must choose at least one. "
	# Judge whether the minAge and maxAge are integers between 0 and 99.
	pattern = re.compile(r'\d+$')
	match = pattern.match(minAge)
	if not match:
		return "The between ages must be integer between 0 and 99. "
	match = pattern.match(maxAge)
	if not match:
		return "The between ages must be integer between 0 and 99. "
	# Judge whether the minAge is less than the maxAge.
	maxAge = locale.atoi(maxAge)
	minAge = locale.atoi(minAge)
	if maxAge < minAge:
		return "In between ages, the min age should be less than the max age. "
	return "" # Don't exist any problems.

def writeSinglesFile(userInfo):
	info = "\n" + ",".join(userInfo)
	fs = open("static/txt/singles.txt", "a")
	fs.write(info)
	fs.close()

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
        seeking = self.get_argument("Seeking_Male", "") + self.get_argument("Seeking_Female", "")
        minAge = self.get_argument("Min_Age")
        maxAge = self.get_argument("Max_Age")

        isError = isValid(name, gender, age, perType, favoriteOS, seeking, minAge, maxAge)
        # Form validation.
    	if isError:
    		self.render("error.html", errorReason=isError)
    	else:
    		matchUsers = matchAllUsers(name, gender, locale.atoi(age), perType, favoriteOS, seeking,\
    			locale.atoi(minAge), locale.atoi(maxAge))
    		self.render("results.html", Name=name, MatchUsers=matchUsers)
    		userInfo = [name, gender, age, perType, favoriteOS, seeking, minAge, maxAge]
    		writeSinglesFile(userInfo)

class LoginHandler(tornado.web.RequestHandler):
	def post(self):
		name = self.get_argument("loginName")
		flag = isUserExist(name)
		if flag:
			userInfo = (x for x in flag.split(","))
			name = userInfo.next()
			gender = userInfo.next()
			age = userInfo.next()
			perType = userInfo.next()
			favoriteOS = userInfo.next()
			seeking = userInfo.next()
			minAge = userInfo.next()
			maxAge = userInfo.next()
			matchUsers = matchAllUsers(name, gender, locale.atoi(age), perType, favoriteOS, seeking,\
    			locale.atoi(minAge), locale.atoi(maxAge))
			self.render("results.html", Name=name, MatchUsers=matchUsers)
		else:
			self.render("error.html", errorReason="This user doesn't exist. ")

if __name__ == "__main__":
    tornado.options.parse_command_line()
    application = tornado.web.Application(
    [(r"/", RegisterHandler), (r"/result", ResultHandler), (r"/login", LoginHandler)],
    template_path = os.path.join(os.path.dirname(__file__), "templates"),
    static_path = os.path.join(os.path.dirname(__file__), "static"),
    debug = True
    )
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
