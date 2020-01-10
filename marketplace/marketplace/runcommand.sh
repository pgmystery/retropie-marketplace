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


search_for_update() {
	source $BASEDIR/dialog/info.sh "Searching for Updates" "Searching for Updates!\nPlease wait..."
	$python_venv $BASEDIR/core/updater.py
	if [[ -f "/tmp/retropie-marketplace-master/marketplace/setup.py" ]]; then
		source $BASEDIR/dialog/info.sh "Updating Marketplace" "Updating Marketplace!\nAfter updating, the emulationstation will be restarted!\nPlease wait..."
		$python_venv "/tmp/retropie-marketplace-master/marketplace/setup.py"
		touch /tmp/es-restart
		pkill -f -e "/opt/retropie/supplementary/.*/emulationstation$"
	fi
}


info() {
	VERSION=`$python_venv $BASEDIR/core/get_version.py`
	source $BASEDIR/dialog/msgbox.sh "About RetroPie-Marketplace" "RetroPie-Marketplace version: v$VERSION\nCreated by Philipp Glaw\nGithub: https://github.com/pgmystery/retropie-marketplace"
}


marketplace() {
	source $BASEDIR/dialog/info.sh "Creating emulator-list" "Create a list with all available emulators which are supported!\nPlease wait..."
	STORES=`$python_venv $BASEDIR/core/get_stores.py "stores" "$BASEDIR/core/hosts/"`

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

  marketplace_hostlist
}

marketplace_hostlist() {
  # HOSTLIST:
  source $BASEDIR/dialog/info.sh "Creating hosts-list" "Create a list with all available hosts!\nPlease wait..."

  HOSTLIST=`$python_venv $BASEDIR/core/get_hosts.py "$BASEDIR/core/hosts/" "$EM_SYSTEM"`

  LIST=()

  while read -r line; do
      LIST+=("$line" "")
  done <<< "$HOSTLIST"

  if [ "$HOSTLIST" != "ERROR" ] && [ "$HOSTLIST" != "false" ]; then
    source $BASEDIR/dialog/list.sh "List of hosts" "Choose a host where you download the ROM-file!" "Go Back"
  fi

  if [ $LIST_CHOICE_BUTTON -eq 0 ]; then  # Continue
    if [ -z "$LIST_CHOICE" ]; then
      clear
      exit
    else
      marketplace_get_gameslist
    fi
  elif [ $LIST_CHOICE_BUTTON -eq 1 ]; then  # Cancel
    clear
    exit
  elif [ $LIST_CHOICE_BUTTON -eq 3 ]; then  # Go Back
    clear
    marketplace
  fi
}

marketplace_get_gameslist() {
  # LIST GAMES:
  source $BASEDIR/dialog/info.sh "Receiving gameslist" "Receiving gameslist!\nPlease wait..."

  GAMESLIST=`$python_venv $BASEDIR/core/hosts/$LIST_CHOICE.py "get_games" "$EM_SYSTEM"`

  if [ "$GAMESLIST" == "ERROR" ] || [ "$GAMESLIST" == "false" ]; then
    source $BASEDIR/dialog/msgbox.sh "ERROR" "Sorry, but there was an ERROR!\nMaybe it works if you try again..."
    clear
    marketplace_hostlist
  fi

  GAMES=()

  if (( $(grep -c . <<<"$GAMESLIST") == 0 )); then
    source $BASEDIR/dialog/msgbox.sh "ERROR" "No games found!\nMaybe an error with the host or with your internet connection"
    clear
    marketplace_hostlist
  fi

  while read -r line; do
      GAMES+=("$line" "" off)
  done <<< "$GAMESLIST"

  marketplace_show_gameslist
}

marketplace_show_gameslist() {
  source $BASEDIR/dialog/checklist.sh "$SYSTEM" "$SYSTEM" "Choose the games that you want to install or uninstall:" "Go Back"

  if [ $CHOICE_BUTTON -eq 0 ]; then
    if [ -z "$CHOICE" ]; then  # Continue with NO games selected
      source $BASEDIR/dialog/msgbox.sh "No games selected" "No games selected!\nSelect the games you want to install"
      clear
      marketplace_show_gameslist
     else  # Continue with games selected
       clear
       marketplace_download_game
    fi
  elif [ $CHOICE_BUTTON -eq 1 ]; then  # Cancel
    clear
    exit
  elif [ $CHOICE_BUTTON -eq 3 ]; then  # Go Back
    clear
    marketplace_hostlist
  fi
}

marketplace_download_game(){
  source $BASEDIR/dialog/info.sh "Collect Data..." "Collect selected games\nPlease wait..."

  GAMECHOICES=$(eval 'for word in '$CHOICE'; do echo $word; done')

  while read -r line; do
    source $BASEDIR/dialog/info.sh "Getting Downloadfile..." "Getting DownloadFile for:\n\"$line\"\nPlease wait..."
    GAMELINK=`$python_venv $BASEDIR/core/hosts/$LIST_CHOICE.py "get_game_download_link" "$EM_SYSTEM" "$line"`
    if [ "$GAMELINK" == "ERROR" ]; then
      source $BASEDIR/dialog/msgbox.sh "Couldn't download the game" "ERROR on downloading the game :(\nTry to download this game from another host or try it again."
      clear
      marketplace_hostlist
    else
      $python_venv $BASEDIR/core/install_game.py "$EM_SYSTEM" "$line" "$GAMELINK"
    fi
  done <<< "$GAMECHOICES"


  source $BASEDIR/dialog/yesno.sh "Restart Emulationstation" "To see the new installed games, you need to restart emulationstation!\nDo you want to restart emulationstation now?"

  if [[ "$YESNO" == *"0"* ]]; then
    marketplace_restart_emulationstation
  fi
}

marketplace_restart_emulationstation() {
    touch /tmp/es-restart
    pkill -f -e "/opt/retropie/supplementary/.*/emulationstation$"
}


# SEARCH FOR UPDATE
if [[ "$STORE" == *"search for updates"* ]]; then
  search_for_update

# INFO
elif [ "$STORE" == "info" ]; then
  info

# EMULATORS-SELECTION:
elif [ "$STORE" == "marketplace" ]; then
  marketplace
fi

clear
