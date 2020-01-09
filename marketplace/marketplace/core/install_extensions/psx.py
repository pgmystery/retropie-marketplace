# -*- coding: utf-8 -*-
import os
import unecm

from dialog.info import InfoDialog
from dialog.yesno import YesNoDialog
from dialog.gauge import GaugeDialog


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

	psx_bin_file = None
	psx_no_cue_file = True
	psx_ecm_file = None
	for file in extract_files:
		if file.lower().endswith(".bin"):
			psx_bin_file = file
		elif file.lower().endswith(".cue"):
			psx_no_cue_file = False
		elif file.lower().endswith(".ecm"):
			psx_ecm_file = file
	if psx_bin_file:
		if psx_no_cue_file:
			yesno_dialog = YesNoDialog("Rename \".bin\"-file", "On the game: \"" + game_to_install + "\"\nThe downloaded ROM file has a \".bin\"-file without an \".cue\"-file. RetroPie don't support this! Do you want to rename the \".bin\"-file to \".iso\" and try that this will work?\nOn no, the \".bin\"-file will be deleted!")
			if yesno_dialog.answer:
				os.rename(rom_path + "/" + psx_bin_file, rom_path + "/" + psx_bin_file[:len(psx_bin_file) - len(".bin")] + ".iso")
			else:
				os.remove(rom_path + "/" + psx_bin_file)
			InfoDialog("Install Game...", "Installing Game \"" + game_to_install + "\"\nPlease wait...")
	if psx_ecm_file:
		convert_dialog = GaugeDialog("Convert File format", "Uncompress ECM file\nPlease Wait...", max_value=100)
		unecm.process(rom_path + "/" + psx_ecm_file, update_callback=convert_dialog.set_progress)
		convert_dialog.close()
		os.remove(rom_path + "/" + psx_ecm_file)
