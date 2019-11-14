import os
from subprocess import Popen, PIPE


def install_packages():
	packages = Popen('sudo apt-get install -y p7zip', shell=True, stdin=PIPE )
	out, err = packages.communicate()
	print(out)
	return True
