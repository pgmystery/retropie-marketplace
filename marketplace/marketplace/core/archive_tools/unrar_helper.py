# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE
import os

from dialog.gauge import GaugeDialog
from get_path import get_path
from get_os import get_os_architecture


os_architecture = get_os_architecture()
if os_architecture == "32bit":
	unrar_file = "unrar_32"
elif os_architecture == "64bit":
	unrar_file = "unrar_64"
else:
	print("ERROR")
	exit()


path = get_path()


def get_files(archive):
	files = []
	archive_process = Popen([path + "/tools/" + unrar_file, "lt", archive], stdout=PIPE)
	file = ""
	for line in iter(archive_process.stdout.readline, b""):
		line = line.lstrip().replace("\r\n", "").replace("\n", "")
		if len(line) > 0:
			if line.startswith("Name: "):
				file = line.replace("Name: ", "")
			elif line.startswith("Type: "):
				if "file" in line.lower():
					files.append(file)
	return files


def extract_files(archive, files_to_extract, path_to_extract):
	files_to_extract2 = files_to_extract[:]

	uncompress_size = 0
	archive_process = Popen([path + "/tools/" +  unrar_file, "lt", "-y", archive], stdout=PIPE)
	file = ""
	for line in iter(archive_process.stdout.readline, b""):
		line = line.lstrip()
		if line.startswith("Name: "):
			file = line.replace("Name: ", "").replace("\r\n", "").replace("\n", "")
		elif line.startswith("Size: "):
			if file in files_to_extract:
				uncompress_size += int(line.replace("Size: ", "").replace("\r\n", "").replace("\n", ""))


	dialog_title = "Extracting Game..."
	dialog_description = "Extracting Game...\nPlease Wait!"

	extracting_dialog = GaugeDialog(dialog_title, dialog_description, max_value=uncompress_size)

	for file in files_to_extract:
		file_path_complete = path_to_extract + file
		if os.path.isfile(file_path_complete):
			os.remove(file_path_complete)
		file_path = os.path.dirname(os.path.abspath(file_path_complete))
		if not os.path.exists(file_path):
			os.makedirs(file_path)

	cmd = [path + "/tools/" +  unrar_file, "p", "-y", "-idcdp", archive]

	cmd.extend(files_to_extract)
	cmd.append(path_to_extract)

	archive_process = Popen(cmd, stdout=PIPE, bufsize=-1)

	indicator = "------ "
	current_size = 0
	current_file = None
	current_file_changed = False
	first_line = False
	for line in iter(archive_process.stdout.readline, b""):
		line = line.rstrip("\n")
		if line[:1] == "-":
			if line[:len(indicator)] == indicator:
				for current_file_path in files_to_extract2:
					if current_file_path in line:
						if current_file:
							current_file.close()
						current_file = open(path_to_extract + current_file_path, "w+")
						files_to_extract2.remove(current_file_path)
						current_file_changed = True
						first_line = True
						break
				if current_file_changed:
					continue
		if current_file_changed:
			current_file_changed = False
			continue
		if current_file:
			if first_line:
				first_line = False
			else:
				line = "\n" + line
			current_size += len(line)
			extracting_dialog.set_progress(current_size)
			current_file.write(line)
	if current_file:
		current_file.close()
	extracting_dialog.close()

	return True
