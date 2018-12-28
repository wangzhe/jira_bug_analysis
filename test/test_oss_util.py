import datetime
import re
from unittest import TestCase

from module import storage_util
from module.oss_util import read_file_in_oss, copy_file, delete_file
from module.pyplot_util import generate_pie_chart


class TestOSSUtil(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_read_file_in_oss(self):
        object_str = read_file_in_oss('test_read_file_in_oss_remotely.json')
        object_strip_str = re.sub(r'\s+', '', object_str)
        expect_str = str(storage_util.read_json_from_file_locally("test_read_file_in_oss_local.json"))
        expect_strip_str = expect_str.replace(" ", "")
        expect_strip_str = expect_strip_str.replace("\'", "\"")
        self.assertEqual(expect_strip_str, object_strip_str)

    def test_save_image_oss(self):
        label = ['Fore-End', 'Product Logic', 'Server', 'Third Part', 'Wrong Reported']
        data = [7, 3, 15, 3, 15]
        generate_pie_chart(label, data, "test_oss_upload_file_" + datetime.date.today().strftime(
            "%m_%d_%y") + ".png")

    def test_copyfile(self):
        copy_file("test_read_file_in_oss_remotely.json", "test_read_file_in_oss_remotely2.json")
        source = read_file_in_oss("test_read_file_in_oss_remotely.json")
        target = read_file_in_oss("test_read_file_in_oss_remotely2.json")
        self.assertEqual(source, target)

    def test_delete_file(self):
        copy_file("test_read_file_in_oss_remotely.json", "test_read_file_in_oss_remotely2.json")
        self.assertTrue(delete_file("test_read_file_in_oss_remotely2.json"))
