import fnmatch
import hashlib
import os
from typing import List, Tuple


def compute_hashcode_of_file(filename, method="sha1") -> str:
    """
    Compute the hash code of a file.

    Args:
        filename (str): The path to the file.
        method (str, optional): The hash algorithm to use. Defaults to "sha1".

    Returns:
        str: The computed hash code.

    Raises:
        ValueError: If the specified method is not supported.
    """
    if method == "md5":
        hashcode = hashlib.md5()
    elif method == "sha1":
        hashcode = hashlib.sha1()
    else:
        raise ValueError("Currently only the methods md5 and sha1 are supported!")

    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hashcode.update(chunk)

    return hashcode.hexdigest()


def hash_files_in_directory(
    directory,
    method="sha1",
    exclude_files=None,
    exclude_subfolders=None,
) -> List[Tuple[str, str]]:
    """
    Hashes all files in a directory using the specified method.

    Args:
        directory (str): The directory path to hash files in.
        method (str, optional): The hashing method to use. Defaults to "sha1".
        exclude_files (List[str], optional): List of file names or patterns to exclude from hashing.
            Defaults to None.
        exclude_subfolders (List[str], optional): List of subfolder names to exclude from hashing.
            Defaults to None.

    Returns:
        List[Tuple[str, str]]: A list of tuples containing the relative file paths and their
            corresponding hash codes.

    Examples:
        >>> hash_files_in_directory("path/to/directory")
        [
            ("file1.txt", "hashcode1"),
            ("file2.txt", "hashcode2"),
            ("notebook.ipynb", "hashcode3"),
            (".ipynb_checkpoints/notebook-checkpoint.ipynb", "hashcode4"),
            ...
        ]
        >>> hash_files_in_directory(
                "path/to/directory",
                exclude_files=["*.txt"],
                exclude_subfolders=[".ipynb_checkpoints"]
            )
        [
            ("notebook.ipynb", "hashcode3"),
            ...
        ]
    """
    if exclude_files is None:
        exclude_files = []
    if exclude_subfolders is None:
        exclude_subfolders = []
    else:
        exclude_subfolders = [
            os.path.normpath(subfolder) for subfolder in exclude_subfolders
        ]

    hashes = dict()

    for root, dirs, files in os.walk(directory):
        for file in files:
            if any(fnmatch.fnmatch(file, pattern) for pattern in exclude_files):
                continue
            if any([subfolder in root for subfolder in exclude_subfolders]):
                continue
            filename = os.path.join(root, file)
            hashes[os.path.relpath(filename, start=directory)] = (
                compute_hashcode_of_file(filename, method)
            )

    return sorted(hashes.items())


def generate_directory_hash_file(
    directory,
    method="sha1",
    exclude_files=None,
    exclude_subfolders=None,
    output_file="hashes.txt",
):
    """
    Creates a file containing the hash codes of all files in a directory.

    Args:
        directory (str): The directory path to hash files in.
        method (str, optional): The hashing method to use. Defaults to "sha1".
        exclude_files (List[str], optional): List of file names or patterns to exclude from hashing.
            Defaults to None.
        exclude_subfolders (List[str], optional): List of subfolder names to exclude from hashing.
            Defaults to None.
        output_file (str, optional): The name of the file to write the hash codes to.
            Defaults to "hashes.txt".
    """
    if exclude_files is None:
        exclude_files = [output_file]
    else:
        exclude_files.append(output_file)

    hashes = hash_files_in_directory(
        directory, method, exclude_files, exclude_subfolders
    )
    formatted_hashes = "\n".join(
        [f"{hashcode}  {filename}" for filename, hashcode in hashes]
    )
    with open(os.path.join(directory, output_file), "w") as f:
        f.write(formatted_hashes)


def truncate_hashcode(hashcode, number_of_chunks=3, chunk_size=4):
    """
    Truncate a hash code into a more readable format.

    Args:
        hashcode (str): The hash code to truncate.
        number_of_chunks (int, optional): The number of chunks to split the hash code into.
            Defaults to 4.
        chunk_size (int, optional): The size of each chunk. Defaults to 5.

    Returns:
        str: The truncated hash code.
    """
    hash_string = ""
    for i in range(0, number_of_chunks * chunk_size, chunk_size):
        hash_string += f"-{hashcode[i:i+chunk_size]}"
    return hash_string[1:]
