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

	def create_random_tree(self, tree_data):
		array = tree_data[1:]
		random.shuffle(array)
		array.insert(0,(None, None))
		random_tree = self.create_decision_tree(array)
		return random_tree

	def create_decision_tree(self, tree_data):
		tree_data.insert(0,(None, None))
		root = None
		for i in range(1,(len(tree_data)//2)):
			node = decision_node(tree_data[i][0],tree_data[i][1])
			if i == 1:
				root = node
			node.left = decision_node(tree_data[i*2][0],tree_data[i*2][1])
			node.right = decision_node(tree_data[(i*2)+1][0],tree_data[(i*2)+1][1])
			node.left.father = node
			node.right.father = node
		root.father = root
		return root

	def classify(self,decision_node, text):
		if decision_node.decision(text):
			if decision_node.right.txt_class == 'NULL':
				return decision_node.txt_class
			else:
				return classify(decision_node.right, text)
		else:
			if decision_node.left.txt_class != 'NULL':
				return classify(decision_node.left, text)
			else:
				if decision_node.father != decision_node:
					return decision_node.father.txt_class
				else:
					return 'Class not found'

	def classify_tree(self, root):
		return classify(root)

# FALTA
# CRIAR COMO TESTAR A ACURÁCIA DE UMA ÁRVORE DE DECISÃO
# CLASSIFICAR TODA UMA QUANTIDADE DE TEXTOS E RETORNAR ISTO