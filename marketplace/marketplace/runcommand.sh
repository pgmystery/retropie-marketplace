#!/bin/bash

BASEDIR=$(dirname "$0")

MENU_OPTION="$1"

# main retropie install location
rootdir="/opt/retropie"

# if __user is set, try and install for that user, else use SUDO_USER
if [[ -n "$__user" ]]; then
    user="$__user"
    if ! id -u "$__user" &>/dev/null; then
        echo "User $__user not exist"
        exit 1
    fi
else
    user="$SUDO_USER"
    [[ -z "$user" ]] && user="$(id -un)"
fi

home="$(eval echo ~$user)"
datadir="$home/RetroPie"
# biosdir="$datadir/BIOS"
romdir="$datadir/roms"

marketplacedir="$datadir/marketplace"

python_venv="$BASEDIR/core/venv/bin/python"

STORE=`$python_venv "$BASEDIR/core/get_menu_option.py" "$MENU_OPTION"`


# Start joy2key
source $BASEDIR/core/joy2key/joy2key.sh
start_joy2key


# SEARCH FOR UPDATE
if [[ "$STORE" == *"search for updates"* ]]; then
	source $BASEDIR/dialog/info.sh "Searching for Updates" "Searching for Updates!\nPlease wait..."
	$python_venv $BASEDIR/core/updater.py
	if [[ -f "/tmp/retropie-marketplace-master/marketplace/setup.py" ]]; then
		source $BASEDIR/dialog/info.sh "Updating Marketplace" "Updating Marketplace!\nAfter updating, the emulationstation will be restarted!\nPlease wait..."
		$python_venv "/tmp/retropie-marketplace-master/marketplace/setup.py"
		touch /tmp/es-restart
		pkill -f -e "/opt/retropie/supplementary/.*/emulationstation$"
	fi
	clear
	exit
fi


# INFO
if [ "$STORE" == "info" ]; then
	VERSION=`$python_venv $BASEDIR/core/get_version.py`
	source $BASEDIR/dialog/msgbox.sh "About Emulationstation-Marketplace", "Emulationstation-Marketplace version: v$VERSION\nCreated by Philipp Glaw"
	clear
	exit
fi


# EMULATORS-SELECTION:
if [ "$STORE" == "marketplace" ]; then
	source $BASEDIR/dialog/info.sh "Creating emulator-list", "Create a list with all available emulators which are supported!\nPlease wait..."
	STORES=`$python_venv $BASEDIR/core/get_stores.py "stores" "$BASEDIR/core/hosts/"`
fi

LIST=()

while read -r line; do
    LIST+=("$line" "")
done <<< "$STORES"

if [ "$STORES" != "ERROR" ] && [ "$STORES" != "false" ]; then
	source $BASEDIR/dialog/list.sh "List of available systems" "Choose a system where you want to install a game!"
fi

if [ -z "$LIST_CHOICE" ]
then
	clear
	exit
else
	SYSTEM="$LIST_CHOICE"
	EM_SYSTEM=`$python_venv $BASEDIR/core/get_stores.py "system_name" "$LIST_CHOICE"`
fi



# HOSTLIST:
source $BASEDIR/dialog/info.sh "Creating hosts-list", "Create a list with all available hosts!\nPlease wait..."

HOSTLIST=`$python_venv $BASEDIR/core/get_hosts.py "$BASEDIR/core/hosts/" "$EM_SYSTEM"`

LIST=()

while read -r line; do
    LIST+=("$line" "")
done <<< "$HOSTLIST"

if [ "$HOSTLIST" != "ERROR" ] && [ "$HOSTLIST" != "false" ]; then
	source $BASEDIR/dialog/list.sh "List of Host" "Choose a host where you download the ROM-file!"
fi

if [ -z "$LIST_CHOICE" ]
then
	clear
	exit
fi


# GET_INSTALLED_GAMES:
# INSTALLED_GAMES=`$python_venv $BASEDIR/core/get_installed_games.py "$romdir" "$EM_SYSTEM"`  # TODO!!!


# LIST GAMES:
source $BASEDIR/dialog/info.sh "Receiving gameslist" "Receiving gameslist!\nPlease wait..."

GAMESLIST=`$python_venv $BASEDIR/core/hosts/$LIST_CHOICE.py "get_games" "$EM_SYSTEM"`

if [ "$GAMESLIST" == "ERROR" ] || [ "$GAMESLIST" == "false" ]; then
	source $BASEDIR/dialog/msgbox.sh "ERROR", "Sorry, but there was an ERROR!\nMaybe it works if you try again..."
	clear
	exit
fi


# TODO: CHECK INSTALLED GAMES IN THE LIST AND IF THERE UNSET -> UNINSTALL THEM!


GAMES=()

if (( $(grep -c . <<<"$GAMESLIST") == 0 )); then
	source $BASEDIR/dialog/msgbox.sh "ERROR", "No Games found!\nMaybe an error with the host or with your internet connection"
	clear
	exit
fi

while read -r line; do
    GAMES+=("$line" "" off)
done <<< "$GAMESLIST"

source $BASEDIR/dialog/checklist.sh "$SYSTEM" "$SYSTEM" "Choose the games that you want to install or uninstall:"

if [ -z "$CHOICE" ]
then
	clear
	exit
fi

source $BASEDIR/dialog/info.sh "Collection Data..." "Collection selected Games\nPlease wait..."

GAMECHOICES=$(eval 'for word in '$CHOICE'; do echo $word; done')

while read -r line; do
	source $BASEDIR/dialog/info.sh "Getting Downloadfile..." "Getting DownloadFile for:\n\"$line\"\nPlease wait..."
	GAMELINK=`$python_venv $BASEDIR/core/hosts/$LIST_CHOICE.py "get_game_download_link" "$EM_SYSTEM" "$line"`
	$python_venv $BASEDIR/core/install_game.py "$EM_SYSTEM" "$line" "$GAMELINK"
done <<< "$GAMECHOICES"


source $BASEDIR/dialog/yesno.sh "Restart Emulationstation" "To see the new installed games, you need to restart emulationstation!\nDo you want to restart emulationstation now?"

if [[ "$YESNO" == *"0"* ]]; then
	touch /tmp/es-restart
	pkill -f -e "/opt/retropie/supplementary/.*/emulationstation$"
fi

clear
