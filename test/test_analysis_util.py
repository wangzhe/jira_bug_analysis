import datetime
from unittest import TestCase

from module.analysis_util import the_closest_sprint_start_date, compose_search_jql_uri, get_last_sprint_duration


class AnalysisUtilTest(TestCase):
    def setUp(self):
        pass

    @staticmethod
    def test_write_down():
        # rows = ["testA1|testA2", "testB1|testB2", "testC1|testC2"]
        # write_cvs_items(rows=rows)
        pass

    def test_the_closest_sprint_start_date(self):
        input_date = datetime.datetime.strptime("11/03/18", "%m/%d/%y")
        sprint_end_date = the_closest_sprint_start_date(input_date)
        self.assertEqual(datetime.datetime.strptime("10/31/18", "%m/%d/%y"), sprint_end_date)

    def test_compose_search_jql(self):
        expect_jql_uri = "jql=project+%3D+OBT+AND+created+%3E%3D+%272018%2F10%2F03%27+AND+created+%3C+%272018%2F10%2" \
                         "F31%27+ORDER+BY+created+DESC"
        search_jql_uri = compose_search_jql_uri(datetime.datetime.strptime("10/31/18", "%m/%d/%y"))
        self.assertEqual(expect_jql_uri, search_jql_uri)

    def test_compose_search_jql_when_startAt_is_zero(self):
        expect_jql_uri = "jql=project+%3D+OBT+AND+created+%3E%3D+%272018%2F10%2F03%27+AND+created+%3C+%272018%2F10%2" \
                         "F31%27+ORDER+BY+created+DESC"
        search_jql_uri = compose_search_jql_uri(datetime.datetime.strptime("10/31/18", "%m/%d/%y"), 0)
        self.assertEqual(expect_jql_uri, search_jql_uri)

    def test_compose_search_jql_when_startAt_is_not_zero(self):
        expect_jql_uri = "jql=project+%3D+OBT+AND+created+%3E%3D+%272018%2F10%2F03%27+AND+created+%3C+%272018%2F10%2" \
                         "F31%27+ORDER+BY+created+DESC&startAt=50"
        search_jql_uri = compose_search_jql_uri(datetime.datetime.strptime("10/31/18", "%m/%d/%y"), 50)
        self.assertEqual(expect_jql_uri, search_jql_uri)

    def test_find_last_sprint_duration_with_date_input(self):
        start_date, end_date = get_last_sprint_duration(datetime.datetime.strptime("11/03/18", "%m/%d/%y"))
        self.assertEqual(datetime.datetime.strptime("10/17/18", "%m/%d/%y"), start_date)
        self.assertEqual(datetime.datetime.strptime("10/31/18", "%m/%d/%y"), end_date)
