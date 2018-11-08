date_format = {
    "default": "%m/%d/%y",
    "in_file": "%Y/%m/%d"
}

show_last_n_bars = -6
sprint_bug_summary_filename = "sprint_bug_summary.json"
online_bug_summary_png = "online_bug_summary.png"
graphic_path = "graphics/"
database_path = "database/"
config_path = "config/"

sender = 'aaa@.ddd.com'
receiver = 'bbb@.eee.com'
subject = 'python email with pictures'
smtpserver = 'smtp.sina.com.cn'
img_list = 'graphics'


def get_sprint_bug_summary_filename():
    return sprint_bug_summary_filename


def get_online_bug_summary_png_filename():
    return online_bug_summary_png
