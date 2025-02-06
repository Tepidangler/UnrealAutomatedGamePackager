# AutomatedMapBuild
Python Script to Automatically build your levels in Unreal Editor via the commandline 

help: python PackageGame.py  UE/Project/Path Path/To/Maps

Ex: python PackageGame.py "D:\path\to\uproject.uproject" "D:\path\to\maps"

# Known Issues:

Currently if packaging on MacOS and targeting for Windows it will fail (for a myriad of reasons). So Until a time comes where UE is made more robust to allow for things like that, or I figure out a way to make that possible you'll either just have to build on Windows, or go into the PackageGame.py file and change the ```-Platform=Win64``` argument in ```PackageGame()``` to ```-Platform=Mac``` (I'm Making an assumption here on the platform name)
