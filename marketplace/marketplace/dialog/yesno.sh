#!/bin/sh

dialog --title "$1" \
        --yesno "$2" 22 76 \
        2>&1 >/dev/tty

YESNO=$?

if [ "$3" = "true" ]; then
	echo "$YESNO"
fi
