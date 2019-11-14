import sys
from os import path
import urllib2
import requests
from lxml import etree


emulators = {
	"psx": "Playstation",
	"n64": "Nintendo 64",
	"gb": "Nintendo Gameboy",
	"atari2600": "Atari 2600",
	"atari5200": "Atari 5200",
	"atari7800": "Atari 7800",
	"nes": "NES",
	"snes": "SNES",
	"gba": "Nintendo Gameboy Advance",
	"gbc": "Nintendo Gameboy Color",
	"sega32x": "Sega 32X",
	"atarilynx": "Atari Lynx",
	"mastersystem": "Sega Master System",
	"neogeo": "SNK Neo Geo",
	"ngp": "SNK Neo Geo Pocket",
	"ngpc": "SNK Neo Geo Pocket Color",
}

emulators_link = {
	"psx": "Games/NTSC/",
	"n64": "Roms/",
	"sega32x": "Games/",
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
	emulator_link = ""
	if emulator in emulators_link:
		emulator_link = emulators_link[emulator]
	emulator = emulators[emulator]

	header = {
		'User-Agent': '',
	}

	gamelist = ""
	gamelist_url = "https://the-eye.eu/public/rom/%s/%s/" % (emulator, emulator_link)
	req = urllib2.Request(gamelist_url, headers=header)
	response = urllib2.urlopen(req)
	html = etree.HTML(response.read())
	gamelist_object = html.xpath("./body/div[1]/div/div[@class='ui left aligned stacked segment']/pre//a")
	gamelist_object.pop(0)
	gamelist_object.pop(len(gamelist_object) - 1)
	for game in gamelist_object:
		if game.text:
			gamelist += game.text + "\n"
	gamelist = gamelist[:-1]

	return gamelist


def get_game_download_link(*args, **kwargs):
	try:
		emulator = args[0][1]
		game_to_install = args[0][2]
	except IndexError:
		return "ERROR"

	if not emulator in emulators.keys():
		return "ERROR"

	# Delete illegal chars:
	illegal_chars = [
		"\\",
	]
	for char in illegal_chars:
		game_to_install = game_to_install.replace(char, "")

	emulator_link = ""
	if emulator in emulators_link:
		emulator_link = emulators_link[emulator]
	emulator = emulators[emulator]

	header = {
		'User-Agent': '',
	}

	gamedownloadURL = ""

	url = "https://the-eye.eu/public/rom/%s/%s" % (emulator, emulator_link)

	req = urllib2.Request(url, headers=header)
	response = urllib2.urlopen(req)
	html = etree.HTML(response.read())

	downloadlink_object = html.xpath('.//a[text()="%s"]' % game_to_install)[0]

	gamedownloadURL = url + downloadlink_object.attrib["href"]

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
