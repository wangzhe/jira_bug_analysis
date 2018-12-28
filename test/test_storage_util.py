import json
from unittest import TestCase
from unittest.mock import MagicMock

from module import sys_invariant
from module.jira_system import JiraInfo
from module.storage_util import read_json_from_file, is_debug_in_local


class TestStorageUtil(TestCase):
    def test_read_json_from_file_in_local(self):
        sys_invariant.get_debug_against_oss = MagicMock(name='debug_against_oss')
        sys_invariant.get_debug_against_oss.return_value = False

        json_data = read_json_from_file("test_read_file_in_oss_local.json")
        print(type(json.dumps(json_data)))
        self.assertEqual(str, type(json.dumps(json_data)))

    def test_read_json_from_file_in_oss(self):
        sys_invariant.get_debug_against_oss = MagicMock(name='debug_against_oss')
        sys_invariant.get_debug_against_oss.return_value = True

        json_data = read_json_from_file("test_read_file_in_oss_remotely.json")
        print(type(json.dumps(json_data)))
        self.assertEqual(str, type(json.dumps(json_data)))

    def test_is_debug_in_local_false_when_not_debug(self):
        test_instance = JiraInfo().instance
        test_instance.is_debug = MagicMock(name='is_debug')
        test_instance.is_debug.return_value = False

        sys_invariant.get_debug_against_oss = MagicMock(name='debug_against_oss')
        sys_invariant.get_debug_against_oss.return_value = False

        self.assertFalse(is_debug_in_local())

    def test_is_debug_in_local_false_when_against_oss(self):
        test_instance = JiraInfo().instance
        test_instance.is_debug = MagicMock(name='is_debug')
        test_instance.is_debug.return_value = False

        sys_invariant.get_debug_against_oss = MagicMock(name='debug_against_oss')
        sys_invariant.get_debug_against_oss.return_value = True

        self.assertFalse(is_debug_in_local())

    def test_is_debug_in_local_true_when_not_against_oss_and_do_debug(self):
        test_instance = JiraInfo().instance
        test_instance.is_debug = MagicMock(name='is_debug')
        test_instance.is_debug.return_value = True

        sys_invariant.get_debug_against_oss = MagicMock(name='debug_against_oss')
        sys_invariant.get_debug_against_oss.return_value = False

        self.assertTrue(is_debug_in_local())

    def test_is_debug_in_local_false_when_against_oss_and_do_debug(self):
        test_instance = JiraInfo().instance
        test_instance.is_debug = MagicMock(name='is_debug')
        test_instance.is_debug.return_value = True

        sys_invariant.get_debug_against_oss = MagicMock(name='debug_against_oss')
        sys_invariant.get_debug_against_oss.return_value = True

        self.assertFalse(is_debug_in_local())

    def tearDown(self):
        super().tearDown()
        test_instance = JiraInfo().instance
        test_instance.is_debug = MagicMock(name='is_debug')
        test_instance.is_debug.return_value = True

        sys_invariant.get_debug_against_oss = MagicMock(name='debug_against_oss')
        sys_invariant.get_debug_against_oss.return_value = False
