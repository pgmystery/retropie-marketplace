import os
import sys
import signal
import shutil
import urllib
import urllib2
from urlparse import urlsplit
import re
from subprocess import Popen, PIPE
import requests
from lxml import etree

from get_path import get_path


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

infoscreen = Popen(["/" + path + "../dialog/info.sh", "Downloading Game...", "Starting download!\nPlease wait..."])

if request_type == "post":
	session = requests.Session()
	response = session.get(game_downloadlink)

	r = requests.post(game_downloadlink, cookies=session.cookies.get_dict(), stream=True)

	if "content-disposition" in r.headers:
		fname = re.findall("filename=(.+)", r.headers['content-disposition'])[0].replace("\"", "")
	else:
		fname = os.path.basename(urlsplit(r.url)[2])
		fname = urllib.unquote(fname).decode('utf8')
elif request_type == "get":
	r = requests.get(game_downloadlink, stream=True)

	fname = os.path.basename(urlsplit(r.url)[2])
	fname = urllib.unquote(fname).decode('utf8')


total_size = int(r.headers.get('content-length', 0))

dialog_title = "Downloading ROM..."
dialog_description = "Downloading \"%s\"\nNeed to downloading %s Bytes\nPlease wait..." % (game_to_install, str("{:,}".format(total_size)))
process = Popen(["/" + path + "../dialog/gauge.sh", dialog_title, dialog_description], stdin=PIPE)
process.stdin.write('0\n')

filepath = path + "../tmp/" + fname

with open(filepath, 'wb') as f:
	current_size = 0
	current_progress = 0
	for chunk in r.iter_content(chunk_size=1024): 
		if chunk:
			current_size += len(chunk)
			f.write(chunk)
			progress = int((float(current_size) / float(total_size)) * 100.0)
			if current_progress < progress:
				current_progress = progress
				process.stdin.write(str(progress) + '\n')

out, err = process.communicate()  # NEED THIS, WITHOUT IT WILL BREAK!!!

infoscreen = Popen(["/" + path + "../dialog/info.sh", "Install Game...", "Installing Game \"" + game_to_install + "\"\nPlease wait..."])

with open("/etc/emulationstation/es_systems.cfg", "r") as f:
	xml_data = f.read()

root = etree.XML(xml_data)

system = root.xpath('//name[text()="%s"]' % store)[0].getparent()

rom_path_object = system.xpath("./path")[0]
rom_path = etree.tostring(rom_path_object, method="text", encoding="UTF-8").replace(" ", "").replace("\n", "") + "/"

extensions_object = system.xpath("./extension")[0]
allowed_extensions = etree.tostring(extensions_object, method="text", encoding="UTF-8").replace("\n", "").split(" ")
allowed_extensions = filter(lambda extension: extension != "", allowed_extensions)

if store == "psx":
	allowed_extensions.append(".bin")
	allowed_extensions.append(".BIN")
	allowed_extensions.append(".ecm")
	allowed_extensions.append(".ECM")


extract_files = []
if filepath.endswith(".zip"):
	import zip_helper as unpacker
elif filepath.endswith(".tar"):
	import tar_helper as unpacker
elif filepath.endswith(".7z"):
	import sevenz_helper as unpacker
elif filepath.endswith(".rar"):
	import unrar_helper as unpacker
else:
	unpacker = None

if unpacker:
	files = unpacker.get_files(filepath)

	if len(files) > 0:
		for file in files:
			for extension in allowed_extensions:
				if file.endswith(extension):
					extract_files.append(file)
		if len(extract_files) > 0:
			unpacker.extract_files(filepath, extract_files, rom_path)
else:
	for extension in allowed_extensions:
		if filepath.endswith(extension):
			shutil.move(filepath, rom_path)

# PSX-BIN:
if store == "psx":
	psx_bin_file = None
	for file in extract_files:
		if file.lower().endswith(".bin"):
			psx_bin_file = file
			break
	if psx_bin_file:
		if not os.path.isfile(rom_path + psx_bin_file[:len(psx_bin_file) - len(".bin")] + ".cue") and not os.path.isfile(rom_path + psx_bin_file[:len(psx_bin_file) - len(".bin")] + ".CUE"):
			yesno = Popen(["/" + path + "../dialog/yesno.sh", "Rename \".bin\"-file", "On the game: \"" + game_to_install + "\"\nThe downloaded ROM file has a \".bin\"-file without an \".cue\"-file. RetroPie don't support this! Do you want to rename the \".bin\"-file to \".iso\" and try that this will work?\nOn no, the \".bin\"-file will be deleted!", "true"], stdout=PIPE)
			yesno.wait()
			out, err = yesno.communicate()
			if out:
				if out.find("0") > -1:
					os.rename(rom_path + "/" + psx_bin_file, rom_path + "/" + psx_bin_file[:len(psx_bin_file) - len(".bin")] + ".iso")
				else:
					os.remove(rom_path + "/" + psx_bin_file)
			else:
				os.remove(rom_path + "/" + psx_bin_file)
			infoscreen = Popen(["/" + path + "../dialog/info.sh", "Install Game...", "Installing Game \"" + game_to_install + "\"\nPlease wait..."])

if os.path.exists(filepath):
	os.remove(filepath)
