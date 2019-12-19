import cherrypy, json, pymongo, sys, os
from os.path import abspath
from jinja2 import Environment, FileSystemLoader
sys.path.append('../')
from mongoURI import mongoURI
sys.path.append('../../')
from common.active_learning_logreg import active_learning_logreg

env = Environment(loader=FileSystemLoader('views'))

class Root(object):
    def __init__(self, active_learning_logreg):
        self.active_learning_logreg = active_learning_logreg
    
    @cherrypy.expose
    def index(self):
        texts_to_classify = self.active_learning_logreg.doc_collection.count_documents({'to_classify':1})
        if not texts_to_classify:
            tmpl = env.get_template('index_no_texts.html')
            return tmpl.render({'tipo_texto':'Direito X','model_score':self.active_learning_logreg.model_score})
        else:
            tmpl = env.get_template('index.html')
            return tmpl.render({'tipo_texto':'Direito X','n_textos_classificar':texts_to_classify})   

    @cherrypy.expose
    def classify_text(self, textId, item_class):
        self.active_learning_logreg.update_one({'_id':textId},{'$set':{
            'class_human':item_class,
            'to_classify':0
        }})
        texts_to_classify = self.active_learning_logreg.doc_collection.count_documents({'to_classify':1})
        if not texts_to_classify:
            stop_or_not = self.active_learning_logreg.stop_model_check()
            if stop_or_not:
                self.active_learning_logreg.dump_model()
            else:
                self.active_learning_logreg.update_model()
                self.active_learning_logreg.find_K_documents()
        return self.index()

    @cherrypy.expose
    def get_decision(self):
        tmpl = env.get_template('get_decision.html')
        raw_text = ''
        textId = ''
        item_classes = [('-1','Talvez'),('0','Impertinente'),('1','Pertinente')]
        return tmpl.render({'raw_text':raw_text,'textId':textId,'item_classes':item_classes})

PATH_MODEL = os.getcwd()

# actv_lrn = active_learning_logreg(self, N, K, threshold_delta, csv_path, path_model_save, uri_mongo=None)
actv_lrn = active_learning_logreg(30, 20, 0.4, 'csv_path.csv', PATH_MODEL, uri_mongo=None)

# actv_lrn = 1

cherrypy.config.update({'server.socket_port': 8099})
cherrypy.quickstart(Root(actv_lrn),'/')