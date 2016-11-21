u"""Test for WREK download program."""

import unittest
import random
import os
from wrek_download import aux_functions

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

if __name__ == '__main__':
    unittest.main()
