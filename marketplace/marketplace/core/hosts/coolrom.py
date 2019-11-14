import sys
from os import path
import urllib2
import requests
from lxml import etree


emulators = {
	"psx": "psx",
	"atari2600": "atari2600",
	"atari5200": "atari5200",
	"atari7800": "atari7800",
	"neogeo": "neogeo",
	"ngp": "neogeopocket",
	"gamegear": "gamegear",
	"mastersystem": "mastersystem",
}


def get_supported_emulators(*args, **kwargs):
	# try:
	# 	emulator = args[0][1]
	# except IndexError:
	# 	return "ERROR"

	# if emulator in emulators.keys():
	# 	return "true"
	# else:
	# 	return "false"
	return emulators.keys()


def get_games(*args, **kwargs):
	try:
		emulator = args[0][1]
	except IndexError:
		return "ERROR"

	if not emulator in emulators.keys():
		return "ERROR"
	emulator = emulators[emulator]
	gamelist_url = "http://coolrom.com/roms/%s/all/" % emulator
	try:
		response = urllib2.urlopen(gamelist_url)
	except:
		return "ERROR"
	html = etree.HTML(response.read())
	gamelist_object = html.xpath("./body/center/table/tr/td/table/tr[4]/td/table/tr/td/font/font")[0]
	for e in gamelist_object:
		if e.tag != "br":
			gamelist_object.remove(e)
	for e in gamelist_object.xpath("//br"):
		e.tail = "\n" + e.tail if e.tail else "\n"
	etree.strip_elements(gamelist_object,'br',with_tail=False)
	gamelist_object = etree.tostring(gamelist_object, method="text", encoding="UTF-8")
	gamelist = ""
	for line in gamelist_object.splitlines():
		if not line.isspace() and len(line) > 0:
			gamelist += line + "\n"
	gamelist = gamelist.rsplit("\n",1)[0]

	return gamelist


def get_game_download_link(*args, **kwargs):
	try:
		emulator = args[0][1]
		game_to_install = args[0][2]
	except IndexError:
		return "ERROR"

	if not emulator in emulators.keys():
		return "ERROR"
	emulator = emulators[emulator]

	# Delete illegal chars:
	illegal_chars = [
		"\\",
	]
	for char in illegal_chars:
		game_to_install = game_to_install.replace(char, "")

	# get URL:
	firstChar = game_to_install[:1]
	if firstChar.isalpha():
		url = "http://coolrom.com/roms/psx/%s/" % firstChar.lower()
	else:
		url = "http://coolrom.com/roms/psx/0/"

	try:
		response = urllib2.urlopen(url)
	except:
		print("ERROR")
		exit()

	html = etree.HTML(response.read())

	gamelist_object = html.xpath("./body/center/table/tr/td/table/tr[4]/td/table/tr/td/font/font")[0]

	gamelink = None
	for div in gamelist_object.xpath("//div"):
		if len(div.xpath("./a")) > 0:
			gamelink = div.xpath("./a")[0]
			game = etree.tostring(gamelink, method="text", encoding="UTF-8")
			if game == game_to_install:
				break

	if gamelink is None:
		print("ERROR")
		exit()

	gameURL = gamelink.attrib['href']

	if not gameURL:
		print("ERROR")
		exit()

	try:
		response = urllib2.urlopen("http://coolrom.com" + gameURL)
	except:
		print("ERROR")
		exit()

	html = etree.HTML(response.read())
	gamedownload_object = html.xpath("./body/center/table/tr/td/table/tr[4]/td/table/tr/td/center/a")[0]
	gamedownloadURL = gamedownload_object.attrib['href']
	gamedownloadURL = gamedownloadURL[gamedownloadURL.find("/dlpop.php?"):]
	gamedownloadURL = gamedownloadURL[:gamedownloadURL.find("'")]

	try:
		response = urllib2.urlopen("http://coolrom.com/" + gamedownloadURL)
	except:
		print("ERROR")
		exit()

	html = etree.HTML(response.read())
	html_text = etree.tostring(html, method="html", pretty_print=True)

	html_text_dlLink = html_text.find("http://dl.coolrom.com/dl/")
	gamedownloadURL = html_text[html_text_dlLink:html_text.find("\"", html_text_dlLink)]

	return gamedownloadURL


if __name__ == "__main__":
	try:
		run = sys.argv[1]
		if run == "get_games":
			print(get_games(sys.argv[1:len(sys.argv)]))
		elif run == "get_game_download_link":
			print(get_game_download_link(sys.argv[1:len(sys.argv)]))
		else:
			print("ERROR")
	except IndexError:
		print("ERROR")
