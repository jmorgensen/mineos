#!/usr/bin/env python2.7

import unittest
import os

from mineos import mc
from shutil import rmtree

class TestMineOS(unittest.TestCase):
    def setUp(self):
        from pwd import getpwnam
        from getpass import getuser
        self._owner = getpwnam(getuser())
        self._path = self._owner.pw_dir

    def tearDown(self):
        for d in ('servers', 'backup', 'archive', 'log'):
            try:
                rmtree(os.path.join(self._path, d))
            except OSError:
                continue
  
    def test_bare_environment(self):
        for s in (None, '', False):
            instance = mc()
            self.assertIsNone(instance.server_name)
            with self.assertRaises(AttributeError):
                instance.env

    def test_binary_paths(self):
        instance = mc()
        for k,v in instance.BINARY_PATHS.iteritems():
            self.assertIsInstance(v, str)
            self.assertTrue(v)

    def test_valid_server_name(self):
        bad_names = ['this!', 'another,server', '"hello"',
                     '.minecraft', 'top^sirloin', 'me@you',
                     'server-with-hyphens','`', '\t',
                     'minecraft 1.6', '']

        ok_names = ['server', 'pvp', '21324', 'server_one',
                    'minecraft1.6', '_a_server']

        for server_name in bad_names:
            with self.assertRaises(ValueError):
                instance = mc(server_name)

        for server_name in ok_names:
            instance = mc(server_name)
            self.assertIsNotNone(instance.server_name)

    def test_set_owner(self):
        instance = mc('one')
        
        self.assertTrue(self._owner, instance._owner)

    def test_load_config(self):
        from conf_reader import config_file
        
        instance = mc('one')

        self.assertIsInstance(instance.server_properties, config_file)
        self.assertIsInstance(instance.server_properties[:], dict)
        self.assertIsInstance(instance.server_config, config_file)
        self.assertIsInstance(instance.server_config[:], dict)

        self.assertFalse(os.path.isfile(instance.env['sp']))
        self.assertFalse(os.path.isfile(instance.env['sc']))
        
    def test_create_sp(self):
        '''instance = mc('one')

        instance._create_sp()
        self.assertTrue(os.path.isfile(instance.env['sp']))
        self.assertFalse(instance.server_config[:])

        self._load_config()
        self.assertTrue(instance.server_config[:])'''
        pass
        




if __name__ == "__main__":
    unittest.main()  
