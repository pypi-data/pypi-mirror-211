# -*- coding: utf-8 -*-

__all__ = (
    # exceptions
    "NotAFileError",
    "DirectoryNotFoundError",
    # path utils
    "stringify_path",
    "stringify_paths",
    "check_if_path_exists",
    "check_if_paths_exist",
    "check_if_file_exists",
    "check_if_files_exist",
    "check_if_dir_exists",
    "check_if_dirs_exist",
    "get_paths",
    "get_file_paths",
    "get_dir_paths",
    # type aliases
    "StrPath",
)

from kaparoo.filesystem.exceptions import DirectoryNotFoundError, NotAFileError
from kaparoo.filesystem.path import (
    check_if_dir_exists,
    check_if_dirs_exist,
    check_if_file_exists,
    check_if_files_exist,
    check_if_path_exists,
    check_if_paths_exist,
    get_dir_paths,
    get_file_paths,
    get_paths,
    stringify_path,
    stringify_paths,
)
from kaparoo.filesystem.types import StrPath
