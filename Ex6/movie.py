# 
#    Filename: movie.py
#    Description: 
#    Last modified: 2014-11-17 22:24
#
#    Created by Eleven on 2014-11-17
#    Email: eleveneat@gmail.com
#    Copyright (C) 2014 Eleven. All rights reserved.
#
import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)

class Info(object):
    def __init__(self, full_name, publish_year, grade, reviews_number):
        self.full_name = full_name
        self.publish_year = publish_year
        self.grade = grade
        self.reviews_number= reviews_number
    def getDirFileMessage(self, path):
        fs = open(path, "r")
        self.full_name = fs.readline()
        self.publish_year = fs.readline()
        self.grade = fs.readline()
        self.reviews_number = fs.readline()
        fs.close()

class GeneralOverview(object):
    def __init__(self, overview_list):
        self.overview_list = overview_list
    def getDirFileMessage(self, path):
        fs = open(path, "r")
        self.overview_list = fs.readlines()
        fs.close()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        #initialization
        full_name = self.get_argument("full_name", None)
        publish_year = self.get_argument("publish_year", None)
        grade = self.get_argument("grade", None)
        reviews_number = self.get_argument("reviews_number", None)
        rotten_or_fresh = self.get_argument("rotten_or_fresh", None)
        overview_list = self.get_argument("overview_list", None)
        review_rotten_or_fresh_list =[]
        review_content_list = []
        review_name_list = []
        review_company_list = []

        asked_film_name = self.get_argument("film")
        picture_path = asked_film_name + "/" + "generaloverview.png"


        info = Info(full_name, publish_year, grade, reviews_number)
        info_path = "static/moviefiles/" + asked_film_name + "/info.txt"
        info.getDirFileMessage(info_path)

        if int(info.grade) >= 60:
            rotten_or_fresh = "freshbig.png"
        else:
            rotten_or_fresh = "rottenbig.png"

        generalOverview = GeneralOverview(overview_list)
        generalOverview_path = "static/moviefiles/" + asked_film_name + "/generaloverview.txt"
        generalOverview.getDirFileMessage(generalOverview_path)

        getReviewMessage(asked_film_name, review_rotten_or_fresh_list,\
            review_content_list, review_name_list, review_company_list)


        self.render("movie.html", film_picture_path = picture_path,\
            film_name = info.full_name,\
            film_publish_year = info.publish_year,\
            film_grade = info.grade,\
            film_reviews_number = info.reviews_number,\
            film_rotten_or_fresh = rotten_or_fresh,\
            film_overview_list = generalOverview.overview_list,\
            film_review_rotten_or_fresh_list = review_rotten_or_fresh_list,\
            film_review_content_list = review_content_list,\
            film_review_name_list = review_name_list,\
            film_review_company_list = review_company_list)

def getReviewMessage(asked_film_name, review_rotten_or_fresh_list,\
    review_content_list, review_name_list, review_company_list):
    path = "static/moviefiles/" + asked_film_name

    all_reviews_list = [x for x in os.listdir(path) if x.find("review") is not -1]
    for item in all_reviews_list:
        fs = open(path + "/" + item, "r")

        review_content_list.append(fs.readline())

        rotten_or_fresh = fs.readline()
        if rotten_or_fresh.find("ROTTEN") is not -1:
            review_rotten_or_fresh_list.append("rotten.gif")
        else:
            review_rotten_or_fresh_list.append("fresh.gif")

        review_name_list.append(fs.readline())

        review_company_list.append(fs.readline())
        fs.close()

if __name__ == "__main__":
    tornado.options.parse_command_line()
    application = tornado.web.Application(
    [(r"/", MainHandler)],
    template_path = os.path.join(os.path.dirname(__file__), "templates"),
    static_path = os.path.join(os.path.dirname(__file__), "static"),
    debug = True
    )
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()



