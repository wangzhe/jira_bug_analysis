from unittest import TestCase

from module.oss_util import get_file


class TestOSSUtil(TestCase):
    def test_get_file(self):
        get_file()
