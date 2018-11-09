date_format = {
    "default": "%m/%d/%y",
    "in_file": "%Y/%m/%d"
}

show_last_n_bars = -6
sprint_bug_summary_filename = "sprint_bug_summary.json"
online_bug_summary_png = "online_bug_summary.png"
online_bug_priority_png = "online_bug_priority.png"
online_bug_classification_png = "online_bug_classification.png"


graphic_path = "graphics/"
database_path = "database/"
config_path = "config/"
img_list = 'graphics'

receivers = ['jack.wang@chope.co', '40646734@qq.com']


def get_sprint_bug_summary_filename():
    return sprint_bug_summary_filename


def get_online_bug_summary_png_filename():
    return online_bug_summary_png
