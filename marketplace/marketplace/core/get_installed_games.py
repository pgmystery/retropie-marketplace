import sys
import ntpath


try:
	main_rom_path = sys.argv[1]
	store = ntpath.basename(sys.argv[2]).replace(".rp", "")
except IndexError:
	print("ERROR")

rom_path = main_rom_path + "/" + store + "/"
