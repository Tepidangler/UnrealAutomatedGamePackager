#!/bin/sh
#This is a batch file to build and package the Game, simply run this and all important information should be output to the terminal
# Authored By: De'Lano Wilcox
# Notes: If you're reading this; If there are any errors that stop the game from packaging copy the output in the terminal and send it to me

PWD="$(pwd)"

if [[ ($# -ne 1) ]]; then
	echo "Help:"
	echo "./BuildPackagedGame-MacOS.sh <project-name>"
else

	if command -v python3 >/dev/null 2>&1; then
		./PackageGame.py "$PWD/$1.uproject" "$PWD/Content/$1/Maps/Levels/"

	else
		echo "Python not installed on this machine. Please visit https://www.python.org/downloads/macos/ and download the latests Stable Release!"
	fi
fi
