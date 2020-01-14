#!/bin/bash

TITLE="$1"
DESCRIPTION="$2"
WIDTH=22
HEIGHT=76

dialog --title "$TITLE" --progressbox "$DESCRIPTION" $WIDTH $HEIGHT
