from unittest import TestCase

from bug_analysis import do_bug_analysis
from module.pyplot_util import generate_bar_chart, generate_barh_chart, generate_pie_chart


class TestMain(TestCase):

    def test_main_process(self):
        # all debug in local
        do_bug_analysis()
        # pass

