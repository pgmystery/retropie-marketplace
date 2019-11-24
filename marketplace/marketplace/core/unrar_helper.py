from subprocess import Popen, PIPE
import shutil
import platform

from get_path import get_path


bit_version = platform.architecture()[0]
if bit_version == "32bit":
	unrar_file = "unrar_32"
elif bit_version == "64bit":
	unrar_file = "unrar_64"
else:
	print("ERROR")
	exit()


path = get_path()


def get_files(archive):
	files = []
	archive_file = Popen([path + "/tools/" + unrar_file, "lb", archive], stdout=PIPE)
	archive_file.wait()
	out, err = archive_file.communicate()
	if out:
		for line in out.split("\n"):
			if len(line) > 0:
				files.append(line)
		return files
	else:
		return files


def extract_files(archive, files_to_extract, path_to_extract):
	cmd = [path + "/tools/" +  unrar_file, "x", "-y", archive]
	tmp_dir = path + "/../tmp/"
	files = []
	if type(files_to_extract) == str:
		cmd.append(files_to_extract)
		files.append(tmp_dir + files_to_extract)
	elif type(files_to_extract) == list:
		for file in files_to_extract:
			cmd.append(file)
			files.append(tmp_dir + file)
	else:
		return False
	cmd.append(tmp_dir)
	# TODO: If the file already is in the output folder, ask the user to override it or not!!!
	archive_file = Popen(cmd, stdout=PIPE)
	archive_file.wait()
	for file in files:
		shutil.move(file, path_to_extract)
	return True
