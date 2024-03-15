import os
import subprocess
import unittest
from tempfile import TemporaryDirectory

from e2xgrader.exchange.hash_utils import (
    generate_directory_hash_file,
    truncate_hashcode,
)


class TestGenerateDirectoryHashFile(unittest.TestCase):

    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        self.directory = self.temp_dir.name

        # Create some test files
        with open(os.path.join(self.directory, "file1.txt"), "w") as f:
            f.write("Test file 1")
        with open(os.path.join(self.directory, "file2.txt"), "w") as f:
            f.write("Test file 2")
        with open(os.path.join(self.directory, "notebook.ipynb"), "w") as f:
            f.write("Test notebook")
        os.makedirs(os.path.join(self.directory, ".ipynb_checkpoints"))
        with open(
            os.path.join(self.directory, ".ipynb_checkpoints", "notebook.ipynb"), "w"
        ) as f:
            f.write("Test checkpoint")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_generate_directory_hash_file_without_exclusions_and_sha1(self):
        generate_directory_hash_file(
            self.directory, method="sha1", output_file="hashes.txt"
        )
        # Call sha1sum to check the hash codes. Make sure the output is as expected.
        expected_output = (
            ".ipynb_checkpoints/notebook.ipynb: OK\n"
            "file1.txt: OK\n"
            "file2.txt: OK\n"
            "notebook.ipynb: OK\n"
        )
        output = subprocess.check_output(
            f"cd {self.directory} && sha1sum -c hashes.txt",
            shell=True,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
        )
        self.assertEqual(output, expected_output)

    def test_generate_directory_hash_file_without_exclusions_and_md5(self):
        generate_directory_hash_file(
            self.directory, method="md5", output_file="hashes.txt"
        )
        # Call sha1sum to check the hash codes. Make sure the output is as expected.
        expected_output = (
            ".ipynb_checkpoints/notebook.ipynb: OK\n"
            "file1.txt: OK\n"
            "file2.txt: OK\n"
            "notebook.ipynb: OK\n"
        )
        output = subprocess.check_output(
            f"cd {self.directory} && md5sum -c hashes.txt",
            shell=True,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
        )
        self.assertEqual(output, expected_output)

    def test_generate_directory_hash_file_with_exclusions(self):
        generate_directory_hash_file(
            self.directory,
            method="sha1",
            exclude_files=["*.txt"],
            exclude_subfolders=[".ipynb_checkpoints"],
            output_file="hashes.txt",
        )
        # Call sha1sum to check the hash codes. Make sure the output is as expected.
        expected_output = "notebook.ipynb: OK\n"
        output = subprocess.check_output(
            f"cd {self.directory} && sha1sum -c hashes.txt",
            shell=True,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
        )
        self.assertEqual(output, expected_output)

    def test_generate_directory_hash_file_with_nonexistent_directory(self):
        with self.assertRaises(FileNotFoundError):
            generate_directory_hash_file(
                "nonexistent_directory", output_file="hashes.txt"
            )

    def test_generate_directory_hash_file_with_specified_output_file(self):
        output_file = os.path.join(self.directory, "output_hashes.txt")
        generate_directory_hash_file(
            self.directory, method="sha1", output_file=output_file
        )
        self.assertTrue(os.path.exists(output_file))

    def test_generate_directory_hash_file_excludes_output_file(self):
        output_file = os.path.join(self.directory, "file1.txt")
        generate_directory_hash_file(
            self.directory, method="sha1", output_file=output_file
        )
        with open(output_file, "r") as f:
            content = f.read()
        self.assertNotIn("hashes.txt", content)

    def test_generate_directory_hash_file_excludes_files_in_subfolders(self):
        generate_directory_hash_file(
            self.directory,
            method="sha1",
            exclude_files=["*.ipynb"],
            output_file="hashes.txt",
        )
        with open(os.path.join(self.directory, "hashes.txt"), "r") as f:
            content = f.read()
            self.assertNotIn(".ipynb_checkpoints/notebook.ipynb", content)
            self.assertNotIn("notebook.ipynb", content)

    def test_generate_directory_hash_file_with_unsupported_hash_method(self):
        with self.assertRaises(ValueError):
            generate_directory_hash_file(
                self.directory, method="unsupported_method", output_file="hashes.txt"
            )


class TestTruncateHashcode(unittest.TestCase):

    def test_truncate_hashcode(self):
        hashcode = "1234567890abcdef"
        self.assertEqual(
            truncate_hashcode(hashcode, number_of_chunks=1, chunk_size=4), "1234"
        )
        self.assertEqual(
            truncate_hashcode(hashcode, number_of_chunks=2, chunk_size=3), "123-456"
        )
        self.assertEqual(
            truncate_hashcode(hashcode, number_of_chunks=2, chunk_size=10),
            "1234567890-abcdef",
        )
