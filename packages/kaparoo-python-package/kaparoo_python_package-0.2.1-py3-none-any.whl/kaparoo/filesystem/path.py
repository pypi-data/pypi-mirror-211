# -*- coding: utf-8 -*-

from __future__ import annotations

__all__ = (
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
)

import os
import random
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import TYPE_CHECKING, Literal, overload

from kaparoo.filesystem.exceptions import DirectoryNotFoundError, NotAFileError

if TYPE_CHECKING:
    from kaparoo.filesystem.types import StrPath


def stringify_path(path: StrPath) -> str:
    """Convert a path to a string representation."""
    return os.fspath(path)


def stringify_paths(paths: Sequence[StrPath]) -> Sequence[str]:
    """Convert a sequence of paths to a sequence of string representations."""
    return [stringify_path(p) for p in paths]


@overload
def check_if_path_exists(path: StrPath, *, stringify: Literal[False] = False) -> Path:
    ...


@overload
def check_if_path_exists(path: StrPath, *, stringify: Literal[True]) -> str:
    ...


@overload
def check_if_path_exists(path: StrPath, *, stringify: bool) -> Path | str:
    ...


def check_if_path_exists(path: StrPath, *, stringify: bool = False) -> Path | str:
    """Check if a given path exists and return it as a `Path` object.

    Args:
        path: The path to check for existence.
        stringify: Whether to return the path as a string. Defaults to `False`.

    Returns:
        The path as a `Path` object or a string, depending on the value of `stringify`.

    Raises:
        FileNotFoundError: If the path does not exist.
    """

    if not (path := Path(path)).exists():
        raise FileNotFoundError(f"no such path: {path}")

    return stringify_path(path) if stringify else path


@overload
def check_if_paths_exist(
    paths: Sequence[StrPath],
    *,
    root: StrPath | None = None,
    stringify: Literal[False] = False,
) -> Sequence[Path]:
    ...


@overload
def check_if_paths_exist(
    paths: Sequence[StrPath], *, root: StrPath | None = None, stringify: Literal[True]
) -> Sequence[str]:
    ...


@overload
def check_if_paths_exist(
    paths: Sequence[StrPath], *, root: StrPath | None = None, stringify: bool
) -> Sequence[Path] | Sequence[str]:
    ...


def check_if_paths_exist(
    paths: Sequence[StrPath], *, root: StrPath | None = None, stringify: bool = False
) -> Sequence[Path] | Sequence[str]:
    """Check if multiple paths exist and return them as a sequence of `Path` objects.

    Args:
        paths: A sequence of paths to check for existence.
        root: The root directory to resolve relative paths. If provided, the `paths`
            will be resolved relative to the `root` directory. Defaults to `None`.
        stringify: Whether to return a sequence of strings. Defaults to `False`.

    Returns:
        The paths as a sequence of `Path` objects or a sequence of strings,
            depending on the value of `stringify`.

    Raises:
        DirectoryNotFoundError: If the `root` directory does not exist.
        NotADirectoryError: If `root` exists but is not a directory.
        FileNotFoundError: If any of the paths does not exist.
    """

    if root is not None:
        root = check_if_dir_exists(root)
        paths = [root / p for p in paths]

    paths = [check_if_path_exists(p) for p in paths]

    return stringify_paths(paths) if stringify else paths


@overload
def check_if_file_exists(path: StrPath, *, stringify: Literal[False] = False) -> Path:
    ...


@overload
def check_if_file_exists(path: StrPath, *, stringify: Literal[True]) -> str:
    ...


@overload
def check_if_file_exists(path: StrPath, *, stringify: bool) -> Path | str:
    ...


def check_if_file_exists(path: StrPath, *, stringify: bool = False) -> Path | str:
    """Check if a given path exists and is a file, and return it as a `Path` object.

    Args:
        path: The file path to check for existence.
        stringify: Whether to return the path as a string. Defaults to `False`.

    Returns:
        The path as a `Path` object or a string, depending on the value of `stringify`.

    Raises:
        FileNotFoundError: If the path does not exist.
        NotAFileError: If the path exists but is not a file.
    """

    if not (path := Path(path)).exists():
        raise FileNotFoundError(f"no such file: {path}")
    elif not path.is_file():
        raise NotAFileError(f"not a file: {path}")

    return stringify_path(path) if stringify else path


@overload
def check_if_files_exist(
    paths: Sequence[StrPath],
    *,
    root: StrPath | None = None,
    stringify: Literal[False] = False,
) -> Sequence[Path]:
    ...


@overload
def check_if_files_exist(
    paths: Sequence[StrPath], *, root: StrPath | None = None, stringify: Literal[True]
) -> Sequence[str]:
    ...


