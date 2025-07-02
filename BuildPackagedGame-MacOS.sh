#!/bin/sh
#This is a batch file to build and package the Game, simply run this and all important information should be output to the terminal
# Authored By: De'Lano Wilcox
# Notes: If you're reading this; If there are any errors that stop the game from packaging copy the output in the terminal and send it to me

PWD="$(pwd)"
UNREAL_PATH="$1"
UE_VERSION="$2"
OPTS=""

if [[ ($# -ne 1) ]]; then
	echo "Help:"
	echo "./BuildPackagedGame-MacOS.sh <path-to-project-name> [<unreal-engine-version>]"
else
	if [ ! "$UE_VERSION"]; then
		OPTS="-V $UE_VERSION"
	fi

	if command -v python3 >/dev/null 2>&1; then
		./PackageGame.py $OPTS -e $UNREAL_PATH "$PWD/TinyTitan.uproject" "$PWD/Content/TinyTitan/Maps/Levels/"

	else
		echo "Python not installed on this machine. Please visit https://www.python.org/downloads/macos/ and download the latests Stable Release!"
	fi
fi
