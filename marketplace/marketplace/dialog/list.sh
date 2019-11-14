#!/bin/bash

LIST_CHOICE=$(dialog --clear \
	                	  --backtitle "$1" \
		                  --title "$1" \
		                  --menu "$2" \
		                  22 76 22 \
		                  "${LIST[@]}" \
		                  2>&1 >/dev/tty)

clear
