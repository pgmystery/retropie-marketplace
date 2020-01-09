# -*- coding: utf-8 -*-
import os
import sys
import ntpath
import shutil
import urllib
from urlparse import urlsplit
import re
import requests
from importlib import import_module

from get_path import get_path
from dialog.info import InfoDialog
from dialog.gauge import GaugeDialog
from dialog.yesno import YesNoDialog
import etree


path = get_path()


try:
	store = sys.argv[1]
	game_to_install = sys.argv[2]
	# Delete illegal chars:
	illegal_chars = [
		"\\",
	]
	for char in illegal_chars:
		game_to_install = game_to_install.replace(char, "")
	game_downloadlink = sys.argv[3]
except IndexError:
	print("ERROR")

install_extension = None
install_extension_path = path + "/install_extensions/"
sys.path.append(install_extension_path)
if os.path.isfile(install_extension_path + store + ".py"):
	install_extension = import_module(store)

h = requests.head(game_downloadlink, allow_redirects=True)
header = h.headers
content_type = header.get('content-type')
if 'text' in content_type.lower():
	request_type = "post"
elif 'html' in content_type.lower():
	request_type = "post"
else:
	request_type = "get"

if not os.path.exists(path + "../tmp/"):
	os.makedirs(path + "../tmp/")

total_size = 100

InfoDialog("Downloading Game...", "Starting download!\nPlease wait...")

if request_type == "post":
	session = requests.Session()
	response = session.get(game_downloadlink)
	r = requests.post(game_downloadlink, cookies=session.cookies.get_dict(), stream=True)
elif request_type == "get":
	r = requests.get(game_downloadlink, stream=True)

if "content-disposition" in r.headers:
	fname = re.findall("filename=(.+)", r.headers['content-disposition'])[0].replace("\"", "")
else:
	fname = ntpath.basename(urlsplit(r.url)[2])
	fname = urllib.unquote(fname).decode('utf8')

total_size = int(r.headers.get('content-length', 0))

dialog_title = "Downloading ROM..."
dialog_description = "Downloading \"%s\"\nNeed to downloading %s Bytes\nPlease wait..." % (game_to_install, str("{:,}".format(total_size)))
download_dialog = GaugeDialog(dialog_title, dialog_description, max_value=total_size)

filepath = path + "../tmp/" + fname

with open(filepath, 'wb') as f:
	current_size = 0
	for chunk in r.iter_content(chunk_size=1024):
		if chunk:
			current_size += len(chunk)
			f.write(chunk)
			download_dialog.set_progress(current_size)

download_dialog.close()

InfoDialog("Install Game...", "Installing Game \"" + game_to_install + "\"\nPlease wait...")

with open("/etc/emulationstation/es_systems.cfg", "r") as f:
	xml_data = f.read()

root = etree.parse(xml_data)

system = None
systems = root.findall(".//system")
for s in systems:
	if s.find(".//name").text == store:
		system = s
		break

rom_path_object = system.find("./path")
rom_path = etree.tostring(rom_path_object).replace(" ", "").replace("\n", "") + "/"

extensions_object = system.find("./extension")
allowed_extensions = etree.tostring(extensions_object).replace("\n", "").split(" ")
allowed_extensions = filter(lambda extension: extension != "", allowed_extensions)

if install_extension:
	allowed_extensions = install_extension.load_extension(allowed_extensions)

extract_files = []
if filepath.endswith(".zip"):
	import archive_tools.zip_helper as unpacker
elif filepath.endswith(".tar"):
	import archive_tools.tar_helper as unpacker
elif filepath.endswith(".7z"):
	import archive_tools.sevenz_helper as unpacker
elif filepath.endswith(".rar"):
	import archive_tools.unrar_helper as unpacker
else:
	unpacker = None

if unpacker:
	files = unpacker.get_files(filepath)

	if len(files) > 0:
		for file in files:
			for extension in allowed_extensions:
				if file.endswith(extension):
					if os.path.isfile(rom_path + "/" + ntpath.basename(file)):
						yesNoDialog = YesNoDialog("Override file?", "The file '%s' already existing. Do you want to override this file?" % ntpath.basename(file))
						if yesNoDialog.answer == False:
							continue
					extract_files.append(file)
		if len(extract_files) > 0:
			unpacker.extract_files(filepath, extract_files, rom_path)
else:
	for extension in allowed_extensions:
		if filepath.endswith(extension):
			shutil.move(filepath, rom_path)

InfoDialog("Install Game...", "Installing Game \"" + game_to_install + "\"\nPlease wait...")

if install_extension:
	data = {
		"path": path,
		"rom_path": rom_path,
		"game_to_install": game_to_install,
		"extract_files": extract_files,
	}
	install_extension.after_install(data)

if os.path.exists(filepath):
	os.remove(filepath)
