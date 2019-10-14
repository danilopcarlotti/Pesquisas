import networkx as nx, re, sys, pandas as pd, matplotlib.pyplot as plt, os
from operator import itemgetter

class networkx_graphs():
	"""docstring for networkx_graphs"""
	def __init__(self, file_path=None):
		self.file_path = file_path

	def df_dir_graph(self,originC,destinationC, csvf=False, excelf=False):
		# originC = column representing origin of node of directional graph
		# destinationC = column representing destination of node of directional graph
		# the number of connections between two vertices is represented as an attribute, 'weight', of the edge
		if excelf:
			df = pd.read_excel(self.file_path, error_bad_lines=False)
		elif csvf:
			df = pd.read_csv(self.file_path, error_bad_lines=False)
		self.create_dir_graph()
		for index, row in df.iterrows():
			if self.graph.has_edge(row[originC], row[destinationC]):
				self.graph[row[originC]][row[destinationC]]['weight'] += 1
			else:
				self.graph.add_edge(row[originC], row[destinationC], weight=1)

	def closeness_centrality(self):
		return networkx.closeness_centrality(self.graph)

	def create_dir_graph(self):
		self.graph = nx.DiGraph()

	def create_mul_dir_graph(self):
		self.graph = nx.MultiGraph()

	def create_undir_graph(self):
		self.graph = nx.Graph()

	def degree_centrality(self):
		return networkx.degree_centrality(self.graph)
	
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

	def standard_report(self):
		nx.draw(self.graph,edge_color='b')
		plt.savefig(self.file_path.split('/')[-1][:-5]+'.png')
		dicionario_resultados = {
		'Nome do arquivo analisado' : self.file_path.split('/')[-1],
		'Nós que interagem entre si' : self.graph.nodes,
		'Ciclos fechados' : self.graph.simple_cycles(),
		'Quantidade de arestas que chegam ou saem dos nós' : self.graph.degree_edges(),
		'Quantidade de arestas entre nós' : self.graph.get_edge_attributes(sorted_tuples=True)
		}
		return dicionario_resultado