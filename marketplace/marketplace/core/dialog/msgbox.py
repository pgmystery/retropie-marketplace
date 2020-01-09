# -*- coding: utf-8 -*-
from Dialog import Dialog


class MSGBoxDialog(Dialog):
	def __init__(self, title, msg, finish_callback=None):
		super(MSGBoxDialog, self).__init__()
		self.dialog = self._create_dialog("msgbox", title, msg)
		self.dialog.wait()
		if finish_callback:
			finish_callback()
