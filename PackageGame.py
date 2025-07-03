#!/usr/bin/env python3
from pathlib import Path
from typing import (Iterable, Never)
import argparse
import os
import re
import subprocess
import sys
import platform

detected_platform = platform.system().upper()
cwd = Path.cwd()
is_win = is_osx = is_linux = False
is_win = "WINDOWS" in detected_platform
is_osx = "DARWIN" in detected_platform
MIN_UE_VERSION = 4.0
MAX_UE_VERSION = 6.0

if is_osx:
    DEFAULT_EPIC_PATH_STR = "/Users/Shared/Epic Games"
else:
    DEFAULT_EPIC_PATH_STR = "C:\\Program Files\\Epic Games"
parser = argparse.ArgumentParser()
parser.add_argument('-e',
                    '--epic-path',
                    default=DEFAULT_EPIC_PATH_STR)
parser.add_argument('-V',
                    '--ue-version')
parser.add_argument('uproject_path')
parser.add_argument('levels_path')
args = parser.parse_args()

#iterate through levels
def get_level_names(levels_path: Path) -> Iterable:
    filtered_list = [f.stem for f in levels_path.iterdir() \
        if not f.name.lower().endswith("uasset") \
        and not f.is_dir()]
    return filtered_list

def run_build_for_levels(bin_path: Path, project_path: Path, level_names: list) -> Never:
    for level_name in level_names:
        print(f"Rebuilding {level_name} map")
        level_path = f"{project_path}{level_name}"
        subprocess.run([
            f"{project_path}{level_name}",
            f"-AutomatedMapBuild CLDesc=\"Rebuilding {level_name} map\" UseSCC=true",
            ],
            -1,
            bin_path
        )

def package_game(build_tool: Path, project_path: Path) -> Never:
    project = {
        "name": project_path.resolve().stem,
        "parent": project_path.resolve().parents[0]
    }
    packaged_game_dir = project["parent"].joinpath("PackagedGame")
    if not packaged_game_dir.exists():
        packaged_game_dir.mkdir()
    
    print(f"Packaging {project['name']}")
    print(f"{project_path}/{project['name']}.uproject")
    subprocess.run([build_tool,
                    "BuildCookRun",
                    f"-project={project_path}",
#                    "-compile",
                    "-targetplatform=Win64",
                    "-clientconfig=Shipping",
                    "-stage",
                    "-pak",
                    "-build=True",
                    "-cook",
                    "-nodebuginfo",
                    "-package",
                    "-distribution",
                    f"-stagingdirectory={packaged_game_dir}"],
                    cwd=build_tool.joinpath('../../').resolve())

def main() -> Never:
    automation_tool = ""
    automation_tool_ext = ".bat" if is_win else ".sh"
    editor_names = {
        "UE4": "UE4Editor",
        "UE5": "UnrealEditor",
    }

    if len(sys.argv) < 3:
        print('help: python PackageGame.py [-e UE/] UE/Project/Path Path/To/Maps\n')
        print(r'Ex: python PackageGame.py [-e UE/] "D:\path\to\uproject.uproject" "D:\path\to\maps"')
        exit()

    ver_pattern = re.compile("\d.\d{1,2}")
    ue_version = ""
    if args.ue_version and ver_pattern.search(args.ue_version) is not None:
        ue_version = args.ue_version
    else:
        print("Which version of Unreal Engine does this project use?")
        print("ex. 5.0")
        ue_version = input("> ").strip()
        if "." not in ue_version:
            ue_version += ".0"

    if float(ue_version) < MIN_UE_VERSION and float(ue_version) >= MAX_UE_VERSION:
        print("\nThis program only works with UE4 or UE5\n Now Exiting!")
        exit()

    editor = editor_names[f"UE{ue_version.split('.')[0]}"]

    ue_path = Path(args.epic_path).joinpath(f"UE_{ue_version}/Engine").resolve()
    bin_path = ""
    try:
        if is_osx:
            bin_path = list(ue_path.joinpath("Binaries/Mac/").glob(f"{editor}"))[0]
        else:
            bin_path = list(ue_path.joinpath("Binaries/Win64/").glob(f"{editor}.exe"))[0]
        bin_path = bin_path.resolve()
    except IndexError:
        print("Could not find Unreal Editor executable.")
        exit()
    print(f"Unreal Engine {ue_version} editor found.")
    automation_tool = ue_path.joinpath(f"Build/BatchFiles/RunUAT{automation_tool_ext}")

    ue_project_path = Path(args.uproject_path).resolve()
    levels_path = Path(args.levels_path).resolve()
    level_names = get_level_names(levels_path)

    run_build_for_levels(bin_path, ue_project_path, level_names)
    package_game(automation_tool, ue_project_path)

if __name__ == "__main__":
    main()
