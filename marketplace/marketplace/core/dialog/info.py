# -*- coding: utf-8 -*-
from Dialog import Dialog


class InfoDialog(Dialog):
	def __init__(self, title, msg):
		super(InfoDialog, self).__init__()
		self.dialog = super(InfoDialog, self)._create_dialog("info", title, msg)
