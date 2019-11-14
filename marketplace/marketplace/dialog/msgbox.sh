#!/bin/sh

dialog --title "$1" \
        --msgbox "$2" 22 76 \
        2>&1 >/dev/tty

MSGBOX=$?

if [ "$3" = "true" ]; then
	echo "$MSGBOX"
fi
