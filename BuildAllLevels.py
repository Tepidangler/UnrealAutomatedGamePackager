import os
import subprocess
import sys

#iterate through levels
def iterateLevels(LevelPath):
    lvldct = []

    for r, d, f in os.walk(LevelPath):
        for file in range (len(f)):
            if not f[file].lower().endswith((".uasset")):
                   lvldct.append(f[file].rsplit(".", 1)[0])
    return lvldct


#main
def main():

    result = []

    if len(sys.argv) != 3:
        print('help: python BuildAllLevels.py  UE/Project/Path Path/To/Maps\n')
        print(r'Ex: python BuildAllLevels.py "D:\path\to\uproject.uproject" "D:\path\to\maps"')
        exit()

    UEVersion = input("Are you using UE 4 or UE 5?: ")

    if  UEVersion == "UE4" or UEVersion == "4":
        print("Searching For UE4 Executable")
        for r,d,f in os.walk("C:\\"):
            if "UE4Editor.exe" in f:
             print("UE4 Result Found")
             result.append(os.path.join(r, "UE4Editor.exe"))
             UEPath = result[0]
             break
    elif  UEVersion == "UE5" or UEVersion == "5":
        print("Searching For UE5 Executable")
        for r,d,f in os.walk("C:\\"):
            if "UnrealEditor.exe" in f:
             print("UE5 Result Found")
             result.append(os.path.join(r, "UE4Editor.exe"))
             UEPath = result[0]
             break
    else:
        print("\nThis program only works with UE4 or UE5\n Now Exiting!")
        exit()

    UEProjectPath = '"' + sys.argv[1] + '"'
    LevelsPath = sys.argv[2]
    LevelNames = iterateLevels(LevelsPath)
    SpaceKey = " "
    
    #run UE Command to Build Lighting
    for f in range(0, len(LevelNames)):
        print('Rebuilding '+LevelNames[f]+' map')
        subprocess.run(UEPath+SpaceKey+UEProjectPath+SpaceKey+LevelNames[f]+SpaceKey+'-AutomatedMapBuild CLDesc="Rebuilding '+LevelNames[f]+' map" UseSCC=true')




#run main

main()