from module.analysis_util import the_closest_sprint_start_date, get_the_last_sprint_bugs, debug_log_console
from module.file_util import *
from module.jba_email import send_email_from_graphics
from module.jira_bug import JiraBugList
from module.jira_method import is_system_available, system_init, get_fields_in_dict
from module.pyplot_util import *
from module.pyplot_util import bug_data_and_label_classified_in_catalog
from module.sys_invariant import date_format, show_last_n_bars, get_online_bug_summary_png_filename, \
    get_sprint_bug_summary_filename, graphic_path, online_bug_priority_png, online_bug_classification_png, \
    online_bug_unclassified_png, online_bug_source_in_csv, database_path


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


def generate_bug_priority_barhchart(bug_list):
    priority_data, priority_label = bug_data_and_label_classified_in_catalog(bug_list,
                                                                             ["Low", "Medium", "High", "Highest"],
                                                                             'priority')
    debug_log_console(str(priority_data))
    debug_log_console(str(priority_label))
    generate_barh_chart(priority_label, priority_data, online_bug_priority_png)
    return online_bug_priority_png


def generate_bug_classification_piechart(bug_list):
    classify_data, classify_label = bug_data_and_label_classified_in_catalog(bug_list,
                                                                             ["Fore-End", "Product Logic", "Server",
                                                                              "Third Part", "Wrong Reported"],
                                                                             'bug classify')
    debug_log_console(str(classify_data))
    debug_log_console(str(classify_label))
    generate_pie_chart(classify_label, classify_data, online_bug_classification_png, "Classification")
    return online_bug_classification_png


def generate_bug_unclassified_piechart(bug_list):
    classify_data, classify_label = bug_data_and_label_classified_in_catalog(bug_list,
                                                                             ["Fore-End", "Product Logic", "Server",
                                                                              "Third Part", "Wrong Reported"],
                                                                             'bug classify')
    unclassified_label = ["Clarified", "Non-Clarified"]
    unclassified_data = [sum(classify_data), (len(bug_list.bugs) - sum(classify_data))]
    debug_log_console(str(unclassified_label))
    debug_log_console(str(unclassified_data))
    generate_pie_chart(unclassified_label, unclassified_data, online_bug_unclassified_png, "Unclassified")
    return online_bug_unclassified_png


def write_bug_list_to_csv(bug_list):
    if bug_list.bugs[0] is None:
        return
    column_header = bug_list.bugs[0].keys()
    write_to_csv(column_header, bug_list.bugs, online_bug_source_in_csv)
    return online_bug_source_in_csv


def do_bug_analysis():
    basic_base64_token = system_init()
    if not is_system_available(basic_base64_token):
        print("system check failed, please ask admin")
        return

    bug_list = get_bug_list(basic_base64_token)

    # No.1 graphic - bug summary
    summary_barchart_filename = generate_bug_summary_barchart(bug_list)
    debug_log_console(summary_barchart_filename)

    # No.2 graphic - bug priority
    priority_barchart_filename = generate_bug_priority_barhchart(bug_list)
    debug_log_console(priority_barchart_filename)

    # No.3 graphic - bug classification
    classification_piechart_filename = generate_bug_classification_piechart(bug_list)
    debug_log_console(priority_barchart_filename)

    # No.4 graphic - bug unclassified
    unclassified_piechart_filename = generate_bug_unclassified_piechart(bug_list)
    debug_log_console(priority_barchart_filename)

    online_bug_source_filename = write_bug_list_to_csv(bug_list)
    debug_log_console(online_bug_source_filename)

    # final step - compose and send email
    graphs_full_path = [graphic_path + summary_barchart_filename,
                        graphic_path + priority_barchart_filename,
                        graphic_path + classification_piechart_filename,
                        graphic_path + unclassified_piechart_filename]
    file_full_path = database_path + online_bug_source_filename
    send_email_from_graphics(graphs_full_path, file_full_path)
