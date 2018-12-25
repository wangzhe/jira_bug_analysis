import datetime
import json
from unittest import TestCase
from unittest.mock import Mock

from bug_analysis import store_count_into_file, generate_online_bug_summary_chart, generate_bug_summary_barchart, \
    append_latest_sprint_info, generate_bug_priority_barhchart, \
    generate_bug_classification_piechart, generate_bug_unclassified_piechart, write_bug_list_to_csv
from module.pyplot_util import bug_data_and_label_classified_in_catalog
from module import jira_bug
from module.storage_util import read_json_from_file, file_recover
from module.jira_bug import JiraBugList
from module.sys_invariant import date_format, online_bug_source_in_csv


class TestAnalysis(TestCase):

    def setUp(self):
        global bugList, filename

        self.test_filename = "test_sprint_bug_summary.json"
        file_recover(self.test_filename)
        filename = "sprint_bug_summary.json"
        file_recover(filename)

        online_bugs = read_json_from_file('test_data_online_bug_completed.json')

        jira_bug.fetch_date_from_jira_cloud = Mock()
        jira_bug.fetch_date_from_jira_cloud.return_value = online_bugs
        fields = self.read_field_json_data()

        bugList = JiraBugList(None, None, fields)
        bugList.fetch_list_from_jira()

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

    def test_online_bug_summary(self):
        generate_bug_summary_barchart(bugList)

    def test_store_count_into_file(self):
        sprint_online_bug_summary_json_data = store_count_into_file(filename, 15,
                                                                    datetime.datetime.strptime("10/31/18",
                                                                                               date_format["default"]))

    def test_generate_online_bug_summary_chart(self):
        bug_summary_json = read_json_from_file(filename)
        generate_online_bug_summary_chart(bug_summary_json, None)

    def test_append_latest_sprint_info_when_input_date_duplicated(self):
        expect_json = sprint_online_bug_summary_json_data = read_json_from_file(self.test_filename)
        sprint_start_date = datetime.datetime.strptime(expect_json[1]["sprint date"], date_format["in_file"])
        last_sprint_bugs_count = 0
        sprint_online_bug_summary_json_data = append_latest_sprint_info(last_sprint_bugs_count,
                                                                        sprint_online_bug_summary_json_data,
                                                                        sprint_start_date)
        self.assertEqual(0, sprint_online_bug_summary_json_data[1]["sprint bug count"])

    def test_append_latest_sprint_info_when_input_date_new(self):
        sprint_online_bug_summary_json_data = read_json_from_file(self.test_filename)
        sprint_start_date = datetime.datetime.strptime("2018/08/09", date_format["in_file"])
        last_sprint_bugs_count = 0
        sprint_online_bug_summary_json_data = append_latest_sprint_info(last_sprint_bugs_count,
                                                                        sprint_online_bug_summary_json_data,
                                                                        sprint_start_date)
        self.assertEqual(0, sprint_online_bug_summary_json_data[len(sprint_online_bug_summary_json_data) - 1][
            "sprint bug count"])

    def test_bug_data_and_label_classified_in_catalog(self):
        priority_data, priority_label = bug_data_and_label_classified_in_catalog(bugList,
                                                                                 ["Low", "Medium", "High", "Highest"],
                                                                                 'priority')
        self.assertEqual(1, priority_data[0])
        self.assertEqual(48, priority_data[1])

    def test_generate_bug_priority_barhchart(self):
        generate_bug_priority_barhchart(bugList)

    def test_generate_bug_classification_piechart(self):
        generate_bug_classification_piechart(bugList)

    def test_generate_bug_unclassified_piechart(self):
        generate_bug_unclassified_piechart(bugList)

    def test_write_bug_list_to_csv(self):
        self.assertEqual(online_bug_source_in_csv, write_bug_list_to_csv(bugList))
