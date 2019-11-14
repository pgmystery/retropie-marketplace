import os
import sys
from subprocess import Popen
from install_lxml_requiremens import install_lxml_requiremens


def install_venv(install_path):
	if getattr(sys, 'frozen', False):
		# frozen
		path = os.path.dirname(sys.executable) + "/"
	else:
		# unfrozen
		path = os.path.dirname(os.path.realpath(__file__)) + "/"

	if not install_lxml_requiremens():
		return False

	if not os.path.isdir(install_path):
		os.makedirs(install_path)
		venv = Popen(["python", path + "virtualenv.py", install_path])
		out, err = venv.communicate()
		print(out)

		# INSTALL REQUIREMENTS:
		requirements_path = path + "requirements.txt"
		if os.path.isfile(requirements_path):
			python_venv_path = install_path + "/bin/python"
			if os.path.isfile(python_venv_path):
				requirements = Popen([python_venv_path, "-m", "pip", "install", "-r", requirements_path])
				out, err = requirements.communicate()
				print(out)
				return True
	return False
