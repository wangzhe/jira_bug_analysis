import getpass

date_format = {
    "default": "%m/%d/%y",
    "in_file": "%Y/%m/%d"
}

need_show_plot = False  # warning: variant
local_storage = True    # warning: variant

show_last_n_bars = -6
sprint_bug_summary_filename = "sprint_bug_summary.json"
online_bug_summary_png = "online_bug_summary.png"
online_bug_priority_png = "online_bug_priority.png"
online_bug_classification_png = "online_bug_classification.png"
online_bug_unclassified_png = "online_bug_unclassified.png"
online_bug_source_in_csv = 'source.csv'

graphic_path = "graphics/"
database_path = "database/"
config_path = "config/"
img_list = 'graphics'


def get_sprint_bug_summary_filename():
    return sprint_bug_summary_filename


def get_online_bug_summary_png_filename():
    return online_bug_summary_png


def get_system_user():
    return getpass.getuser()