@overload
def check_if_files_exist(
    paths: Sequence[StrPath], *, root: StrPath | None = None, stringify: bool
) -> Sequence[Path] | Sequence[str]:
    ...


def check_if_files_exist(
    paths: Sequence[StrPath], *, root: StrPath | None = None, stringify: bool = False
) -> Sequence[Path] | Sequence[str]:
    """Check if multiple files exist and return them as a sequence of `Path` objects.

    Args:
        paths: A sequence of file paths to check for existence.
        root: The root directory to resolve relative paths. If provided, the `paths`
            will be resolved relative to the `root` directory. Defaults to `None`.
        stringify: Whether to return a sequence of strings. Defaults to `False`.

    Returns:
        The file paths as a sequence of `Path` objects or a sequence of strings,
            depending on the value of `stringify`.

    Raises:
        DirectoryNotFoundError: If the `root` directory does not exist.
        NotADirectoryError: If `root` exists but is not a directory.
        FileNotFoundError: If any of the file paths does not exist.
        NotAFileError: If any of the paths exists but is not a file.
    """  # noqa: E501

    if root is not None:
        root = check_if_dir_exists(root)
        paths = [root / p for p in paths]

    paths = [check_if_file_exists(p) for p in paths]

    return stringify_paths(paths) if stringify else paths


@overload
def check_if_dir_exists(
    path: StrPath, *, make: bool | int = False, stringify: Literal[False] = False
) -> Path:
    ...


@overload
def check_if_dir_exists(
    path: StrPath, *, make: bool | int = False, stringify: Literal[True]
) -> str:
    ...


@overload
def check_if_dir_exists(
    path: StrPath, *, make: bool | int = False, stringify: bool
) -> Path | str:
    ...


def check_if_dir_exists(
    path: StrPath, *, make: bool | int = False, stringify: bool = False
) -> Path | str:
    """Check if a given path exists and is a directory, and return it as a `Path` object.

    Args:
        path: The directory path to check for existence.
        make: Whether to create the directory if it does not exist. If an `int` is provided,
            use it as the octal mode for the directory. Defaults to `False`.
        stringify: Whether to return the path as a string. Defaults to `False`.

    Returns:
        The path as a `Path` object or a string, depending on the value of `stringify`.

    Raises:
        DirectoryNotFoundError: If the path does not exist and `make` is False.
        NotADirectoryError: If the path exists but is not a directory.
    """  # noqa: E501

    if not (path := Path(path)).exists():
        if make is False:
            raise DirectoryNotFoundError(f"no such directory: {path}")
        path.mkdir(mode=511 if make is True else make, parents=True)  # 511 == 0o777
    elif not path.is_dir():
        raise NotADirectoryError(f"not a directory: {path}")

    return stringify_path(path) if stringify else path


@overload
def check_if_dirs_exist(
    paths: Sequence[StrPath],
    *,
    root: StrPath | None = None,
    make: bool | int = False,
    stringify: Literal[False] = False,
) -> Sequence[Path]:
    ...


@overload
def check_if_dirs_exist(
    paths: Sequence[StrPath],
    *,
    root: StrPath | None = None,
    make: bool | int = False,
    stringify: Literal[True],
) -> Sequence[str]:
    ...


@overload
def check_if_dirs_exist(
    paths: Sequence[StrPath],
    *,
    root: StrPath | None = None,
    make: bool | int = False,
    stringify: bool,
) -> Sequence[Path] | Sequence[str]:
    ...


def check_if_dirs_exist(
    paths: Sequence[StrPath],
    *,
    root: StrPath | None = None,
    make: bool | int = False,
    stringify: bool = False,
) -> Sequence[Path] | Sequence[str]:
    """Check if multiple directories exist and return them as a sequence of `Path` objects.

    Args:
        paths: A sequence of directory paths to check for existence.
        root: The root directory to resolve relative paths. If provided, the `paths`
            will be resolved relative to the `root` directory. Defaults to `None`.
        make: Whether to create the directory if it does not exist. If an `int` is provided,
            use it as the octal mode for the directory. Defaults to `False`.
        stringify: Whether to return a sequence of strings. Defaults to `False`.

    Returns:
        The directory paths as a sequence of `Path` objects or a sequence of strings,
            depending on the value of `stringify`.

    Raises:
        DirectoryNotFoundError: If the `root` directory does not exist
        DirectoryNotFoundError: If any of the directory paths does not exist.
        NotADirectoryError: If `root` exists but is not a directory.
        NotADirectoryError: If any of the paths exists but is not a directory.
    """  # noqa: E501

    if root is not None:
        root = check_if_dir_exists(root)
        paths = [root / p for p in paths]

    paths = [check_if_dir_exists(p, make=make) for p in paths]

    return stringify_paths(paths) if stringify else paths


