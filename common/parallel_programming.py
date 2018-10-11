from threading import Thread
from queue import Queue
import time

class parallel_programming(Thread):
	def __init__(self):
		Thread.__init__(self) 
		
	def run_f_nbatches(self, f, batch_f, nthreads=100):
		q = Queue()
		contador = 0
		for i in batch_f:
			if contador < nthreads:
				q.put(i)
				contador += 1
			else:
				q.put(i)
				threads = []
				while not q.empty():
					t = Thread(target=f, args=(q.get(),))
					t.start()
					threads.append(t)
				for th in threads:
					th.join()
				contador = 0
		threads = []
		while not q.empty():
			t = Thread(target=f, args=(q.get(),))
			t.start()
		for th in threads:
			th.join()

def main():
	pass

if __name__ == '__main__':
	main()