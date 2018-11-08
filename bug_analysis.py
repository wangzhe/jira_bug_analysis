import datetime

from module.analysis_util import the_closest_sprint_start_date, get_the_last_sprint_bugs, debug_log_console
from module.file_util import file_backup, write_json_obj_to_file, read_json_from_file
from module.jba_email import JbaEmail
from module.jira_bug import JiraBugList
from module.jira_method import is_system_available, system_init, get_fields_in_dict
from module.pyplot_util import generate_bar_chart
from module.sys_invariant import date_format, show_last_n_bars, get_online_bug_summary_png_filename, \
    get_sprint_bug_summary_filename, graphic_path


def store_count_into_file(sprint_bug_summary_filename, last_sprint_bugs_count, sprint_start_date):
    file_backup(sprint_bug_summary_filename)
    sprint_online_bug_summary_json_data = read_json_from_file(sprint_bug_summary_filename)
    sprint_online_bug_summary_json_data = append_latest_sprint_info(last_sprint_bugs_count,
                                                                    sprint_online_bug_summary_json_data,
                                                                    sprint_start_date)
    write_json_obj_to_file(sprint_bug_summary_filename, sprint_online_bug_summary_json_data)
    return sprint_online_bug_summary_json_data


def append_latest_sprint_info(last_sprint_bugs_count, sprint_online_bug_summary_json_data, sprint_start_date):
    is_updated = False
    sprint_start_date_str = datetime.datetime.strftime(sprint_start_date, date_format["in_file"])
    for sprint_summary in sprint_online_bug_summary_json_data:
        if sprint_summary["sprint date"] == sprint_start_date_str:
            sprint_summary["sprint bug count"] = last_sprint_bugs_count
            is_updated = True
            break
    if not is_updated:
        sprint_online_bug_summary_json_data.append(
            {"sprint date": sprint_start_date_str,
             "sprint bug count": last_sprint_bugs_count})
    return sprint_online_bug_summary_json_data


def generate_online_bug_summary_chart(sprint_bug_summary_json, filename):
    dates, counts = convert_summary_into_dates_and_counts(sprint_bug_summary_json)
    debug_log_console(dates)
    generate_bar_chart(dates, counts, filename)


def convert_summary_into_dates_and_counts(sprint_bug_summary_json):
    dates = []
    counts = []

    for sprint_bug in sprint_bug_summary_json:
        dates.append(sprint_bug["sprint date"])
        counts.append(sprint_bug["sprint bug count"])
    return dates[show_last_n_bars:], counts[show_last_n_bars:]


def generate_bug_summary_barchart(bug_list):
    # find the latest sprint bugs
    last_sprint_bugs, sprint_start_date = get_the_last_sprint_bugs(bug_list)
    print(sprint_start_date)

    # store the count into file
    sprint_bug_summary_json = store_count_into_file(get_sprint_bug_summary_filename(), len(last_sprint_bugs),
                                                    sprint_start_date)

    # generate chart
    generate_online_bug_summary_chart(sprint_bug_summary_json, get_online_bug_summary_png_filename())

    return get_online_bug_summary_png_filename()


def get_bug_list(basic_base64_token):
    fields = get_fields_in_dict(basic_base64_token)
    sprint_start_date = the_closest_sprint_start_date(datetime.datetime.now())
    bug_list = JiraBugList(sprint_start_date, basic_base64_token, fields)

    is_list_fetched_successful = bug_list.fetch_list_from_jira()
    if not is_list_fetched_successful:
        return None
    print("total bugs: " + str(len(bug_list.bugs)))
    return bug_list


def generate_bug_priority_barchart(bug_list):
    return None


def do_analysis():
    basic_base64_token = system_init()
    if not is_system_available(basic_base64_token):
        print("system check failed, please ask admin")
        return

    bug_list = get_bug_list(basic_base64_token)

    # No.1 graphic - bug summary
    summary_barchart_filename = generate_bug_summary_barchart(bug_list)
    debug_log_console(summary_barchart_filename)

    # No.2 graphic - bug priority
    priority_barchart_filename = generate_bug_priority_barchart(bug_list)
    debug_log_console(priority_barchart_filename)

    # final step - compose and send email
    graphs_full_path = [graphic_path + summary_barchart_filename]
    jba_email = JbaEmail().instance
    email_body = jba_email.compose_email_body(graphs_full_path)
    jba_email.send_email(email_body.as_string())
