# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE, STDOUT
import os

from dialog.gauge import GaugeDialog
from get_path import get_path
from get_os import get_os_architecture


os_architecture = get_os_architecture()
if os_architecture == "32bit":
	sevenz_file = "7zr_32"
elif os_architecture == "64bit":
	sevenz_file = "7zr_64"
else:
	print("ERROR")
	exit()


path = get_path()


def get_files(archive):
	files = []
	archive_process = Popen([path + "/tools/" + sevenz_file, "l", "-ba", "-slt", archive], stdout=PIPE)
	file = ""
	for line in iter(archive_process.stdout.readline, b""):
		if line.startswith("Path = "):
			file = line.replace("Path = ", "")
		elif line.startswith("Attributes = "):
			file_attributes = line.replace("Attributes = ", "")
			if file_attributes[0:1].lower() != "d":
				files.append(file.replace("\r\n", "").replace("\n", ""))
	return files


def extract_files(archive, files_to_extract, path_to_extract):
	if type(files_to_extract) == str:
		files_to_extract = [files_to_extract]

	uncompress_size = 0
	archive_file = Popen([path + "/tools/" + sevenz_file, "l", "-ba", "-slt", archive], stdout=PIPE)
	out, err = archive_file.communicate()
	if out:
		file = None
		for line in out.split("\n"):
			if line.startswith("Path = "):
				file = line.replace("Path = ", "")
			elif line.startswith("Size = "):
				if file in files_to_extract:
					uncompress_size += int(line.replace("Size = ", ""))

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

	cmd = [path + "/tools/" + sevenz_file, "x", "-y", "-ba", "-so", archive, "-o" + path_to_extract]
	cmd.extend(files_to_extract)
	archive_process = Popen(cmd, stdout=PIPE, stderr=STDOUT, bufsize=-1)

	files_to_extract2 = files_to_extract[:]
	current_size = 0
	end_indicator = "Everything is Ok"
	indicator = "Extracting  "
	current_file = None
	empty_line = 0
	first_line = False
	for line in iter(archive_process.stdout.readline, b''):
		line = line.rstrip("\n")
		if current_file and line == "":
			empty_line += 1
			if empty_line > 2:
				empty_line -= 1
				current_size += len("\n")
				extracting_dialog.set_progress(current_size)
				current_file.write("\n")
			continue
		else:
			if line[:1] == indicator[:1]:
				if line[:len(end_indicator)] == end_indicator:
					empty_line -= 1
					if current_file and empty_line > 0:
						for l in range(empty_line):
							current_size += len("\n")
							extracting_dialog.set_progress(current_size)
							current_file.write("\n")
					break
				if line[:len(indicator)] == indicator:
					line_temp = line[len(indicator):]
					for file in files_to_extract2:
						if line_temp[:len(file)] == file:
							if current_file:
								if empty_line > 0:
									for l in range(empty_line):
										current_size += len("\n")
										extracting_dialog.set_progress(current_size)
										current_file.write("\n")
									empty_line = 0
								current_file.close()
							files_to_extract2.remove(file)
							current_file = open(path_to_extract + file, "w+")
							line = line_temp[len(file):]
							first_line = True
							break
		if current_file:
			if empty_line > 0:
				for l in range(empty_line):
					line = "\n" + line
				empty_line = 0
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

