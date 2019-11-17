# -*- coding: utf-8 -*-
import urllib2
from lxml import etree
import json


class Host(object):
	def __init__(self, emulators=None, emulators_link=None):
		if emulators is None:
			emulators = {}
		if emulators_link is None:
			emulators_link = {}
		self.emulators = emulators
		self.emulators_link = emulators_link
		self.gamelist = []

	def run(self, sys_argv, host):
		run = sys_argv[1]
		if run == "get_games":
			return host.get_games(sys_argv[1:len(sys_argv)])
		elif run == "get_game_download_link":
			return host.get_game_download_link(sys_argv[1:len(sys_argv)])
		else:
			return "ERROR"

	def add_game(self, game):
		self.gamelist.append(game)

	def get_gameslist(self):
		return "\n".join(self.gamelist)

	def validate_game_to_install(self, game_to_install):
		# Delete illegal chars:
		illegal_chars = [
			"\\",
		]
		for char in illegal_chars:
			game_to_install = game_to_install.replace(char, "")
		return game_to_install

	def get_emulator(self, emulator):
		if emulator not in self.emulators.keys():
			return "ERROR"
		emulator = self.emulators[emulator]
		return emulator

	def get_emulator_link(self, emulator):
		if emulator not in self.emulators_link:
			return "ERROR"
		emulator_link = self.emulators_link[emulator]
		return emulator_link

	def get_html(self, url):
		return etree.HTML(self.request(url).read())

	def get_json(self, url):
		return json.load(self.request(url))

	def request(self, url):
		header = {
			'User-Agent': '',
		}
		req = urllib2.Request(url, headers=header)
		return urllib2.urlopen(req)
