import sys
from os import path
import urllib2
import requests
from lxml import etree


emulators = {
	"psx": "playstation",
	"snes": "super-nintendo",
	"nes": "nintendo",
	"gb": "gameboy",
	"gba": "gameboy-advance",
	"gbc": "gameboy-color",
	"amstradcpc": "amstrad-cpc",
	"atari2600": "atari-2600",
	"atari5200": "atari-5200",
	"atari7800": "atari-7800",
	"atari800": "atari-800",
	"atarilynx": "atari-lynx",
	"gamegear": "game-gear",
	"mastersystem": "sega-master-system",
	"sega32x": "sega-32x",
	"n64": "nintendo-64",
	"neogeo": "neo-geo",
	"ngp": "neo-geo-pocket",
	"ngpc": "neo-geo-pocket-color",
	"sg-1000": "sega-sg1000",
	"zxspectrum": "zx-spectrum",
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

	page = 1

	header = {
		'User-Agent': '',
	}

	gamelist = ""

	while True:
		gamelist_url = "https://romsmania.cc/roms/%s/search?name=&genre=&region=&orderBy=name&orderAsc=1&page=%s" % (emulator, str(page))
		req = urllib2.Request(gamelist_url, headers=header)
		response = urllib2.urlopen(req)
		html = etree.HTML(response.read())
		gamelist_object = html.xpath("./body/table/tbody//tr")
		if len(gamelist_object) == 0:
			break
		for tr in gamelist_object:
			tr_a = tr.xpath("./td[1]/a")[0]
			gametext = etree.tostring(tr_a, method="text", encoding="UTF-8")
			for line in gametext.splitlines():
				if not line.isspace() and len(line) > 0:
					gamelist += line + "\n"
		page += 1
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
	emulator = emulators[emulator]

	# Delete illegal chars:
	illegal_chars = [
		"\\",
	]
	for char in illegal_chars:
		game_to_install = game_to_install.replace(char, "")

	url = "https://romsmania.cc/roms/%s/search?name=%s&genre=&region=&orderBy=name&orderAsc=1&page=1" % (emulator, game_to_install)

	header = {
		'User-Agent': '',
	}

	req = urllib2.Request(url, headers=header)
	response = urllib2.urlopen(req)

	html = etree.HTML(response.read())
	gamelink_object = html.xpath("./body/table/tbody/tr/td/a")[0]
	gamelink = gamelink_object.attrib['href']

	gamelink_name = gamelink.split("/")
	gamelink_name = gamelink_name[len(gamelink_name) - 1]

	game_downloadlink = "https://romsmania.cc/download/roms/%s/%s" % (emulator, gamelink_name)

	req = urllib2.Request(game_downloadlink, headers=header)
	response = urllib2.urlopen(req)
	
	html = etree.HTML(response.read())
	downloadlink_object = html.xpath("./body/div[@class='out']/div[@class='wait']/p[@class='wait__text']/a")[0]

	gamedownloadURL = downloadlink_object.attrib["href"]

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
