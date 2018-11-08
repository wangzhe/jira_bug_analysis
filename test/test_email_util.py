from unittest import TestCase

from module.email_util import compose_email_body
from module.file_util import write_html_to_file
from module.sys_invariant import graphic_path, online_bug_summary_png


class TestEmailUtil(TestCase):
    def test_compose_email_body(self):
        graphs_full_path = [graphic_path + "test_" + online_bug_summary_png]
        print(graphs_full_path)
        email_body = compose_email_body(graphs_full_path)
        write_html_to_file("test.eml", email_body.as_string())
