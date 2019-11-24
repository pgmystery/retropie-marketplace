# -*- coding: utf-8 -*-
import os
from subprocess import Popen, PIPE
import pyecm2cue


def load_extension(allowed_extensions):
	allowed_extensions.append(".bin")
	allowed_extensions.append(".BIN")
	allowed_extensions.append(".ecm")
	allowed_extensions.append(".ECM")
	return allowed_extensions

def after_install(data):
	extract_files = data["extract_files"]
	rom_path = data["rom_path"]
	game_to_install = data["game_to_install"]
	path = data["path"]

	psx_bin_file = None
	psx_bin_ecm_file = None
	for file in extract_files:
		file = os.path.basename(os.path.normpath(file))
		if file.lower().endswith(".bin"):
			psx_bin_file = file
			break
		if file.lower().endswith(".bin.ecm"):
			psx_bin_ecm_file = file
			break
	if psx_bin_file:
		if not os.path.isfile(rom_path + psx_bin_file[:len(psx_bin_file) - len(".bin")] + ".cue") and not os.path.isfile(rom_path + psx_bin_file[:len(psx_bin_file) - len(".bin")] + ".CUE"):
			yesno = Popen(["/" + path + "../dialog/yesno.sh", "Rename \".bin\"-file", "On the game: \"" + game_to_install + "\"\nThe downloaded ROM file has a \".bin\"-file without an \".cue\"-file. RetroPie don't support this! Do you want to rename the \".bin\"-file to \".iso\" and try that this will work?\nOn no, the \".bin\"-file will be deleted!", "true"], stdout=PIPE)
			yesno.wait()
			out, err = yesno.communicate()
			if out:
				if out.find("0") > -1:
					os.rename(rom_path + "/" + psx_bin_file, rom_path + "/" + psx_bin_file[:len(psx_bin_file) - len(".bin")] + ".iso")
				else:
					os.remove(rom_path + "/" + psx_bin_file)
			else:
				os.remove(rom_path + "/" + psx_bin_file)
			infoscreen = Popen(["/" + path + "../dialog/info.sh", "Install Game...", "Installing Game \"" + game_to_install + "\"\nPlease wait..."])
	if psx_bin_ecm_file:
		infoscreen = Popen(["/" + path + "../dialog/info.sh", "Convert File format", "Convert .BIN.ECM to .BIN file\nPlease Wait..."], stdin=PIPE)
		pyecm2cue.process(rom_path + "/" + psx_bin_ecm_file)
		os.remove(rom_path + "/" + psx_bin_ecm_file)
		psx_bin_cue_file = rom_path + "/" + psx_bin_ecm_file[:len(psx_bin_ecm_file) - len(".ecm")] + ".cue"
		if os.path.isfile(psx_bin_cue_file):
			os.remove(psx_bin_cue_file)
