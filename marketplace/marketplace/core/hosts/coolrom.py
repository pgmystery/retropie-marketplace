import sys
from lxml import etree
from Host import Host


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
		gamelist_object = html.xpath("./body/center/table/tr/td/table/tr[4]/td/table/tr/td/font/font")[0]
		for e in gamelist_object:
			if e.tag != "br":
				gamelist_object.remove(e)
		for e in gamelist_object.xpath("//br"):
			e.tail = "\n" + e.tail if e.tail else "\n"
		etree.strip_elements(gamelist_object,'br',with_tail=False)
		gamelist_object = etree.tostring(gamelist_object, method="text", encoding="UTF-8")
		for line in gamelist_object.splitlines():
			if not line.isspace() and len(line) > 0:
				self.add_game(line)
		return self.get_gameslist()

	def get_game_download_link(self, *args):
		game_to_install = self.validate_game_to_install(args[0][2])
		# get URL:
		firstChar = game_to_install[:1]
		if firstChar.isalpha():
			url = "http://coolrom.com/roms/psx/%s/" % firstChar.lower()
		else:
			url = "http://coolrom.com/roms/psx/0/"
		html = self.get_html(url)
		gamelist_object = html.xpath("./body/center/table/tr/td/table/tr[4]/td/table/tr/td/font/font")[0]
		gamelink = None
		for div in gamelist_object.xpath("//div"):
			if len(div.xpath("./a")) > 0:
				gamelink = div.xpath("./a")[0]
				game = etree.tostring(gamelink, method="text", encoding="UTF-8")
				if game == game_to_install:
					break

		if gamelink is None:
			return "ERROR"

		gameURL = gamelink.attrib['href']

		if not gameURL:
			return "ERROR"

		html = self.get_html("http://coolrom.com" + gameURL)
		gamedownload_object = html.xpath("./body/center/table/tr/td/table/tr[4]/td/table/tr/td/center/a")[0]
		gamedownloadURL = gamedownload_object.attrib['href']
		gamedownloadURL = gamedownloadURL[gamedownloadURL.find("/dlpop.php?"):]
		gamedownloadURL = gamedownloadURL[:gamedownloadURL.find("'")]

		html = self.get_html("http://coolrom.com/" + gamedownloadURL)
		html_text = etree.tostring(html, method="html", pretty_print=True)

		html_text_dlLink = html_text.find("http://dl.coolrom.com")
		gamedownloadURL = html_text[html_text_dlLink:html_text.find("\"", html_text_dlLink)]

		return gamedownloadURL


if __name__ == "__main__":
	try:
		print(CoolROM().run(sys.argv))
	except:
		print("ERROR")
