# -*- coding: utf-8 -*-
import sys
from lxml import etree
from Host import Host


emulators = {
	"atari2600": "atari2600",
	"atari5200": "atari5200",
	"atari7800": "atari7800",
	"atarilynx": "lynx",
	"gamegear": "gg",
	"gba": "gba",
	"gbc": "gbc",
	"mame-libretro": "mame",
	"mastersystem": "sms",
	"megadrive": "saturn",
	"n64": "n64",
	"nes": "nes",
	"ngp": "ngp",
	"pcengine": "pcengine",
	"psx": "psx",
	"segacd": "segacd",
	"snes": "snes",
	"vectrex": "vectrex",
}

class ROMHustler(Host):
	def __init__(self):
		super(ROMHustler, self).__init__(emulators)

	def run(self, sys_argv, host=None):
		return super(ROMHustler, self).run(sys_argv, self)

	def get_games(self, *args):
		emulator = self.get_emulator(args[0][1])
		page = 1
		counter = 0
		last_gamename = ""
		run_loop = True
		while run_loop and page < 1000:
			gamelist_url = "https://romhustler.org/roms/%s/page:%s/sort:Rom.title/direction:asc" % (emulator, str(page))
			html = self.get_html(gamelist_url)
			gameslist_object = html.xpath(".//div[@id='roms_table']")[0]
			for div in gameslist_object:
				if "class" in div.attrib and div.attrib["class"] == "row":
					gamelink_object_list = div.xpath("./div[@class='title']/a")
					if len(gamelink_object_list) > 0:
						gamename = etree.tostring(gamelink_object_list[0], method="text", encoding="UTF-8")
						if counter == 0:
							if last_gamename == gamename:
								run_loop = False
								break
							last_gamename = gamename
						counter += 1
						self.add_game(gamename)
			page += 1
			counter = 0
		return self.get_gameslist()

	def get_game_download_link(self, *args):
		emulator = self.get_emulator(args[0][1])
		game_to_install = self.validate_game_to_install(args[0][2])
		page = 1
		gamedownloadURL = ""
		while page < 10000:
			gamelist_url = "https://romhustler.org/roms/%s/page:%s/sort:Rom.title/direction:asc" % (emulator, str(page))
			html = self.get_html(gamelist_url)
			downloadlink_object_list = html.xpath('.//a[text()="%s"]' % game_to_install)
			if len(downloadlink_object_list) > 0:
				downloadlink_object = downloadlink_object_list[0]
				gamedownloadURL = "https://romhustler.org/" + downloadlink_object.attrib["href"]
				break
			page += 1

		html = self.get_html(gamedownloadURL)
		downloadlink_object = html.xpath('.//a[@title="%s"]' % game_to_install)[0]
		gamedownloadURL = downloadlink_object.attrib["href"]
		game_id = gamedownloadURL.split("/")[2]

		gamedownloadURL = self.get_json("https://romhustler.org/link/" + game_id)["hashed"]

		return gamedownloadURL


if __name__ == "__main__":
	try:
		print(ROMHustler().run(sys.argv))
	except:
		print("ERROR")
