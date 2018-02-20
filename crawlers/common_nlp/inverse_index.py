import collections
from textNormalization import textNormalization

class inverted_index(textNormalization):
	"""Class for creating and manipulating inverted indexes"""
	def __init__(self):
		self.inv_index = collections.defaultdict(set)

i = inverted_index()
print(i.tokenizer())