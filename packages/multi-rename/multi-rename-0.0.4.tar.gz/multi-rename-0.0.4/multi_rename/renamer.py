"""
Renamer Module.

This module contains functions for adding affixes,
and for full renaming.

An affix can either be a prefix or suffix.
Depending on the chosen type, the affix string
will be added to the start or end of the file name
respectively.

For full renaming, a new name is required which will be
given to all the files in a directory.

By default, the trailing numbers will start from 1,
with an increment of 1.
This can be configured as required.

A separator can also be optionally added between
the new name and the trailing number.

If any file types need to be excluded from the renaming
process, files with these extensions can be ignored.
"""

import os

def __add_affix(dir_path=None, affix=None, affix_type=None, sep=None, filter_ext=None):
    """
    Add an affix to the existing file names in a directory.

    Parameters
    ----------
    dir_path : str
        The directory which contains the files that need to be renamed
    affix: str
        The affix string which will be added to the existing
        file name
    affix_type: str
        The type of affix to be used. Possible values: prefix, suffix
    sep: str, optional
        Separator string to be used between the file name and affix
        (default is empty string)
    filter_ext : list of str, optional
        List of file extensions that should be ignored
        (default is an empty list)

    Returns
    -------
    renamed_files : list
        List of renamed file names.
    """
    renamed_files = []

    if dir_path is not None and affix is not None:

        # Handle trailing slash
        if not dir_path.endswith(os.path.sep):
            dir_path += os.path.sep

        file_list = os.listdir(dir_path)

        for file_str in file_list:
            file_path = os.path.join(dir_path, file_str)
            file_name, extension = os.path.splitext(file_str)

            # Skip any directories
            if not os.path.isdir(file_path):

                if filter_ext is None:
                    filter_ext = []

                # Skip any files which have extensions
                # that are to be ignored
                if filter_ext and extension[1:] in filter_ext:
                    continue

                if sep is None:
                    sep = ''

                # Create the new file name
                if affix_type == 'prefix':
                    repl_name = affix + sep + file_name + extension
                elif affix_type == 'suffix':
                    repl_name = file_name + sep + affix + extension

                # Create the destination path
                repl_path = os.path.join(dir_path, repl_name)

                # Rename the file
                os.replace(file_path, repl_path)

                renamed_files.append(repl_name)

    return renamed_files


def add_prefix(dir_path=None, prefix=None, sep=None, filter_ext=None):
    """
    Add a prefix to the existing file names in a directory.
    Wrapper for the __add_affix() function.
    """
    return __add_affix(dir_path=dir_path, affix=prefix, affix_type='prefix', sep=sep, filter_ext=filter_ext)


def add_suffix(dir_path=None, suffix=None, sep=None, filter_ext=None):
    """
    Add a prefix to the existing file names in a directory.
    Wrapper for the __add_affix() function.
    """
    return __add_affix(dir_path=dir_path, affix=suffix, affix_type='suffix', sep=sep, filter_ext=filter_ext)


def full_rename(dir_path=None, new_name=None, idx=1, increment=1, sep=None, filter_ext=None):
    """
    Rename all the files with a new name with incrementing numbers.

    Parameters
    ----------
    dir_path : str
        The directory which contains the files that need to be renamed
    new_name: str
        The new name for all the files in the directory
    idx: int
        Start value of the trailing number for the file name
        (default is 1)
    increment: int
        The amount by which to increment the trailing number
        (default is 1)
    sep: str, optional
        Separator string to be used between the file name and affix
        (default is an empty string)
    filter_ext : list of str, optional
        List of file extensions that should be ignored
        (default is an empty list)

    Returns
    -------
    renamed_files : list
        List of renamed file names.
    """
    renamed_files = []

    if dir_path is not None and new_name is not None:

        # Handle trailing slash
        if not dir_path.endswith(os.path.sep):
            dir_path += os.path.sep

        file_list = os.listdir(dir_path)

        for file_str in file_list:
            file_path = os.path.join(dir_path, file_str)
            extension = os.path.splitext(file_str)[1]

            # Skip any directories
            if not os.path.isdir(file_path):

                if filter_ext is None:
                    filter_ext = []

                # Skip any files which have extensions
                # that are to be ignored
                if filter_ext and extension[1:] in filter_ext:
                    continue

                if sep is None:
                    sep = ''

                # Create the new file name
                repl_name = new_name + sep + str(idx) + extension
                idx += increment

                # Create the destination path
                repl_path = os.path.join(dir_path, repl_name)

                # Rename the file
                os.replace(file_path, repl_path)

                renamed_files.append(repl_name)

    return renamed_files


def change_extension(dir_path=None, new_ext=None, filter_ext=None):
    """
    Change the file extensions for all files in a directory.

    Parameters
    ----------
    dir_path : str
        The directory which contains the files that need to be renamed
    new_ext: str
        The new file extension
    filter_ext : list of str, optional
        List of file extensions that should be ignored
        (default is an empty list)

    Returns
    -------
    renamed_file_exts : list
        List of renamed file names and extensions.
    """
    renamed_files = []

    if dir_path is not None and new_ext is not None:
        # Handle trailing slash
        if not dir_path.endswith(os.path.sep):
            dir_path += os.path.sep

        file_list = os.listdir(dir_path)

        for file_str in file_list:
            file_path = os.path.join(dir_path, file_str)
            file_name, extension = os.path.splitext(file_str)

            # Skip any directories
            if not os.path.isdir(file_path):

                if filter_ext is None:
                    filter_ext = []

                # Skip any files which have extensions
                # that are to be ignored
                if filter_ext and extension[1:] in filter_ext:
                    continue

                # Add a '.' to the file extension if not present
                if '.' not in new_ext:
                    new_ext = '.' + new_ext

                # Create the new file name
                repl_name = file_name + new_ext

                # Create the destination path
                repl_path = os.path.join(dir_path, repl_name)

                # Rename the file
                os.replace(file_path, repl_path)

                renamed_files.append(repl_name)
    
    return renamed_files