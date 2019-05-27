import re, os

class recursive_folders():
	"""Find all files in a series of folders recursively and, if desired, apply a function"""
	def __init__(self):
		pass

	def find_file_or_folder(self, file_or_folder, paths):
		try:
			folder = os.listdir(file_or_folder)
			for f in folder:
				self.find_file_or_folder(file_or_folder+'/'+f,paths)
		except Exception as e:
			paths.append(file_or_folder)

	def find_files(self,ini_path):
		paths = []
		self.find_file_or_folder(ini_path, paths)
		return paths

	def apply_f_files(self, ini_path, f):
		paths = self.find_files(ini_path)
		for a in paths:
			f(a)

def main():
	r = recursive_folders()
	paths = r.find_files('')
	print(paths)

if __name__ == '__main__':
	main()