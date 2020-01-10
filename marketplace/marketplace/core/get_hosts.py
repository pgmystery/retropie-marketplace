from os import listdir
from os.path import isfile, join, splitext
import sys
import importlib


def get_hosts(args):
	try:
		hosts_dir = args[1]
		sys.path.append(hosts_dir)
		if len(args) > 2:
			em_system = args[2]
		else:
			em_system = None
	except IndexError:
		return "ERROR"

	hosts_list = ""

	for f in listdir(hosts_dir):
		if isfile(join(hosts_dir, f)) and f.endswith(".py") and f != "__init__.py" and f != "Host.py":
			host = splitext(f)[0]
			if em_system:
				host_module = importlib.import_module(host)
				host_systems = host_module.emulators.keys()
				if em_system in host_systems:
					hosts_list += host + "\n"
			else:
				hosts_list += host + "\n"

	if len(hosts_list) > 0:
		return hosts_list.rsplit("\n", 1)[0]
	else:
		return "false"


if __name__ == "__main__":
	print(get_hosts(sys.argv))
