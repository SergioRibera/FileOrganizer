#!/bin/python3
# Author: Sergio Ribera
import argparse, os, shutil, sys, os.path, json

def saveConfig():
    global folders_by_extension
    folders_by_extension = {
        "exe": "Software",
        "txt": "Texts",
        "pdf": "PDF Documents",
        "epub": "Books",
        "jpg": "Images",
        "jpeg": "Images",
        "png": "Images",
        "raw": "Images",
        "mp3": "Music",
        "ogg": "Audio",
        "mp4": "Videos",
        "mkv": "Videos",
        "avi": "Videos",
        "xlsx": "Excel Files",
        "ppt": "Slides",
        "doc": "Documents",
        "rar": "Compressed Files",
        "zip": "Compressed Files"
    }
    with open('config.json', 'w') as outfile:
        json.dump(folders_by_extension, outfile, indent=4)

def loadConfig(confFile='config.json'):
    global folders_by_extension
    if not os.path.exists(confFile):
        saveConfig()
        return
    with open(confFile) as jsonFile:
        folders_by_extension = json.load(jsonFile)

def directory(file_extension: str) -> str:
    if not file_extension:
        return
    return folders_by_extension.get(file_extension, 'Extras')


def organize(path: str):
    if not os.path.exists(path):
        print(f"ERROR. Not found {path} or not exists.")
        return

    files = os.listdir(path)
    extensions = [os.path.splitext(file)[1].strip(".") for file in files]

    for ext in extensions:
        dir = directory(ext) or ""
        new_directory = os.path.join(path, dir)
        if dir and not os.path.exists(new_directory):
            os.makedirs(new_directory)

    for file in files:
        ext = os.path.splitext(file)[1].strip(".")
        _dir = directory(ext)
        if not _dir:
            continue

        source_filepath = os.path.join(path, file)
        print(source_filepath)
        destination_filepath = os.path.join(path, _dir, file)
        print(destination_filepath)

        if not os.path.exists(destination_filepath):
            shutil.move(source_filepath, destination_filepath)
            print(f"Was moved {file} into {_dir} directory. \n")
    print(f"All the files was organized successfully in {path}")


# 
parser = argparse.ArgumentParser(description="This script organize your files in folder")
parser.add_argument('-d', '--dir', metavar='path', help='This is the path to organize')
parser.add_argument('-c', '--config', metavar='file', help='This file contains config to reorganize your files')

args = parser.parse_args()

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        parser.print_help()
    try:
        if args.config:
            loadConfig(args.config)
        else:
            loadConfig()
        if args.dir:
            organize(args.dir)
        else:
            parser.print_help()
    except Exception as e:
        print(f"There was an error: {str(e)}")
        parser.print_help()
