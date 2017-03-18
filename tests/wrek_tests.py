u"""Test for WREK download program."""

import unittest
import random
import os
import sys
import tempfile
sys.path.insert(0, os.path.abspath('../wrek_download/wrek_download'))

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
        # Paths
        self.archive_path = tempfile.TemporaryDirectory()
        self.temporary_path = tempfile.TemporaryDirectory()
        self.output_path = tempfile.TemporaryDirectory()
        self.whitelist_path = tempfile.TemporaryFile()
        self.program = None


class AtmosphericsTestCase(WREKShowTestCase):

    u"""Test that an Atmospherics mp3 file was downloaded."""

    def setUp(self):
        u"""Set up test framework."""
        super(AtmosphericsTestCase, self,).setUp()
        self.program = [x for x in self.wrek_programs if 'atmospherics' in x][0]
        print(self.program)

    def test_print_attr(self):
        for attr in dir(self):
            print(attr, getattr(self, attr))



if __name__ == '__main__':
    unittest.main()
