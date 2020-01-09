import sys
from Host import Host
import etree


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


class CoolROM(Host):
	def __init__(self):
		super(CoolROM, self).__init__(emulators)

	def run(self, sys_argv, host=None):
		return super(CoolROM, self).run(sys_argv, self)

	def get_games(self, *args):
		emulator = self.get_emulator(args[0][1])
		gamelist_url = "http://coolrom.com/roms/%s/all/" % emulator
		html = self.get_html(gamelist_url)
		gamelist_object = html.find("./body/center/table//tr/td/table//tr[4]/td/table//tr/td/font/font")
		for e in gamelist_object:
			if e.tag == "br":  # TODO: THE FIRST GAME IS NOT IN A BR...
				gamename = etree.tostring(e)
				text = gamename.replace("\t", "").replace("\n", "")
				if text:
					self.add_game(gamename)
		return self.get_gameslist()

	def get_game_download_link(self, *args):
		game_to_install = self.validate_game_to_install(args[0][2])
		firstChar = game_to_install[:1]
		if firstChar.isalpha():
			url = "http://coolrom.com/roms/psx/%s/" % firstChar.lower()
		else:
			url = "http://coolrom.com/roms/psx/0/"
		html = self.get_html(url)
		gamelist_object = html.find("./body/center/table//tr/td/table//tr[4]/td/table//tr/td/font/font")
		gamelink = None
		for div in gamelist_object.findall("./div"):
			if len(div.findall("./a")) > 0:
				gamelink = div.find("./a")
				game = etree.tostring(gamelink)
				if game == game_to_install:
					break

		if gamelink is None:
			return "ERROR"

		gameURL = gamelink.attrib['href']

		if not gameURL:
			return "ERROR"

		html = self.get_html("http://coolrom.com" + gameURL)
		gamedownload_object = html.find("./body/center/table//tr/td/table//tr[4]/td/table//tr/td/font/center/a")
		gamedownloadURL = gamedownload_object.attrib['href']
		gamedownloadURL = gamedownloadURL[gamedownloadURL.find("/dlpop.php?"):]
		gamedownloadURL = gamedownloadURL[:gamedownloadURL.find("'")]

		html = self.get_html("http://coolrom.com/" + gamedownloadURL)
		html_text = etree.tostring(html)

		html_text_dlLink = html_text.find("http://dl.coolrom.com")
		gamedownloadURL = html_text[html_text_dlLink:html_text.find("\"", html_text_dlLink)]

		return gamedownloadURL


if __name__ == "__main__":
	try:
		print(CoolROM().run(sys.argv))
	except:
		print("ERROR")
