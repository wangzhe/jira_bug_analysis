import base64
import json

import requests

from module.analysis_util import debug_log_console, debug_log_json_file
from module.jira_system import JiraInfo


def get_current_user(base64_api_token):
    uri = "/rest/api/2/myself"
    response = get_response(base64_api_token, uri)
    return json.loads(response.text)


def get_response(base64_api_token, uri):
    url = "https://" + info.host + uri
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Basic " + base64_api_token,
        "Accept": "application/json",
    }
    response = requests.request(
        "GET",
        url,
        headers=headers
    )
    return response


def is_system_available(basic_base64_token):
    print("System checking ...")
    user_profile = get_current_user(basic_base64_token)
    print("System checked...done")
    return user_profile["active"]


def system_init():
    global info
    info = JiraInfo()
    my_token = info.user + ":" + info.token
    basic_base64_token = base64.b64encode(bytes(my_token, 'utf-8')).decode("utf-8")
    print(basic_base64_token)
    return basic_base64_token


def get_filter(base64_api_token, filter_id):
    uri = "/rest/api/3/filter/" + filter_id
    response = get_response(base64_api_token, uri)
    print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))


def search_online_bug_in_json(base64_api_token, jql_uri=""):
    uri = "/rest/api/3/search?" + jql_uri
    print("search bug from " + uri)
    response = get_response(base64_api_token, uri)
    debug_log_console(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
    return json.loads(response.text)


def get_fields_in_dict(basic_base64_token):
    field = {}

    uri = "/rest/api/3/field"
    print("fetch field from " + uri)
    response = get_response(basic_base64_token, uri)

    for item in json.loads(response.text):
        id_str = item['id']
        if id_str.startswith('customfield'):
            field[item['name']] = id_str
            debug_log_console(item['name'] + "----" + id_str)
    return field
