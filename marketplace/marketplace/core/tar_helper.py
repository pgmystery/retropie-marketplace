import tarfile


def get_files(archive):
	files = []
	with tarfile.open(archive, mode="r") as tar_ref:
		for file in tar_ref.getmembers():
			files.append(file)
	return files


def extract_files(archive, files_to_extract, path_to_extract):
	if type(files_to_extract) == str:
		files_to_extract = [files_to_extract]
	with tarfile.open(archive, mode="r") as tar_ref:
		for file in files_to_extract:
			tar_ref.extract(file, path=path_to_extract)
	return True
