u"""Test for WREK download program."""

import unittest
import random
import os
import tempfile
from wrek_download import aux_functions
from wrek_download.parse_wrek_website import initialize_shows

# Ignore setting attribute outside init.
# pylama: ignore:W0201


class AuxiliarFunctionsTestCase(unittest.TestCase):

    u"""Test the aux_functions.py file."""

    def setUp(self):
        u"""Set up test framework."""

        # Non existent paths
        self.non_existent_folder_path = os.path.abspath(
            '/tmp/{0}'.format(random.random()))
        self.non_existent_file_path = os.path.abspath(
            '/tmp/{0}'.format(random.random()))

    def test_create_whitelist(self):
        u"""Test various errors for whitelist."""
        with self.assertRaises(FileNotFoundError):
            aux_functions.create_whitelist(
                self.non_existent_file_path)


class WREKShowTestCase(unittest.TestCase):

    u"""Test that an mp3 file was downloaded."""

    def setUp(self):
        u"""Set up test framework."""
        self.wrek_programs = initialize_shows()
        self.archive_folder = tempfile.TemporaryDirectory()
        self.temporary_folder = tempfile.TemporaryDirectory()
        self.output_folder = tempfile.TemporaryDirectory()
        self.program = None

class AtmosphericsTestCase(WREKShowTestCase):

    u"""Test that an Atmospherics mp3 file was downloaded."""

    def setUp(self):
        self.program = [x for x in self.wrek_programs if 'atmospherics' in x][0]



if __name__ == '__main__':
    unittest.main()
