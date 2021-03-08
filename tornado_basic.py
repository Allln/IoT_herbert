from __future__ import print_function
import tornado.ioloop
import tornado.web
from os.path import dirname


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('web.html')


if __name__ == '__main__':

    # Handlers (access points)
    app = tornado.web.Application([
        (r'/', MainHandler),
        (r'/(.*)', tornado.web.StaticFileHandler, {
            'path': dirname(__file__) })
        ], debug=True)

    # Port
    TORNADO_PORT = 8813
    app.listen(TORNADO_PORT)

    # Start the server
    tornado.ioloop.IOLoop.current().start()
