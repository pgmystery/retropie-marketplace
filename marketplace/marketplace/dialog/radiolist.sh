#!/bin/bash

RADIOLIST_CHOICE=$(dialog --clear \
	                	  --backtitle "$1" \
		                  --title "$1" \
		                  --radiolist "$2" \
		                  22 76 22 \
		                  "${RADIOLIST[@]}" \
		                  2>&1 >/dev/tty)

clear
