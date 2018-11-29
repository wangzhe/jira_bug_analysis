from module.jira_method import system_init, is_system_available, get_all_sprints_in_board, get_active_sprints_in_board, \
    get_sprint_story_in_board, get_reports_in_board

board_dict = {
    "comm_board": 24,
    "cb_board": 4,
    "mr_board": 1,
    "admin_board": 8,
    "app_board": 5,
    "wid_board": 7,
    "api_board": 23
}


def do_story_analysis():
    basic_base64_token = system_init()
    # if not is_system_available(basic_base64_token):
    #     print("system check failed, please ask admin")
    #     return

    # bpards_list = get_boards(basic_base64_token, "COMM board")
    # something = get_all_sprints_in_board(basic_base64_token, 24)
    # something = get_sprint_story_in_board(basic_base64_token, 24, 450)
    # something = get_active_sprints_in_board(basic_base64_token, 24)
    something = get_reports_in_board(basic_base64_token, 24)

    # No.1 graphic - bug summary

    # final step - compose and send email
    # graphs_full_path = [graphic_path + summary_barchart_filename]
    # send_email_from_graphics(graphs_full_path)s
