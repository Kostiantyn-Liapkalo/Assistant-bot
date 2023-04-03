import os
import re
import shutil


from typing import Tuple
from os.path import split
from pathlib import Path
from prettytable import PrettyTable
from random import randint

chat_in_progress = True

def create_folders_from_groups(path_to_folder: str, folder_names: dict) -> None:

    # This func creates folders for sorted files from folder_names keys

    for folder_for_sorted in folder_names.keys():
        os.makedirs(path_to_folder + "\\" + folder_for_sorted, exist_ok=True)


def delete_empty_folders(paths_to_folders: set[Path]) -> None:

    # This func removes empty folders

    for folder_path in paths_to_folders:
        folder_path = Path(folder_path)

        if folder_path.is_dir() and not next(folder_path.iterdir(), None):
            os.rmdir(folder_path)
            delete_empty_folders(paths_to_folders)


def generate_formats(file_names: list, formats: dict) -> tuple[set, set]:

    known_formats = set()
    unknown_formats = set()

    # Generate sets with known and unknown formats of files
    for file in file_names:
        for name_group, file_format in formats.items():
            if file.split(".")[-1].upper() in file_format:
                known_formats.add(file.split(".")[-1])
            elif file.split(".")[-1].upper() not in file_format:
                unknown_formats.add(file.split(".")[-1])
                unknown_formats = unknown_formats.difference(known_formats)
    return known_formats, unknown_formats


def normalize(item_name: str) -> str:

    # This func takes name of file, translates and returns new name

    item_name = (
        re.sub(r"\W", "_", item_name.split(".")[0]) + "." + item_name.split(".")[-1]
    )

    cyrillic = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    latin = (
        "a",
        "b",
        "v",
        "g",
        "d",
        "e",
        "e",
        "j",
        "z",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "r",
        "s",
        "t",
        "u",
        "f",
        "h",
        "ts",
        "ch",
        "sh",
        "sch",
        "",
        "y",
        "",
        "e",
        "yu",
        "ya",
        "je",
        "i",
        "ji",
        "g",
    )

    translating_map = {}

    for cyril_symbol, latin_symbol in zip(cyrillic, latin):
        translating_map[ord(cyril_symbol)] = latin_symbol
        translating_map[ord(cyril_symbol.upper())] = latin_symbol.upper()

    table = item_name.maketrans(translating_map)

    return str(item_name).translate(table)


def rename_files(file_paths: set[Path], formats: dict):
    for file_for_rename in file_paths:
        for known_formats in formats.values():
            if str(file_for_rename).split(".")[-1].upper() in known_formats:
                new_name = normalize(file_for_rename.name)
                os.rename(file_for_rename, split(file_for_rename)[0] + "\\" + new_name)


def rename_folders(folder_paths: set[Path]):
    list_of_paths = [str(folder_path_for_sort) for folder_path_for_sort in folder_paths]
    list_of_paths = reversed(
        sorted(list_of_paths, key=len)
    )  # sorted paths by len to sort in correctly turn

    for folder_for_rename in list_of_paths:
        new_name = normalize(str(Path(folder_for_rename).name))
        os.rename(
            folder_for_rename,
            str(split(folder_for_rename)[0]) + "\\" + new_name.split(".")[0],
        )


def parse_files(folder_path: str, ignore_list: list) -> Tuple[list[str], set[Path]]:

    # This func iterates through the files and returns the names and paths of all files in the given folder

    path = Path(folder_path)
    file_names = []
    set_of_paths = set()

    for item in path.rglob("*"):
        if item.is_file():
            file_names.append(item.name)
            if split(item)[0].split("\\")[-1] not in ignore_list:
                set_of_paths.add(Path(item))

    return file_names, set_of_paths


def parse_folders(folder_path: str, ignore_list) -> Tuple[list[str], set[Path]]:

    # This func iterates through the folders and returns the names and paths of all folders in the argument-folder

    path = Path(folder_path)
    names_of_folders = []
    set_of_paths = set()

    for item in path.rglob("*"):
        if not item.is_file():
            if item.name not in ignore_list:
                names_of_folders.append(item.name)
                set_of_paths.add(Path(item))

    return names_of_folders, set_of_paths


