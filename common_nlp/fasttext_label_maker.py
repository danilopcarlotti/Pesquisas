import csv, sys

class label_maker():
	"""
	Creates label file for fasttext from csv with labels and text
	The csv file must contain two rows.
	row[0] = labels separeted by , (comma)
	row[1] = text
	"""
	def __init__(self, fileName, output):
		self.fileName = fileName
		self.output = output

	def csv_iterator(self):
		csvfile = open(self.fileName)
		csvIterator = csv.reader(csvfile, delimiter=',', quotechar='"')
		return csvIterator

	def output_labels(self):
		labels = open(self.output+'.txt', 'w', encoding='utf8')
		csv_iterator = self.csv_iterator()
		next(csv_iterator)
		for row in csv_iterator:
			labels_list = row[0].split(',')
			labels_row = ''
			for l in labels_list:
				labels_row += '__label__'+l+' '
			labels.write(labels_row+row[1]+'\n')
		labels.close()

if __name__ == '__main__':
	c = label_maker(sys.argv[1],'label_'+sys.argv[1][:-4])
	c.output_labels()