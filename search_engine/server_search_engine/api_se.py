import cherrypy, json, pymongo, sys, os
from os.path import abspath
from jinja2 import Environment, FileSystemLoader
from cherrypy.lib import static
from binary_search_inverted_index import binary_search_inverted_index

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.getcwd()))))
from pesquisas.search_engine.mongo_url import mongo_url
from os.path import abspath

env = Environment(loader=FileSystemLoader("views"))


class Root(object):
    def __init__(self):
        self.bsii = binary_search_inverted_index()
        self.localDir = os.path.dirname(__file__)
        self.absDir = os.path.join(os.getcwd(), self.localDir)

    @cherrypy.expose
    def index(self):
        tmpl = env.get_template("index.html")
        return tmpl.render()

    @cherrypy.expose
    def search_text(self, search):
        self.bsii.retrive_data(search, prefix="files/")
        tmpl = env.get_template("download.html")
        return tmpl.render(
            {
                "nome_arquivo": "files/" + search.replace(" ", "_") + ".xlsx",
                "expressao": search,
            }
        )

    @cherrypy.expose
    def download_file(self, file_name):
        path = os.path.join(self.absDir, file_name)[:-1]
        return static.serve_file(
            path, "application/x-download", "attachment", os.path.basename(path)
        )


# actv_lrn = 1
config = {
    "/css": {
        "tools.staticdir.on": True,
        "tools.staticdir.dir": os.getcwd() + "/views/css/",
    },
}

cherrypy.config.update({"server.socket_port": 8035})
cherrypy.quickstart(Root(), "/", config=config)
