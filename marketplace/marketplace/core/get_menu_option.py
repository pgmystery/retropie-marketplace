import sys
import ntpath


try:
	option = ntpath.basename(sys.argv[1]).replace(".rp", "")
	print(option)
except IndexError:
	print("ERROR")
