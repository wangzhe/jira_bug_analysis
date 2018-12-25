import datetime
import re
from unittest import TestCase

from module import storage_util, sys_invariant
from module.oss_util import check_oss
from module.pyplot_util import generate_pie_chart


class TestOSSUtil(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        sys_invariant.local_storage = True

    def test_oss_available(self):
        object_str = check_oss()
        object_strip_str = re.sub(r'\s+', '', object_str)
        expect_str = str(storage_util.read_json_from_file("test_oss_bug_summary.json"))
        expect_strip_str = expect_str.replace(" ", "")
        expect_strip_str = expect_strip_str.replace("\'", "\"")
        self.assertEqual(expect_strip_str, object_strip_str)

    def test_save_image_oss(self):
        label = ['Fore-End', 'Product Logic', 'Server', 'Third Part', 'Wrong Reported']
        data = [7, 3, 15, 3, 15]
        print(sys_invariant.local_storage)
        generate_pie_chart(label, data, "test_oss_upload_file_" + datetime.date.today().strftime(
            "%m_%d_%y") + ".png")

