from get_path import get_path


path = get_path()

with open(path + "../VERSION", "r") as f:
	version = f.read()

print(version)
