# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE

from get_path import get_path


class Dialog(object):
	def __init__(self):
		self.path = get_path()

	def _create_dialog(self, dialog_type, title, msg, *args):
		self.dialog_type = dialog_type
		self.title = title
		self.msg = msg
		cmd = ["/%s../dialog/%s.sh" % (self.path, dialog_type), title, msg]
		cmd.extend(args)
		return Popen(cmd, stdin=PIPE)
