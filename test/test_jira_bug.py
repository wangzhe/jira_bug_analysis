import datetime
import json
from unittest import TestCase

from module.storage_util import read_json_from_file
from module.jira_bug import JiraBugList


class JiraBugTest(TestCase):
    def setUp(self):
        global bugList, online_bugs
        online_bugs = read_json_from_file('test_data_online_bug_unfinished.json')
        fields = self.read_field_json_data()
        bugList = JiraBugList(None, None, fields)
        bugList.update_bug_list_info(online_bugs)
        bugList.append_bugs(online_bugs)

    @staticmethod
    def read_field_json_data():
        with open('test_fields.json', 'r') as inputfile:
            json_data = inputfile.read()
            data = json.loads(json_data)
            fields = {}
            for item in data:
                id_str = item['id']
                if id_str.startswith('customfield'):
                    fields[item['name']] = id_str
        return fields

    def test_general_info_is_correct_when_read_test_data(self):
        self.assertEqual(102, bugList.total)
        self.assertEqual(50, bugList.max_results)
        self.assertEqual(50, bugList.next_start_at)

    def test_details_are_correct_when_read_test_data(self):
        bugs = bugList.bugs
        bug_dict = bugs[0]
        self.assertEqual("OBT-663", bug_dict["key"])
        self.assertEqual("Medium", bug_dict["priority"])
        self.assertEqual("Done", bug_dict["status"])
        self.assertEqual("Wrong Reported", bug_dict["bug classify"])
        self.assertEqual("2018-10-30T16:41:03.790+0800", bug_dict["created"])
        self.assertEqual("2018-10-30T17:58:49.852+0800", bug_dict["resolved"])
        self.assertEqual("2018-10-30T16:40:00.000+0800", bug_dict["first response time"])

    def test_total_bugs_after_data_read(self):
        bugs = bugList.bugs
        self.assertEqual(50, len(bugs))

    def test_is_completed_when_next_start_at_bigger_than_total(self):
        bugList.next_start_at = 150
        bugList.total = 102
        self.assertTrue(bugList.is_completed())

    def test_is_not_completed_when_total_is_zero(self):
        bugList.total = 0
        self.assertFalse(bugList.is_completed())

    def test_is_not_completed_when_next_start_at_less_than_total(self):
        bugList.next_start_at = 100
        bugList.total = 102
        self.assertFalse(bugList.is_completed())

    def test_get_bugs_by_duration_when_input_start_and_end_date(self):
        start_date = datetime.datetime.strptime("10/24/18", "%m/%d/%y")
        end_date = datetime.datetime.strptime("10/31/18", "%m/%d/%y")
        bugs = bugList.get_bugs_by_duration(start_date, end_date)
        self.assertEqual(14, len(bugs))
