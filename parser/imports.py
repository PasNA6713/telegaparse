import requests
import json
import random
from collections import deque
from bs4 import BeautifulSoup as BS
import threading
import time


class retry:
	def __init__(self, tries):
		self.tries = tries
        
	def __call__(self, func):
		def process(*args, **kwargs):
			try:
				result = func(*args, **kwargs)
				return result
			except requests.exceptions.ConnectionError:
				print("Failed")
				self.tries -= 1
				if self.tries:
					process(try_number, *args, **kwargs)
				else:
					print ("\nCan not parse, check your net connection")
		return process 
