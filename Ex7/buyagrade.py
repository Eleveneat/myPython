#
#    Filename: buyagrade.py
#    Description: None.
#    Last modified: 2014-11-25 21:50
#
#    Created by Eleven on 2014-11-23
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

class MainHandler(tornado.web.RequestHandler):
    # @tornado.web.authenticated
    def get(self):
        self.render("buyagrade.html")
    def post(self):
        name = self.get_argument("Name", 1)
        section = self.get_argument("Section")
        creditCardNum = self.get_argument("CreditCardNum")
        creditCardType = self.get_argument("CreditCardType")
        print type(creditCardType)

        if(len(name)*len(creditCardNum)):
            if creditCardType == "Visa":
                pattern = re.compile(r'4{1}\d{15}|4{1}\d{3}(-\d{4}){3}')
            else:
                pattern = re.compile(r'5{1}\d{15}|5{1}\d{3}(-\d{4}){3}')
            match = pattern.match(creditCardNum)
            if match and isLuhnValid(creditCardNum):
                writeSuckersFile(name, section, creditCardNum, creditCardType)
                fs = open("static/txt/suckers.txt", "r")
                fileMessages = fs.read()
                fs.close()

                self.render("sucker.html", suckerName=name,
                    suckerSection=section,
                    suckerCreditCardNum=creditCardNum,
                    suckerCreditCardType=creditCardType,
                    suckerFileMessages=fileMessages)
            else:
                reason = "You didn't provide a valid card number."
                self.render("sorry.html", errorReason=reason)
        else:
            reason = "You didn't fill out the form completely."
            self.render("sorry.html", errorReason=reason)


