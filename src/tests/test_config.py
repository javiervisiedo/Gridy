#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   test_config.py
@Time    :   2022/05/01 19:53:41
@Author  :   Javier G. Visiedo
@Version :   0.0.1
@Contact :   javier.g.visiedo@gmail.com
@License :   (C)Copyright 2021-2022, RedMice
@Desc    :   None
'''
import os
import sys

sys.path.append(os.path.dirname(
                os.path.dirname(os.path.realpath(__file__))
                ))
import config as conf

import json
import unittest
from io import StringIO
from unittest import TestCase, mock



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
        with self.assertRaises(SystemExit) as raised:
            conf.config_error("error message", is_fatal=True)

        self.assertEqual(raised.exception.code, 1)
        self.assertEqual(stderr.getvalue(), out)

    def test_load_settings_from_json_file(self):
        # test valid JSON
        file_contents = json.dumps(
            {
                "metamask_address": "0x174BA736AF8808F8283D6beFC01cB6C6976D5F91",
                "metamask_private_key": "YOUR-PRIVATE-KEY"
            }
        )
        m = mock.mock_open(read_data=file_contents)
        with mock.patch('config.open', m):
            result = conf.load_settings()
        self.assertEqual(
            {
                "metamask_address": "0x174BA736AF8808F8283D6beFC01cB6C6976D5F91",
                "metamask_private_key": "YOUR-PRIVATE-KEY"
            },
            result)

    @mock.patch('sys.stderr', new_callable = StringIO)
    def test_load_settings_json_syntax_error(self, stderr):
        file_contents = ' '
        m = mock.mock_open(read_data=file_contents)
        out = "Syntax error on "
        with mock.patch('config.open', m):
            with self.assertRaises(SystemExit) as fatal:
                conf.load_settings()

        self.assertEqual(fatal.exception.code, 1)
        self.assertTrue(stderr.getvalue().startswith(out))

    @mock.patch('sys.stderr', new_callable = StringIO)
    def test_load_settings_file_does_not_exist(self, stderr):

        out = "Fatal error: The config file"
        m = mock.mock_open(read_data='')
        with mock.patch('config.open', m):
            m.side_effect = FileNotFoundError
            with self.assertRaises(SystemExit) as fatal:
                conf.load_settings()
        self.assertTrue(stderr.getvalue().startswith(out))
        self.assertEqual(fatal.exception.code, 1)

if __name__ == '__main__':
    unittest.main()
