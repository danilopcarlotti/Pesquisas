import speech_recognition as sr
from os import path
import sys

class transcrever_audio():
	"""Classe para transcrição em texto de áudio"""
	def __init__(self):
		pass		
	
	def transcrever(self,audio = None):
		if audio:
			AUDIO_FILE = audio
		else:
			AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "audio.wav")
		r = sr.Recognizer()
		with sr.AudioFile(AUDIO_FILE) as source:
			audio = r.record(source)
		try:
			return r.recognize_google(audio,language='pt')
		except:
		    return False

if __name__ == '__main__':
	t = transcrever_audio()
	print(t.transcrever(sys.argv[1]))