from parse_texto import busca
import random, re

class decision_node():
	def __init__(self, expression, txt_class):
		self.father = None
		self.left = None
		self.right = None
		self.expression = expression
		self.txt_class = txt_class

	def decision(self,text):
		return (busca(expression, text, ngroup=0) != '')		

class decision_tree_txt():
	"""
	Decision tree class for processing legal texts based on the ocurrence of regular expressions.
	This works because legal texts should necessarily contain certain keywords used to declare, rule, order, etc.	
	"""
	def __init__(self):
		pass

	def create_random_tree_vector(self, tree_data):
		array = tree_data[1:]
		random.shuffle(array)
		array.insert(0,(None, None))
		random_tree = self.create_decision_tree_vector(array)
		return random_tree

	def create_decision_tree_graph(self, tree_data):
		tree_data_example = '''
			tree_graph_example = 
			{
				'root' : {'node_father':'root','node_right':'node','node_left':'NULL', 'expression' : '', 'txt_class' : ''},
				'node' : {'node_father':'root','node_right':'NULL','node_left':'NULL', 'expression' : '', 'txt_class' : ''}	
			}
		'''
		print(tree_data_example)
	
	def create_decision_tree_vector(self, tree_data):
		tree_data.insert(0,(None, None))
		root = None
		for i in range(1,(len(tree_data)//2)):
			node = decision_node(tree_data[i][0],tree_data[i][1])
			if i == 1:
				root = node
				root.father = root
			node.left = decision_node(tree_data[i*2][0],tree_data[i*2][1])
			node.right = decision_node(tree_data[(i*2)+1][0],tree_data[(i*2)+1][1])
			node.left.father = node
			node.right.father = node
		return root

	def classify_node_graph(self,tree_data, decision_node, text):
		if busca(tree_data[decision_node]['expression'], text, ngroup=0) != '':
			if tree_data[decision_node]['right'] == 'NULL':
				return tree_data[decision_node]['txt_class']
			else:
				return classify_node_graph(tree_data,tree_data[tree_data[decision_node]['right']],text)
		else:
			if tree_data[decision_node]['left'] == 'NULL':
				if decision_node != 'root':
					return tree_data[tree_data[decision_node]['node_father']]['txt_class']
				else:
					return 'Class not found'
			else:
				return classify_node_graph(tree_data,tree_data[tree_data[decision_node]['left']],text)

	def classify_node_vector(self,decision_node, text):
		if decision_node.decision(text):
			if decision_node.right.txt_class == 'NULL':
				return decision_node.txt_class
			else:
				return classify_node(decision_node.right, text)
		else:
			if decision_node.left.txt_class == 'NULL':
				if decision_node.father != decision_node:
					return decision_node.father.txt_class
				else:
					return 'Class not found'
			else:
				return classify_node(decision_node.left, text)

	def classify_tree_vector(self, root):
		return classify_node(root)

## FALTA
# CRIAR COMO TESTAR A ACURÁCIA DE UMA ÁRVORE DE DECISÃO
# CLASSIFICAR TODA UMA QUANTIDADE DE TEXTOS E RETORNAR ISTO