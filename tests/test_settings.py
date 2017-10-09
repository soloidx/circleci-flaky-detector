# -*- coding:utf-8 -*-
import unittest

import settings


SECRET_EXAMPLE = {
        u'secret1': 'secret'
}


class TestSettings(unittest.TestCase):
    """test for settings module"""
    def test_get_secret_sould_exist(self):
        self.assertTrue(hasattr(settings, 'get_secret'))

    def test_get_secret_sould_return_a_parameter(self):
        self.assertEqual(settings.get_secret('secret1', SECRET_EXAMPLE),
                         'secret')

    def test_get_secret_sould_thwor_an_error_on_inexist_key(self):
        self.assertRaises(NotImplementedError,
                          settings.get_secret, 'secret2', SECRET_EXAMPLE)
