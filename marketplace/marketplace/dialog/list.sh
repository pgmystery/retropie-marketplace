#!/bin/bash

if [ -z $3 ]; then
  LIST_CHOICE=$(dialog --clear \
                        --backtitle "$1" \
                        --title "$1" \
                        --menu "$2" \
                        22 76 22 \
                        "${LIST[@]}" \
                        2>&1 >/dev/tty)
else
  LIST_CHOICE=$(dialog --clear \
                        --extra-button \
                        --extra-label "$3" \
                        --backtitle "$1" \
                        --title "$1" \
                        --menu "$2" \
                        22 76 22 \
                        "${LIST[@]}" \
                        2>&1 >/dev/tty)
fi

LIST_CHOICE_BUTTON=$?

clear
