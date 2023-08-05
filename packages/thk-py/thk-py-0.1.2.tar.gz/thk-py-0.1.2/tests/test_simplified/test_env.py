# -*- coding: utf-8 -*-
import unittest
import os

from thk_py.simplified import env


class T(unittest.TestCase):
    test_key = 'test_key'

    def tearDown(self) -> None:
        super().tearDown()
        if os.environ.get(self.test_key, None):
            del os.environ[self.test_key]

    def test__get_str(self):
        self.assertEqual(env.get_str(self.test_key), None)
        os.environ[self.test_key] = 'None'
        self.assertEqual(env.get_str(self.test_key), None)

        v = 'abc'
        self.assertEqual(env.get_str(self.test_key, default=v), v)

        os.environ[self.test_key] = v
        self.assertEqual(env.get_str(self.test_key), v)

    def test__get_int(self):
        self.assertEqual(env.get_int(self.test_key), None)

        v = 123
        self.assertEqual(env.get_int(self.test_key, default=v), v)

        os.environ[self.test_key] = str(v)
        self.assertEqual(env.get_int(self.test_key), v)

    def test__get_bool(self):
        self.assertEqual(env.get_bool(self.test_key), None)

        v = True
        self.assertEqual(env.get_bool(self.test_key, default=v), v)

        os.environ[self.test_key] = str(v)
        self.assertEqual(env.get_bool(self.test_key), v)

        os.environ[self.test_key] = '123'
        self.assertEqual(env.get_bool(self.test_key), False)
