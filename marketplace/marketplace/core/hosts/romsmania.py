import sys
from lxml import etree
from Host import Host


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


class ROMsMania(Host):
	def __init__(self):
		super(ROMsMania, self).__init__(emulators)

	def run(self, sys_argv, host=None):
		return super(ROMsMania, self).run(sys_argv, self)

	def get_games(self, *args):
		emulator = self.get_emulator(args[0][1])
		page = 1
		while True:
			gamelist_url = "https://romsmania.cc/roms/%s/search?name=&genre=&region=&orderBy=name&orderAsc=1&page=%s" % (emulator, str(page))
			html = self.get_html(gamelist_url)
			gamelist_object = html.xpath("./body/table/tbody//tr")
			if len(gamelist_object) == 0:
				break
			for tr in gamelist_object:
				tr_a = tr.xpath("./td[1]/a")[0]
				gametext = etree.tostring(tr_a, method="text", encoding="UTF-8")
				for line in gametext.splitlines():
					if not line.isspace() and len(line) > 0:
						self.add_game(line)
			page += 1
		return self.get_gameslist()

	def get_game_download_link(self, *args):
		emulator = self.get_emulator(args[0][1])
		game_to_install = self.validate_game_to_install(args[0][2])
		url = "https://romsmania.cc/roms/%s/search?name=%s&genre=&region=&orderBy=name&orderAsc=1&page=1" % (emulator, game_to_install)
		html = self.get_html(url)
		gamelink_object = html.xpath("./body/table/tbody/tr/td/a")[0]
		gamelink = gamelink_object.attrib['href']
		gamelink_name = gamelink.split("/")
		gamelink_name = gamelink_name[len(gamelink_name) - 1]
		game_downloadlink = "https://romsmania.cc/download/roms/%s/%s" % (emulator, gamelink_name)
		html = self.get_html(game_downloadlink)
		downloadlink_object = html.xpath("./body/div[@class='out']/center/div[@class='wait']/p[@class='wait__text']/a")[0]
		gamedownloadURL = downloadlink_object.attrib["href"]
		return gamedownloadURL


if __name__ == "__main__":
	try:
		print(ROMsMania().run(sys.argv))
	except:
		print("ERROR")
