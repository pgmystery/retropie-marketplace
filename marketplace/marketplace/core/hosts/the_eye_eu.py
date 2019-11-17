import sys
from Host import Host


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


class TheEyeEu(Host):
	def __init__(self):
		super(TheEyeEu, self).__init__(emulators, emulators_link)

	def run(self, sys_argv, host=None):
		return super(TheEyeEu, self).run(sys_argv, self)

	def get_games(self, *args):
		emulator_origin = args[0][1]
		emulator = self.get_emulator(emulator_origin)
		emulator_link = self.get_emulator_link(emulator_origin)
		gamelist_url = "https://the-eye.eu/public/rom/%s/%s/" % (emulator, emulator_link)
		html = self.get_html(gamelist_url)
		gamelist_object = html.xpath("./body/div[1]/div/div[@class='ui left aligned stacked segment']/pre//a")
		gamelist_object.pop(0)
		gamelist_object.pop(len(gamelist_object) - 1)
		for game in gamelist_object:
			if game.text:
				self.add_game(game.text)
		return self.get_gameslist()

	def get_game_download_link(self, *args):
		emulator_origin = args[0][1]
		emulator = self.get_emulator(emulator_origin)
		emulator_link = self.get_emulator_link(emulator_origin)
		game_to_install = self.validate_game_to_install(args[0][2])
		url = "https://the-eye.eu/public/rom/%s/%s" % (emulator, emulator_link)
		html = self.get_html(url)
		downloadlink_object = html.xpath('.//a[text()="%s"]' % game_to_install)[0]
		gamedownloadURL = url + downloadlink_object.attrib["href"]
		return gamedownloadURL


if __name__ == "__main__":
	try:
		print(TheEyeEu().run(sys.argv))
	except:
		print("ERROR")
