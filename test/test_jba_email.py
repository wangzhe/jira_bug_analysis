from unittest import TestCase

from module.jba_email import JbaEmail
from module.storage_util import read_html_from_file, write_html_to_file
from module.sys_invariant import graphic_path, online_bug_summary_png, database_path, online_bug_source_in_csv


class TestJbaEmail(TestCase):

    def setUp(self):
        global jba_email
        jba_email = JbaEmail().instance

    def test_compose_email_body(self):
        with open(graphic_path + "test_" + online_bug_summary_png, "rb") as graphic_file:
            binary_img = graphic_file.read()
        print(type(binary_img))
        print(binary_img)
        graphs_full_path = [binary_img]
        attach_file_full_path = database_path + online_bug_source_in_csv
        email_body = jba_email.compose_email_body(graphs_full_path, attach_file_full_path)
        write_html_to_file("test2.eml", email_body.as_string())
        html_text = read_html_from_file("test.eml")
        self.assertEqual(html_text[:10], email_body.as_string()[:10])

    # def test_send_email(self):
    #     html_text = read_html_from_file("test2.eml")
    #     print(jba_email.receivers[0])
    #     jba_email.send_email(html_text)
