# -*- coding: utf-8 -*-
from Dialog import Dialog


class GaugeDialog(Dialog):
	def __init__(self, title, msg, start_value=0, max_value=100, finish_callback=None):
		super(GaugeDialog, self).__init__()
		self.stdout = None
		self.stderr = None
		self.start_value = start_value
		self.current_value = start_value
		self.max_value = max_value
		self.finish_callback = finish_callback
		self.dialog = self._create_dialog("gauge", title, msg)
		self.dialog.stdin.write("%s\n" % self.start_value)

	def set_max(self, value):
		self.max_value = value

	def set_progress(self, value):
		progress = int((float(value) / float(self.max_value)) * 100.0)
		if self.current_value != progress:
			self.dialog.stdin.write(str(progress) + "\n")
			self.current_value = progress
			if self.current_value >= self.max_value:
				self.finish_callback()

	def progress(self):
		self.set_progress(1)

	def close(self):
		if self.dialog:
			self.stdout, self.stderr = self.dialog.communicate()
		return True
