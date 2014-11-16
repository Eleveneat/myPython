import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        tl = "Music Viewer"
        h1 = "190M Music Playlist Viewer"
        h2 = "Search Through Your Playlists and Music"
        playlist_be_asked = self.get_argument("playlist", "None")
        if (playlist_be_asked != "None"):
            playlist_path = "static/songs/" + playlist_be_asked
            f = open(playlist_path)
            songs_of_playlist = []
            for line in f.readlines():
                 songs_of_playlist.append(line.strip("\r\n"))
            print songs_of_playlist
            addSizeToSongs(songs_of_playlist)
            self.render("music.html", title = tl, header1 = h1, header2 = h2, songs = songs_of_playlist, playlists = [])
            f.close()
        else:
            all_songs = ["190M Rap.mp3", "Be More.mp3", "Drift Away.mp3", "Hello.mp3","Just Because.mp3", "Panda Sneeze.mp3"]
            all_lists = ["190M Mix.txt", "mypicks.txt", "playlist.txt"]
            addSizeToSongs(all_songs)
            self.render("music.html", title = tl, header1 = h1, header2 = h2, songs = all_songs, playlists = all_lists)

def addSizeToSongs(songs_of_list):
    len_of_list = len(songs_of_list)
    for foo in range(len_of_list):
        song_path = "static/songs/" + songs_of_list[foo]
        tmp_size = os.path.getsize(song_path)
        if tmp_size <= 1023:
            tmp_size = " (" + str(tmp_size) + " b" + ")"
        elif tmp_size > 1048576:
            tmp_size /= 1048576.00
            tmp_size = round(tmp_size, 2)
            tmp_size = " (" + str(tmp_size) + " mb" + ")"
        else:
            tmp_size /= 1024.00
            tmp_size = round(tmp_size, 2)
            tmp_size = " (" + str(tmp_size) + " kb" + ")"
        songs_of_list[foo] += tmp_size
    return songs_of_list

application = tornado.web.Application(
    [(r"/", MainHandler)],
    static_path = os.path.join(os.path.dirname(__file__), "static"),
    template_path = os.path.join(os.path.dirname(__file__), "templates"),
    debug = True
)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()




