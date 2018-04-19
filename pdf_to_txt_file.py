# from pdfminer.pdfparser import PDFParser
# from pdfminer.pdfdocument import PDFDocument
# from pdfminer.pdfpage import PDFPage
# from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
# from pdfminer.converter import PDFPageAggregator
# from pdfminer.layout import LAParams, LTTextBox, LTTextLine
from pdfminer import *
import os

def pdf_to_files(fname):
	file_name = fname.split('.')
	fp = open(fname, 'rb')
	parser = PDFParser(fp)
	doc = PDFDocument(parser)
	rsrcmgr = PDFResourceManager()
	laparams = LAParams()
	device = PDFPageAggregator(rsrcmgr, laparams=laparams)
	interpreter = PDFPageInterpreter(rsrcmgr, device)
	counter = 0
	for page in PDFPage.create_pages(doc):
		file_aux = open(file_name[0] + '_' + str(counter) + '.txt','w')
		interpreter.process_page(page)
		layout = device.get_result()
		text = ''
		for lt_obj in layout:
			if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
				 text += lt_obj.get_text()
		file_aux.write(text)
		file_aux.close()

if __name__ == '__main__':
	cwd = os.getcwd()
	for file in os.listdir():
		try:
			pdf_to_files(file)
		except:
			pass