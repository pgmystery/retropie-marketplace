#!/bin/bash

HEIGHT=22
WIDTH=76
CHOICE_HEIGHT=22
BACKTITLE="$1"
TITLE="$2"
MENU="$3"

CHOICE=$(dialog --clear \
                --backtitle "$BACKTITLE" \
                --title "$TITLE" \
                --checklist "$MENU" \
                $HEIGHT $WIDTH $CHOICE_HEIGHT \
                "${GAMES[@]}" \
                2>&1 >/dev/tty)

clear
