# -*- coding: utf-8 -*-
import platform


def get_os_architecture():
	bit_version = platform.architecture()[0]
	if bit_version == "32bit":
		return "32bit"
	elif bit_version == "64bit":
		return "64bit"
	else:
		return None
