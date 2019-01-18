import networkx as nx, re, sys, pandas as pd, matplotlib.pyplot as plt
from operator import itemgetter

class networkx_graphs():
	"""docstring for networkx_graphs"""
	def __init__(self, file_path=None):
		self.file_path = file_path
		self.graph = None

	def add_edges(self, data):
		for b, e in data:
			if self.graph.has_edge(b, e):
				self.graph[b][e]['weight'] += 1
			else:
				self.graph.add_edge(b, e, weight=1)

	def xls_dir_graph(self,originC,desctinationC):
		# originC = column representing origin of node of directional graph
		# desctinationC = column representing destination of node of directional graph
		# the number of connections between two vertices is represented as an attribute, 'weight', of the edge
		df = pd.read_excel(self.file_path, error_bad_lines=False)
		self.create_dir_graph()
		for index, row in df.iterrows():
			if self.graph.has_edge(row[originC], row[desctinationC]):
				self.graph[row[originC]][row[desctinationC]]['weight'] += 1
			else:
				self.graph.add_edge(row[originC], row[desctinationC], weight=1)

	def create_dir_graph(self):
		self.graph = nx.DiGraph()

	def create_mul_dir_graph(self):
		self.graph = nx.MultiGraph()

	def create_undir_graph(self):
		self.graph = nx.Graph()
	
	def degree_edges(self):
		return sorted([(n,d) for n, d in self.graph.degree()],key=lambda x: x[1],reverse=True)

	def get_edge_attributes(self, attr='weight', sorted_tuples=False):
		values_dic = nx.get_edge_attributes(self.graph,attr)
		if sorted_tuples:
			values = []
			for k,v in values_dic.items():
				values.append((k,v))
			values = sorted(values,key=lambda x: x[1],reverse=True)
		else:
			values = values_dic
		return values

	def simple_cycles(self):
		return list(nx.simple_cycles(self.graph))