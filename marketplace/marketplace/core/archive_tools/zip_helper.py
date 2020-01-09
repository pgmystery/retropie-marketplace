# -*- coding: utf-8 -*-
import os
import zipfile

from dialog.gauge import GaugeDialog


def get_files(archive):
	files = []
	with zipfile.ZipFile(archive, 'r') as zip_ref:
		for file in zip_ref.namelist():
			if not file.endswith("/"):
				files.append(file)
	return files


def extract_files(archive, files_to_extract, path_to_extract):
	if type(files_to_extract) == str:
		files_to_extract = [files_to_extract]

	with zipfile.ZipFile(archive, "r") as zip_file:
		uncompress_size = 0.0
		for file in zip_file.infolist():
			if file.filename in files_to_extract:
				uncompress_size += float(file.file_size)
		current_size = 0
		block_size = 1024

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

			i = zip_file.open(file)
			o = open(path_to_extract + file, "w+")
			while True:
				b = i.read(block_size)
				current_size += len(b)
				extracting_dialog.set_progress(current_size)
				if b == "":
					break
				o.write(b)
			i.close()
			o.close()
		extracting_dialog.close()

	return True