@overload
def get_paths(
    root: StrPath,
    *,
    pattern: str | None = None,
    num_samples: int | None = None,
    ignores: Sequence[StrPath] | None = None,
    condition: Callable[[Path], bool] | None = None,
    recursive: bool = True,
    stringify: Literal[False] = False,
) -> Sequence[Path]:
    ...


@overload
def get_paths(
    root: StrPath,
    *,
    pattern: str | None = None,
    num_samples: int | None = None,
    ignores: Sequence[StrPath] | None = None,
    condition: Callable[[Path], bool] | None = None,
    recursive: bool = True,
    stringify: Literal[True],
) -> Sequence[str]:
    ...


@overload
def get_paths(
    root: StrPath,
    *,
    pattern: str | None = None,
    num_samples: int | None = None,
    ignores: Sequence[StrPath] | None = None,
    condition: Callable[[Path], bool] | None = None,
    recursive: bool = True,
    stringify: bool,
) -> Sequence[Path] | Sequence[str]:
    ...


def get_paths(
    root: StrPath,
    *,
    pattern: str | None = None,
    num_samples: int | None = None,
    ignores: Sequence[StrPath] | None = None,
    condition: Callable[[Path], bool] | None = None,
    recursive: bool = True,
    stringify: bool = False,
) -> Sequence[Path] | Sequence[str]:
    """Get paths of files or directories in a given directory.

    Args:
        root: The directory to search for paths.
        pattern: A glob pattern to match the paths against. Defaults to `None` and
            automatically uses "*" to list all paths included in the `root` directory.
        num_samples: A maximum number of paths to return. If given and its value is
            smaller than the total number of paths, only the `num_samples` paths of the
            total are randomly selected and returned. Hence, even using the same value
            of `num_samples`, may return a different result. Defaults to `None`.
        ignores: A sequence of paths to ignore. If any path in `ignores` does not start
            with `root`, it is treated as a relative path. For example, `any/path` is
            treated as `root/any/path`. Defaults to `None`.
        condition: A predicate that takes a `Path` object and decides whether to include
            the path in the results. Defaults to `None`.
        recursive: Whether to search for paths recursively in subdirectories of the
            `root` directory. Defaults to `True`.
        stringify: Whether to return a sequence of strings. Defaults to `False`.

    Returns:
        The paths that match the specified criteria as a sequence of `Path` objects or a
            sequence of strings, depending on the value of `stringify`.

    Raises:
        DirectoryNotFoundError: If `root` does not exist.
        NotADirectoryError: If `root` exists but is not a directory.
        ValueError: If `num_samples` is not a positive int.
    """  # noqa: E501

    root = check_if_dir_exists(root)

    if not isinstance(pattern, str):
        pattern = "*"

    matched = root.rglob(pattern) if recursive else root.glob(pattern)
    paths = [p for p in matched]

    if root in paths:
        paths.remove(root)

    if not ignores:
        ignores = []

    for ignore in ignores:
        ignore_path = Path(ignore)
        if root not in ignore_path.parents:
            ignore_path = root / ignore_path

        if ignore_path in paths:
            paths.remove(ignore_path)

    if callable(condition):
        paths = [p for p in paths if condition(p)]

    if isinstance(num_samples, int) and num_samples < len(paths):
        if num_samples <= 0:
            raise ValueError("`num_samples` must be a positive int")
        paths = random.sample(paths, num_samples)

    return stringify_paths(paths) if stringify else paths


@overload
def get_file_paths(
    root: StrPath,
    *,
    pattern: str | None = None,
    num_samples: int | None = None,
    ignores: Sequence[StrPath] | None = None,
    condition: Callable[[Path], bool] | None = None,
    recursive: bool = True,
    stringify: Literal[False] = False,
) -> Sequence[Path]:
    ...


@overload
def get_file_paths(
    root: StrPath,
    *,
    pattern: str | None = None,
    num_samples: int | None = None,
    ignores: Sequence[StrPath] | None = None,
    condition: Callable[[Path], bool] | None = None,
    recursive: bool = True,
    stringify: Literal[True],
) -> Sequence[str]:
    ...


@overload
def get_file_paths(
    root: StrPath,
    *,
    pattern: str | None = None,
    num_samples: int | None = None,
    ignores: Sequence[StrPath] | None = None,
    condition: Callable[[Path], bool] | None = None,
    recursive: bool = True,
    stringify: bool,
) -> Sequence[Path] | Sequence[str]:
    ...


