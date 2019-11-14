import zipfile


def get_files(archive):
	files = []
	with zipfile.ZipFile(archive, 'r') as zip_ref:
		for file in zip_ref.namelist():
			files.append(file)
	return files


def extract_files(archive, files_to_extract, path_to_extract):
	if type(files_to_extract) == str:
		files_to_extract = [files_to_extract]
	with zipfile.ZipFile(archive, 'r') as zip_ref:
		for file in files_to_extract:
			zip_ref.extract(file, path_to_extract)
	return True
