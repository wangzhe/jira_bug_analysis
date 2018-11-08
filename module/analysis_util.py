import datetime
from urllib.parse import urlencode

from module.file_util import write_json_to_file
from module.jira_system import JiraInfo


def get_last_sprint_duration(date):
    return (the_closest_sprint_start_date(date) - datetime.timedelta(days=14)), (the_closest_sprint_start_date(date))


def the_closest_sprint_start_date(input_date, init_sprint_start_date_str="08/22/18"):
    calculated_date = sprint_start_date = datetime.datetime.strptime(init_sprint_start_date_str, "%m/%d/%y")
    sprint_count = 0
    while calculated_date < input_date:
        sprint_count = sprint_count + 14
        start_date = calculated_date
        calculated_date = sprint_start_date + datetime.timedelta(days=sprint_count)
    debug_log_console("the_closest_sprint_start_date:" + datetime.datetime.strftime(start_date, "%y/%m/%d"))
    return start_date


def get_the_last_sprint_bugs(bug_list):
    start_date, end_date = get_last_sprint_duration(datetime.datetime.now())
    return bug_list.get_bugs_by_duration(start_date, end_date), start_date


def compose_search_jql_uri(next_sprint_start_date, start_at=0):
    jql_start_date = (next_sprint_start_date - datetime.timedelta(days=14 * 2)).strftime("%Y/%m/%d")
    jql_end_date = next_sprint_start_date.strftime("%Y/%m/%d")
    jql_str = "project = OBT AND created >= '" + \
              jql_start_date + "' AND created < '" + \
              jql_end_date + "' ORDER BY created DESC"
    jql_dict = {'jql': jql_str}
    if start_at > 0:
        jql_dict['startAt'] = start_at
    jql_uri = urlencode(jql_dict)
    return jql_uri


def debug_log_console(text, debug_mode=False):
    if JiraInfo().instance.is_debug() or debug_mode:
        print(text)


def debug_log_json_file(response, filename='temp.json', debug_mode=False):
    if JiraInfo().instance.is_debug() or debug_mode:
        write_json_to_file(filename, response)
