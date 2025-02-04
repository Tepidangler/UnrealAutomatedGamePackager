@echo off
:: #This is a batch file to build and package the Game, simply run this and all important information should be output to the terminal
:: # Authored By: De'Lano Wilcox
:: # Notes: If you're reading this; If there are any errors that stop the game from packaging copy the output in the terminal and send it to me


echo If there are any errors that stop the game from packaging then let me (Delano Wilcox) by making an issue in the github repo.
echo If Exit Status, or the last line of the output is not Success then that's when you should let me know.
echo 

if %1.==. goto Help 

python --version 3 >NUL
if errorlevel 1 goto NoPython

python PackageGame.py %cd%\\%1.uproject %cd%\\Content\\%1\\Maps\\Levels

:NoPython
echo Python Not Installed

:Help
echo Usage:
echo "BuildPackagedGame-Windows.bat <project-name>"
goto :EOF

