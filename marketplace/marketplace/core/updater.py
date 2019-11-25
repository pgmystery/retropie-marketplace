import os
import urllib2
from subprocess import Popen, PIPE
import re
import shutil
import zipfile
import requests

from get_path import get_path


path = get_path()


update_url = "https://raw.githubusercontent.com/pgmystery/retropie-marketplace/master/VERSION"
marketplace_url = "https://github.com/pgmystery/retropie-marketplace/archive/master.zip"


try:
	response = urllib2.urlopen(update_url)
except:
	msgbox = Popen(["/" + path + "../dialog/msgbox.sh", "Couldn't get version", "ERROR on getting the version!\nMaybe check your internet connection"])
	msgbox.wait()
	exit()

newest_version = response.read().replace("\n", "")

with open(path + "/../VERSION", "r") as f:
	current_version = f.read().replace("\n", "")

if newest_version == current_version:
	msgbox = Popen(["/" + path + "../dialog/msgbox.sh", "Update", "You're using the latest version of the RetroPie-Marketplace!"])
	msgbox.wait()
else:
	yesno = Popen(["/" + path + "../dialog/yesno.sh", "Update", "A new Update is available!\nDo you want to update the RetroPie-Marketplace?\nCurrent-Version=\"%s\" - Newest-Version=\"%s\"" % (current_version, newest_version), "true"], stdout=PIPE)
	yesno.wait()
	out, err = yesno.communicate()
	if out:
		if out.find("0") > -1:
			r = requests.get(marketplace_url, stream=True)
			fname = re.findall("filename=(.+)", r.headers['content-disposition'])[0].replace("\"", "")
			total_size = int(r.headers.get('content-length', 0))
			dialog_title = "Downloading UPDATE..."
			dialog_description = "Downloading RetroPie-Marketplace v%s\nNeed to downloading %s Bytes\nPlease wait..." % (newest_version, str("{:,}".format(total_size)))
			process = Popen(["/" + path + "../dialog/gauge.sh", dialog_title, dialog_description], stdin=PIPE)
			process.stdin.write('0\n')
			with open("/tmp/" + fname, 'wb') as f:
				current_size = 0
				current_progress = 0
				for chunk in r.iter_content(chunk_size=1024): 
					if chunk:
						current_size += len(chunk)
						f.write(chunk)
						if current_size > 0 and total_size > 0:
							progress = int((float(current_size) / float(total_size)) * 100.0)
						else :
							progress = 0
						if current_progress < progress:
							current_progress = progress
							process.stdin.write(str(progress) + '\n')
			out, err = process.communicate()  # NEED THIS, WITHOUT IT WILL BREAK!!!

			infoscreen = Popen(["/" + path + "../dialog/info.sh", "Install Update...", "Installing RetroPie-Marketplace v" + newest_version + "\nPlease wait..."])

			new_version_zip = zipfile.ZipFile("/tmp/" + fname)

			uncompress_size = float(sum((file.file_size for file in new_version_zip.infolist())))
			current_size = 0

			block_size = 1024

			progress = 0
			current_progress = 0

			update_path = "/tmp/"

			if os.path.isdir(update_path + "retropie-marketplace-master"):
				shutil.rmtree(update_path + "retropie-marketplace-master")

			dialog_title = "Extracting Update..."
			dialog_description = "Extracting Update...\nPlease wait!"
			process2 = Popen(["/" + path + "../dialog/gauge.sh", dialog_title, dialog_description], stdin=PIPE)
			process2.stdin.write('0\n')

			for file in new_version_zip.namelist():
				if file[-1:] == "/" or file[-1:] == "\\":
					os.makedirs(update_path + file)
					continue
				entry_info = new_version_zip.getinfo(file)
				i = new_version_zip.open(file)
				o = open(update_path + file, "w+")
				current_file_progress = 0
				while True:
					b = i.read(block_size)
					current_size += len(b)
					progress = int(float(current_size) / uncompress_size * 100.0)
					if current_progress < progress:
						current_progress = progress
						process2.stdin.write(str(progress) + '\n')
					if b == "":
						break
					o.write(b)
				i.close()
				o.close()

			out, err = process2.communicate()  # NEED THIS, WITHOUT IT WILL BREAK!!!

			os.remove("/tmp/" + fname)
