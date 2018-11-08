import datetime

from module.analysis_util import compose_search_jql_uri, debug_log_console
from module.jira_method import search_online_bug_in_json


def get_value_in_level_two(bug_fields, level_one_name, level_two_name):
    if bug_fields[level_one_name] is None:
        return None
    return bug_fields[level_one_name][level_two_name]


def fetch_date_from_jira_cloud(basic_base64_token, sprint_start_date, start_at):
    search_uri = compose_search_jql_uri(sprint_start_date, start_at)
    debug_log_console(search_uri)
    online_bug_json = search_online_bug_in_json(basic_base64_token, search_uri)
    return online_bug_json


def bug_details(bug_dict, bug_fields, fields):
    bug_dict["priority"] = get_value_in_level_two(bug_fields, "priority", "name")
    bug_dict["assignee"] = get_value_in_level_two(bug_fields, "assignee", "name")
    bug_dict["status"] = get_value_in_level_two(bug_fields, "status", "name")
    bug_dict["bug classify"] = get_value_in_level_two(bug_fields, fields["Bug Classify"], "value")
    bug_dict["created"] = bug_fields["created"]
    bug_dict["resolved"] = bug_fields["resolutiondate"]
    bug_dict["first response time"] = bug_fields[fields["First Response Time"]]
    return bug_dict


def is_fetch_data_error(online_bug_json):
    return (online_bug_json is None) or (online_bug_json is "")


class JiraBugList:

    def __init__(self, sprint_start_date, basic_base64_token, fields):
        self.sprint_start_date = sprint_start_date
        self.basic_base64_token = basic_base64_token
        self.fields = fields

        self.total = 0
        self.next_start_at = 0
        self.max_results = 0
        self.bugs = []

    def fetch_list_from_jira(self):
        while not self.is_completed():
            debug_log_console("fetch data from " + str(self.next_start_at) + "...")
            online_bug_json = fetch_date_from_jira_cloud(self.basic_base64_token, self.sprint_start_date,
                                                         self.next_start_at)
            if is_fetch_data_error(online_bug_json):
                return False
            self.update_bug_list_info(online_bug_json)
            self.append_bugs(online_bug_json)
        return True

    def update_bug_list_info(self, online_bug_json):
        self.total = online_bug_json["total"]
        self.max_results = online_bug_json["maxResults"]
        self.next_start_at = online_bug_json["startAt"] + self.max_results

    def append_bugs(self, online_bug_json):
        for item in online_bug_json["issues"]:
            bug_dict = {"key": item["key"]}
            bug_fields = item["fields"]
            bug_dict = bug_details(bug_dict, bug_fields, self.fields)
            self.bugs.append(bug_dict)

    def get_bugs_by_duration(self, start_date, end_date):
        result_bug_list = []
        for bug in self.bugs:
            # like 2018-10-30T16:29:04.105+0800
            created_date = datetime.datetime.strptime(bug['created'][:10], '%Y-%m-%d')
            print(datetime.datetime.strftime(created_date, "%Y-%m-%d"))
            if (created_date >= start_date) and (created_date < end_date):
                result_bug_list.append(bug)
        return result_bug_list

    def is_completed(self):
        if (self.total is 0) or (self.next_start_at < self.total):
            return False
        return True
