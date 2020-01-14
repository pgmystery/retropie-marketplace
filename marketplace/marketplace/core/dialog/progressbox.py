# -*- coding: utf-8 -*-
from Dialog import Dialog


class ProgressBox(Dialog):
	def __init__(self, title, msg):
		super(ProgressBox, self).__init__()
		self.dialog = super(ProgressBox, self)._create_dialog("progressbox", title, msg)
		# self.dialog.wait()

	def write(self, text):
		self.dialog.stdin.write(text)

	def close(self):
		if self.dialog:
			self.stdout, self.stderr = self.dialog.communicate()
		return True
