import os
import sys


def get_path():
	if getattr(sys, 'frozen', False):
		# frozen
		return os.path.dirname(sys.executable) + "/"
	else:
		# unfrozen
		return os.path.dirname(os.path.realpath(__file__)) + "/"
