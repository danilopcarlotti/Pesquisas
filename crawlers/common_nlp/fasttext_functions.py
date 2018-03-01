import fasttext, click

class fasttext_functions():
	"""
	Functions that create, train and predict based on fasttext models
	"""
	def __init__(self):
		pass

	def create_model_ft(self,labels):
		return fasttext.supervised(labels,'model_'+labels[:-4])

	def test_model(self,model,testFile):
		classifier = fasttext.load_model(model, encoding='utf-8')
		result = classifier.test(testFile)
		print ('P@1:', result.precision)
		print ('R@1:', result.recall)
		print ('Number of examples:', result.nexamples)

	def predict_text(self,model, text,k):
		classifier = fasttext.load_model(model, encoding='utf-8')
		labels_predict = classifier.predict(text,k)
		print(labels_predict)

@click.group()
def cli():
	pass

@click.command()
@click.option('--labels', help='Name of the txt file with labels')
def create_model(labels):
	f = fasttext_functions()
	f.create_model_ft(labels)

@click.command()
@click.option('--model', help='Name of the model file')
@click.option('--testfile', help='Name of the test file')
def test_ft_model(model,testfile):
	f = fasttext_functions()
	f.test_model(model,testfile)

@click.command()
@click.option('--model', help='Name of the model file')
@click.option('--text',help='Texto a ser predito')
@click.option('-k',default=2,help='Texto a ser predito')
def predict_ft_text(model,text,k):
	f = fasttext_functions()
	if text[-4:] == '.txt':
		lines = [line for line in open(text,'r')]
		f.predict_text(model,lines,k)
	else:
		f.predict_text(model,text,k)

cli.add_command(create_model)
cli.add_command(test_ft_model)
cli.add_command(predict_ft_text)

if __name__ == '__main__':
	cli()