def sort_files(
    paths_to_files: set, file_groups: dict, path_folder_for_sort: str, ignore_list
) -> None:

    # This func moves all files to folders for sorted

    for path_to_file in paths_to_files:

        # get previously folder (/ARCHIVES/file.rar)
        previously_folder = split(path_to_file)[0].split("\\")[-2]

        for name_of_group, formats_list in file_groups.items():

            # check if folder in ignore list
            if (
                split(path_to_file)[-1] in formats_list
                and previously_folder not in ignore_list
            ):
                if Path(path_to_file) != Path(
                    path_folder_for_sort
                    + "\\"
                    + name_of_group
                    + "\\"
                    + split(path_to_file)[-1]
                ):
                    #  Проверка на наличие одноименного файла #
                    document_name = str(path_to_file).split('\\').pop()
                   
                    if os.path.exists(path_folder_for_sort + '\\' + name_of_group + '\\' + document_name):
                        # Создается рандомный префикс для переименования
                        prefix = ''
                        for i in range(1,4):
                            symb = chr(randint(97, 122))
                            if i == 1:
                               symb = symb.upper()
                            prefix+=symb

                        shutil.move(
                        path_to_file , path_folder_for_sort + "\\" + name_of_group + f"\\{prefix}_{document_name}"
                    )
                        ####################################
                    else:
                        shutil.move(
                            path_to_file, path_folder_for_sort + "\\" + name_of_group + "\\"
                        )


def unpack_archives(path_to_archives, groups_of_format):

    # path to folder 'archives' with sorted archives
    path_to_archives = Path(str(path_to_archives) + "\\" + "archives")

    for archive in path_to_archives.rglob("*"):

        # checks if format is known in archive formats
        if archive.name.split(".")[-1].upper() in groups_of_format["archives"]:

            # gets name with archive name for folder
            path_for_unpack = Path(
                str(path_to_archives) + "\\" + archive.name.split(".")[0]
            )

            # creates folder with name for folder
            os.mkdir(path_for_unpack)

            # unpack archive to created folder
            shutil.unpack_archive(archive, path_for_unpack, archive.name.split(".")[-1])


def start_sorter():
    global chat_in_progress
    # ignore list with names of folders to be ignored
    IGNORE_LIST = ["images", "videos", "documents", "audios", "archives"]

    groups_of_format = {
        "images": ["JPEG", "PNG", "JPG", "SVG", "BMP"],
        "videos": ["AVI", "MP4", "MOV", "MKV"],
        "documents": ["DOC", "DOCX", "TXT", "PDF", "XLSX", "PPTX"],
        "audios": ["MP3", "OGG", "WAV", "AMR"],
        "archives": ["ZIP", "GZ", "TAR", "RAR"],
    }

    # dict with files in its type of format
    groups_of_files = {
        "images": [],
        "videos": [],
        "documents": [],
        "audios": [],
        "archives": [],
    }

    # input path to folder
    path_for_sort = input("\n(FOLDER SORTER) Input path to folder that you want to sort >>> ")

    if path_for_sort == "menu":
        chat_in_progress = False

    if not os.path.exists(path_for_sort):
        print('Your path does not exist!')
        return 

    # Create lists with names and paths to files and folders
    file_names, files_paths = parse_files(path_for_sort, IGNORE_LIST)
    folders_names, folders_paths = parse_folders(path_for_sort, IGNORE_LIST)

    # Create sets with all formats that we have
    set_of_formats, set_of_unknown_formats = generate_formats(
        file_names, groups_of_format
    )

    # Renaming
    rename_files(files_paths, groups_of_format)
    rename_folders(folders_paths)

    # Update lists with names and paths to files and folders after renaming
    file_names, files_paths = parse_files(path_for_sort, IGNORE_LIST)
    folders_names, folders_paths = parse_folders(path_for_sort, IGNORE_LIST)

    # Fill list with file names and formats of files
    for file in file_names:
        for name_group, formats in groups_of_format.items():
            if file.split(".")[-1].upper() in formats:
                groups_of_files[name_group].append(file)

    # Calling functions
    create_folders_from_groups(path_for_sort, groups_of_format)
    sort_files(files_paths, groups_of_files, path_for_sort, IGNORE_LIST)
    delete_empty_folders(folders_paths)
    unpack_archives(Path(path_for_sort), groups_of_format)

    # Data output block
    output_table = PrettyTable(["File type", "Number of files"])

    for name, list_of_formats in groups_of_files.items():
        output_table.add_row([name, len(list_of_formats)])

    output_table.add_row(["Known formats", len(set_of_formats)])
    output_table.add_row(["Unknown formats", len(set_of_unknown_formats)])

    print(output_table)

def main():
    global chat_in_progress
    chat_in_progress = True
    while chat_in_progress:
        start_sorter()

if __name__ == "__main__":
    main()
