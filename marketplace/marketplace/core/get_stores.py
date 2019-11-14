import sys
import importlib
import json

from get_path import get_path
from get_hosts import get_hosts


path = get_path()

with open(path + "/../" + "systems.json") as f:
     systems = json.load(f)


def get_stores(args):
	try:
		hosts_dir = args[0]
	except IndexError:
		return "ERROR"
	hosts = get_hosts([None, hosts_dir]).split("\n")
	sys.path.append(hosts_dir)
	stores = []
	for host in hosts:
		host_module = importlib.import_module(host)
		host_stores = host_module.get_supported_emulators()
		for store in host_stores:
			if store in systems.keys():
				if systems[store] not in stores:
					stores.append(systems[store])
			else:
				if store not in stores:
					stores.append(store)
	stores = "\n".join(stores)
	return stores


def get_system_name(args):
	system_name = args[0]
	for system, name in systems.items():
		if name == system_name:
			return system
	return "ERROR"


if __name__ == "__main__":
	if sys.argv[1] == "stores":
		print(get_stores(sys.argv[2:]))
	elif sys.argv[1] == "system_name":
		print(get_system_name(sys.argv[2:]))
	else:
		print("ERROR")