def get_file_paths(
    root: StrPath,
    *,
    pattern: str | None = None,
    num_samples: int | None = None,
    ignores: Sequence[StrPath] | None = None,
    condition: Callable[[Path], bool] | None = None,
    recursive: bool = True,
    stringify: bool = False,
) -> Sequence[Path] | Sequence[str]:
    """Get paths of files in a given directory.

    Args:
        root: The directory to search for paths.
        pattern: A glob pattern to match the paths against. Defaults to `None` and
            automatically uses "*" to list all paths included in the `root` directory.
        num_samples: A maximum number of paths to return. If given and its value is
            smaller than the total number of paths, only the `num_samples` paths of the
            total are randomly selected and returned. Hence, even using the same value
            of `num_samples`, may return a different result. Defaults to `None`.
        ignores: A sequence of paths to ignore. If any path in `ignores` does not start
            with `root`, it is treated as a relative path. For example, `any/path` is
            treated as `root/any/path`. Defaults to `None`.
        condition: A predicate that takes a `Path` object and decides whether to include
            the path in the results. Defaults to `None`.
        recursive: Whether to search for paths recursively in subdirectories of the
            `root` directory. Defaults to `True`.
        stringify: Whether to return a sequence of strings. Defaults to `False`.

    Returns:
        The file paths that match the specified criteria as a sequence of `Path` objects
            or a sequence of strings, depending on the value of `stringify`.

    Raises:
        DirectoryNotFoundError: If `root` does not exist.
        NotADirectoryError: If `root` exists but is not a directory.
        ValueError: If `num_samples` is not a positive int.
    """  # noqa: E501

    if not callable(condition):
        file_condition = lambda p: p.is_file()  # noqa: E731
    else:
        file_condition = lambda p: p.is_file() and condition(p)  # type: ignore[misc] # noqa: E501, E731

    file_paths = get_paths(
        root,
        pattern=pattern,
        num_samples=num_samples,
        ignores=ignores,
        condition=file_condition,
        recursive=recursive,
        stringify=stringify,
    )

    return file_paths


@overload
def get_dir_paths(
    root: StrPath,
    *,
    pattern: str | None = None,
    num_samples: int | None = None,
    ignores: Sequence[StrPath] | None = None,
    condition: Callable[[Path], bool] | None = None,
    recursive: bool = True,
    stringify: Literal[False] = False,
) -> Sequence[Path]:
    ...


@overload
def get_dir_paths(
    root: StrPath,
    *,
    pattern: str | None = None,
    num_samples: int | None = None,
    ignores: Sequence[StrPath] | None = None,
    condition: Callable[[Path], bool] | None = None,
    recursive: bool = True,
    stringify: Literal[True],
) -> Sequence[str]:
    ...


@overload
def get_dir_paths(
    root: StrPath,
    *,
    pattern: str | None = None,
    num_samples: int | None = None,
    ignores: Sequence[StrPath] | None = None,
    condition: Callable[[Path], bool] | None = None,
    recursive: bool = True,
    stringify: bool,
) -> Sequence[Path] | Sequence[str]:
    ...


def get_dir_paths(
    root: StrPath,
    *,
    pattern: str | None = None,
    num_samples: int | None = None,
    ignores: Sequence[StrPath] | None = None,
    condition: Callable[[Path], bool] | None = None,
    recursive: bool = True,
    stringify: bool = False,
) -> Sequence[Path] | Sequence[str]:
    """Get paths of directories in a given directory.

    Args:
        root: The directory to search for paths.
        pattern: A glob pattern to match the paths against. Defaults to `None` and
            automatically uses "*" to list all paths included in the `root` directory.
        num_samples: A maximum number of paths to return. If given and its value is
            smaller than the total number of paths, only the `num_samples` paths of the
            total are randomly selected and returned. Hence, even using the same value
            of `num_samples`, may return a different result. Defaults to `None`.
        ignores: A sequence of paths to ignore. If any path in `ignores` does not start
            with `root`, it is treated as a relative path. For example, `any/path` is
            treated as `root/any/path`. Defaults to `None`.
        condition: A predicate that takes a `Path` object and decides whether to include
            the path in the results. Defaults to `None`.
        recursive: Whether to search for paths recursively in subdirectories of the
            `root` directory. Defaults to `True`.
        stringify: Whether to return a sequence of strings. Defaults to `False`.

    Returns:
        The directory paths that match the specified criteria as a sequence of `Path`
            objects or a sequence of strings, depending on the value of `stringify`.

    Raises:
        DirectoryNotFoundError: If `root` does not exist.
        NotADirectoryError: If `root` exists but is not a directory.
        ValueError: If `num_samples` is not a positive int.
    """  # noqa: E501

    if not callable(condition):
        dir_condition = lambda p: p.is_dir()  # noqa: E731
    else:
        dir_condition = lambda p: p.is_dir() and condition(p)  # type: ignore[misc] # noqa: E501, E731

    dir_paths = get_paths(
        root,
        pattern=pattern,
        num_samples=num_samples,
        ignores=ignores,
        condition=dir_condition,
        recursive=recursive,
        stringify=stringify,
    )

    return dir_paths
