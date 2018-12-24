import json
import re
from unittest import TestCase

from module import file_util
from module.oss_util import check_oss


class TestOSSUtil(TestCase):

    def test_oss_available(self):
        object_str = check_oss()
        object_strip_str = re.sub(r'\s+', '', object_str)
        expect_str = str(file_util.read_json_from_file("test_oss_bug_summary.json"))
        expect_strip_str = expect_str.replace(" ", "")
        expect_strip_str = expect_strip_str.replace("\'", "\"")
        self.assertEqual(expect_strip_str, object_strip_str)
