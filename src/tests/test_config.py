#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   test_config.py
@Time    :   2022/05/01 19:53:41
@Author  :   Javier G. Visiedo 
@Version :   1.0
@Contact :   javier.g.visiedo@gmail.com
@License :   (C)Copyright 2021-2022, RedMice
@Desc    :   None
'''
import unittest
from unittest import TestCase, mock
from io import StringIO

import sys
import os
import json

sys.path.append(os.path.dirname(
                os.path.dirname(os.path.realpath(__file__))
                ))
import config as conf

class TestConfig(TestCase):

    @mock.patch('sys.stderr', new_callable = StringIO)
    def test_error_message(self, stderr):
        """
        Test that error message is printed on stderr
        """

        # Test config_error()
        conf.config_error("error message")
        out = 'error message\n'

        # Check stderr
        self.assertEqual(stderr.getvalue(), out)

    @mock.patch('sys.stderr', new_callable = StringIO)
    def test_exit_on_critical(self, stderr):
        """
        Test that the program exits on critical errors parsing config
        """
        out = 'error message\n'
        with self.assertRaises(SystemExit) as cm:
            conf.config_error("error message", is_fatal=True)

        self.assertEqual(cm.exception.code, 1)
        self.assertEqual(stderr.getvalue(), out)
    
    @mock.patch('sys.stderr', new_callable = StringIO)
    def test_loadSettings_from_json_file(self, stderr):
        # test valid JSON
        file_contents = json.dumps(
            {
                "metamask_address": "0x174BA736AF8808F8283D6beFC01cB6C6976D5F91",
                "metamask_private_key": "YOUR-PRIVATE-KEY"
            }
        )
        m = mock.mock_open(read_data=file_contents)
        with mock.patch('config.open', m):
            result = conf.loadSettings()
        self.assertEqual(
            {
                "metamask_address": "0x174BA736AF8808F8283D6beFC01cB6C6976D5F91",
                "metamask_private_key": "YOUR-PRIVATE-KEY"
            },
            result)

    @mock.patch('sys.stderr', new_callable = StringIO)
    def test_loadSettings_json_syntax_error(self, stderr):
        file_contents = ' '
        m = mock.mock_open(read_data=file_contents)
        out = "Syntax error on "
        with mock.patch('config.open', m):
            with self.assertRaises(SystemExit) as fatal:
                result=conf.loadSettings()

        self.assertEqual(fatal.exception.code, 1)
        self.assertTrue(stderr.getvalue().startswith(out))
        
    @mock.patch('sys.stderr', new_callable = StringIO)
    def test_loadSettings_file_does_not_exist(self, stderr):

        out = "Fatal error: The config file"
        m = mock.mock_open(read_data='')
        with mock.patch('config.open', m):
            m.side_effect = FileNotFoundError
            with self.assertRaises(SystemExit) as fatal:
                conf.loadSettings()
        self.assertTrue(stderr.getvalue().startswith(out))
        self.assertEqual(fatal.exception.code, 1)

if __name__ == '__main__':
    unittest.main()
