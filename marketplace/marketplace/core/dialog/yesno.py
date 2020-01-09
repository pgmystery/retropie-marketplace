# -*- coding: utf-8 -*-
from Dialog import Dialog


class YesNoDialog(Dialog):
	def __init__(self, title, msg, finish_callback=None):
		super(YesNoDialog, self).__init__()
		self.answer = None
		self.dialog = self._create_dialog("yesno", title, msg, "true")
		self.dialog.wait()
		self.out, self.err = self.dialog.communicate()
		if self.out:
			if self.out.find("0") > -1:
				self.answer = True
			else:
				self.answer = False
			if finish_callback:
				finish_callback()
