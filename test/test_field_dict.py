import json
from unittest import TestCase


class FileUtilTest(TestCase):
    def setUp(self):
        pass

    def test_json_in_dict(self):
        with open('test_fields.json', 'r') as inputfile:
            json_data = inputfile.read()
            data = json.loads(json_data)
            for item in data:
                id_str = item['id']
                if id_str.startswith('customfield'):
                    print(item['id'] + "----" + item['name'])
