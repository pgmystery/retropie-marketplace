from subprocess import Popen, PIPE


def get_files(archive):
	files = []
	archive_file = Popen(["7zr", "l", "-ba", "-slt", archive], stdout=PIPE)
	archive_file.wait()
	out, err = archive_file.communicate()
	if out:
		for line in out.split("\n"):
			if line.startswith("Path = "):
				file = line.replace("Path = ", "")
				files.append(file)
		return files
	else:
		return files


def extract_files(archive, files_to_extract, path_to_extract):
	cmd = ["7zr", "e", "-y", archive, "-o" + path_to_extract]
	if type(files_to_extract) == str:
		cmd.append(files_to_extract)
	elif type(files_to_extract) == list:
		for file in files_to_extract:
			cmd.append(file)
	else:
		return False
	cmd.append("-r")
	# TODO: If the file already is in the outoup folder, ask the user to overrite it or not!!!
	archive_file = Popen(cmd, stdout=PIPE)
	archive_file.wait()
	# out, err = archive_file.communicate()
	return True
