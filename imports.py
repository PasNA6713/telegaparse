import requests
import json
from collections import deque
from bs4 import BeautifulSoup as BS


class retry:
	def __init__(self, tries):
		self.tries = tries
        
	def __call__(self, func):
		def process(try_number:int=0, *args, **kwargs):
			try:
				func(*args, **kwargs)
			except requests.exceptions.ConnectionError:
				print("Failed")
				try_number += 1
				if try_number < self.tries:
					process(try_number, *args, **kwargs)
				else:
					print ("\nCan not parse, check your net connection")
		return process 
