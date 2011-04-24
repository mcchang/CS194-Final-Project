import os
import tornado.ioloop
import tornado.web

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "debug": True
}

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("main.html")


class VisHandler(tornado.web.RequestHandler):
    def get(self):
        template = self.request.path[1:] + ".html"
        self.render(template) 


class DataHandler(tornado.web.RequestHandler):
    def get(self):
        data_filename = self.request.path.split("/")[-1]
        data_filepath = os.path.join(settings["static_path"], data_filename)
        data_file = open(data_filepath, 'r')
        data = data_file.read()
        self.write(data)
        data_file.close()


class PlotHandler(tornado.web.RequestHandler):
    def get(self):
        data_filepath = os.path.join(settings["static_path"], "regression")
        plots = os.listdir(data_filepath)
        plots = [os.path.join(data_filepath, plot) for plot in plots]
        self.render("plots.html", plots=plots)


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/plots", PlotHandler),
    (r"/data/.+\.json", DataHandler),
    (r"/.+", VisHandler)
], **settings)


if __name__ == "__main__":
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
