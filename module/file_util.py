import csv
import datetime
import json
import os
from shutil import copyfile

from module.sys_invariant import database_path as db


def get_database_full_path(filename):
    return db + filename


def convert_dict_into_list(row_data):
    return row_data.values()


def is_filename_existed(sprint_bug_summary_filename):
    has_source_file = has_backup_file = False
    for file in os.listdir("./"):
        if file == sprint_bug_summary_filename:
            has_source_file = True
        if file == sprint_bug_summary_filename.replace(".json", "") + "_" + datetime.date.today().strftime(
                "%m_%d_%y") + ".json":
            has_backup_file = True
    return has_source_file and has_backup_file


def file_backup(sprint_bug_summary_filename):
    sprint_bug_summary_filename = get_database_full_path(sprint_bug_summary_filename)

    copyfile(sprint_bug_summary_filename,
             sprint_bug_summary_filename.replace(".json", "") + "_" + datetime.date.today().strftime(
                 "%m_%d_%y") + ".json")


def file_recover(sprint_bug_summary_filename):
    sprint_bug_summary_filename = get_database_full_path(sprint_bug_summary_filename)

    if not is_filename_existed(sprint_bug_summary_filename):
        return
    copyfile(sprint_bug_summary_filename.replace(".json", "") + "_" + datetime.date.today().strftime(
        "%m_%d_%y") + ".json", sprint_bug_summary_filename)


def write_json_obj_to_file(data_filename, jsonobj):
    data_filename = get_database_full_path(data_filename)

    with open(data_filename, 'w') as outfile:
        json.dump(jsonobj, outfile)


def read_json_from_file(data_filename):
    data_filename = get_database_full_path(data_filename)

    with open(data_filename) as input_file:
        json_data = json.load(input_file)
    return json_data


def write_html_to_file(data_filename, html_text):
    data_filename = get_database_full_path(data_filename)

    with open(data_filename, 'w') as outfile:
        outfile.write(html_text)


def read_html_from_file(data_filename):
    data_filename = get_database_full_path(data_filename)

    with open(data_filename) as input_file:
        html_text = input_file.read()
    return html_text


def write_to_csv(header, data, data_filename='source.csv'):
    data_filename = get_database_full_path(data_filename)

    with open(data_filename, mode='w') as source_file:
        csv_writer = csv.writer(source_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        csv_writer.writerow(header)
        for row_data in data:
            row_list = convert_dict_into_list(row_data)
            csv_writer.writerow(row_list)
