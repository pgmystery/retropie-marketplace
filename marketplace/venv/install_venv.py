import os
import sys
from subprocess import Popen


def install_venv(install_path):
	if getattr(sys, 'frozen', False):
		# frozen
		path = os.path.dirname(sys.executable) + "/"
	else:
		# unfrozen
		path = os.path.dirname(os.path.realpath(__file__)) + "/"

	if not os.path.isdir(install_path):
		os.makedirs(install_path)
		venv = Popen(["python", path + "virtualenv.py", install_path])
		out, err = venv.communicate()
		print(out)

		# INSTALL REQUIREMENTS:
		requirements_path = path + "requirements.txt"
		python_venv_path = install_path + "/bin/python"
		if os.path.isfile(requirements_path):
			if os.path.isfile(python_venv_path):
				requirements = Popen([python_venv_path, "-m", "pip", "install", "-r", requirements_path])
				out, err = requirements.communicate()
				print(out)

		# INSTALL ADDITINAL PACKAGES:
		packages_path = path + "packages/"
		for root, dirs, filenames in os.walk(packages_path):
			for dir in dirs:
				if os.path.exists(packages_path + dir + "/setup.py"):
					setup_process = Popen([python_venv_path, "-m", "pip", "install", packages_path + dir])
					out, err = setup_process.communicate()
					print(out)
			break

		return True
	return False
