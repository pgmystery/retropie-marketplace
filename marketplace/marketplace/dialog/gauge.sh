#!/bin/bash

TITLE="$1"
DESCRIPTION="$2"
PCT=0

dialog --title "$TITLE" --gauge "$DESCRIPTION" 22 76 < <(
	while read line
	do
	PCT="$line"
cat <<EOF
XXX
$PCT
$DESCRIPTION
XXX
EOF
	done
)
