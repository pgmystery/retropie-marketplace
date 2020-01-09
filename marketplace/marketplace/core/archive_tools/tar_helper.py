# -*- coding: utf-8 -*-
import os
import tarfile

from dialog.gauge import GaugeDialog


def get_files(archive):
	files = []
	with tarfile.open(archive, mode="r") as tar_ref:
		for file in tar_ref.getmembers():
			if file.isfile():
				files.append(file.name)
	return files


def extract_files(archive, files_to_extract, path_to_extract):
	if type(files_to_extract) == str:
		files_to_extract = [files_to_extract]

	with tarfile.open(archive, mode="r") as tar_file:
		uncompress_size = 0.0
		for file in tar_file.getmembers():
			if file.name in files_to_extract:
				uncompress_size += float(file.size)
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

			i = tar_file.extractfile(file)
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
