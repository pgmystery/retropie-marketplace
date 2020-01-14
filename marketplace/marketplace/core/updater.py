# -*- coding: utf-8 -*-
import os
import urllib2
import re
import shutil
import zipfile
import requests

from get_path import get_path
from dialog.msgbox import MSGBoxDialog
from dialog.yesno import YesNoDialog
from dialog.info import InfoDialog
from dialog.gauge import GaugeDialog


path = get_path()


update_url = "https://raw.githubusercontent.com/pgmystery/retropie-marketplace/master/VERSION"
marketplace_url = "https://github.com/pgmystery/retropie-marketplace/archive/master.zip"


try:
	response = urllib2.urlopen(update_url)
except:
	MSGBoxDialog("Couldn't get version", "ERROR on getting the version!\nMaybe check your internet connection")
	exit()

newest_version = response.read().replace("\n", "")

with open(path + "/../VERSION", "r") as f:
	current_version = f.read().replace("\n", "")

if newest_version == current_version:
	MSGBoxDialog("Update", "You're using the latest version of the RetroPie-Marketplace!")
else:
	yesNoDialog = YesNoDialog("Update", "A new Update is available!\nDo you want to update the RetroPie-Marketplace?\nCurrent-Version=\"%s\" - Newest-Version=\"%s\"" % (current_version, newest_version))
	if yesNoDialog.answer:
		r = requests.get(marketplace_url, stream=True)
		fname = re.findall("filename=(.+)", r.headers['content-disposition'])[0].replace("\"", "")
		total_size = 0
		if "content-length" in r.headers:
			total_size = int(r.headers["content-length"])
		else:
			if "x-varnish" in r.headers:
				if r.headers["x-varnish"].isdigit():
					total_size = int(r.headers["x-varnish"])

		dialog_title = "Downloading UPDATE..."

		download_dialog = None
		if total_size > 0:
			dialog_description = "Downloading RetroPie-Marketplace v%s\nNeed to downloading %s Bytes\nPlease wait..." % (newest_version, str("{:,}".format(total_size)))
			download_dialog = GaugeDialog(dialog_title, dialog_description, max_value=total_size)
		else:
			InfoDialog(dialog_title, "Downloading RetroPie-Marketplace v%s\nPlease wait..." % newest_version)

		with open("/tmp/" + fname, 'wb') as f:
			current_size = 0
			for chunk in r.iter_content(chunk_size=1024):
				if chunk:
					current_size += len(chunk)
					f.write(chunk)
					if download_dialog:
						download_dialog.set_progress(current_size)

		if download_dialog:
			download_dialog.close()

		InfoDialog("Install Update...", "Installing RetroPie-Marketplace v" + newest_version + "\nPlease wait...")

		new_version_zip = zipfile.ZipFile("/tmp/" + fname)

		uncompress_size = float(sum((file.file_size for file in new_version_zip.infolist())))
		current_size = 0

		block_size = 1024

		update_path = "/tmp/"

		if os.path.isdir(update_path + "retropie-marketplace-master"):
			shutil.rmtree(update_path + "retropie-marketplace-master")

		dialog_title = "Extracting Update..."
		dialog_description = "Extracting Update...\nPlease wait!"

		extracting_dialog = GaugeDialog(dialog_title, dialog_description, max_value=uncompress_size)

		for file in new_version_zip.namelist():
			file_path_type = file[-1:]
			if file_path_type == "/" or file_path_type == "\\":
				file_path = update_path + file
				if os.path.isfile(file_path):
					os.remove(file_path)
				elif os.path.isdir(file_path):
					shutil.rmtree(update_path + file)
				os.makedirs(update_path + file)
				continue
			i = new_version_zip.open(file)
			o = open(update_path + file, "w+")
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

		os.remove("/tmp/" + fname)
