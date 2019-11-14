import os
from subprocess import Popen, PIPE


def install_lxml_requiremens():
	lxml_requirements = Popen('sudo apt-get install -y libxml2-dev libxslt-dev python-dev', shell=True, stdin=PIPE )
	out, err = lxml_requirements.communicate()
	print(out)
	return True
