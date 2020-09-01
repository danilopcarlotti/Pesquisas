from cherrypy.lib import static
from cluster_documents import cluster_documents
from jinja2 import Environment, FileSystemLoader
from os.path import abspath
from bson.objectid import ObjectId
import cherrypy, json, pymongo, sys, os, subprocess

env = Environment(loader=FileSystemLoader('views'))

class Root(object):
    def __init__(self):
        self.cd = cluster_documents()
        self.localDir = os.path.dirname(__file__)
        self.absDir = os.path.join(os.getcwd(), self.localDir)
    
    @cherrypy.expose
    def index(self):
        tmpl = env.get_template('index.html')
        return tmpl.render() 

    @cherrypy.expose
    def search_text(self, search):
        file_name_output = str(ObjectId())
        self.cd.retrieve_data(search, file_name_output, prefix='files/')
        tmpl = env.get_template('download.html')
        return tmpl.render({
            'nome_arquivo':os.getcwd()+'/files/'+file_name_output+'.zip',
            'expressao':search
            })

    @cherrypy.expose
    def download_file(self, file_name):
        # subprocess.run('rm {}/files/*.docx'.format(os.getcwd()), shell=True)
        path = os.path.join(self.absDir, file_name)[:-1]
        return static.serve_file(path, 'application/x-download',
                                 'attachment', os.path.basename(path))

config = {
    '/css':
    { 'tools.staticdir.on':True,
        'tools.staticdir.dir': os.getcwd()+"/views/css/"
    },
}
config = {
    'global': {
        'server.socket_host': '0.0.0.0',
        'server.socket_port': int(os.environ.get('PORT', 5000)),
    }
}
# cherrypy.config.update({'server.socket_port': 8055})
cherrypy.quickstart(Root(),'/',config=config)