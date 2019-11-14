import os
import sys


def get_path():
	path = None
	if getattr(sys, 'frozen', False):
		# frozen
		path = os.path.dirname(sys.executable) + "/"
	else:
		# unfrozen
		path = os.path.dirname(os.path.realpath(__file__)) + "/"
	return path
