import datetime
from unittest import TestCase

from module.pyplot_util import generate_bar_chart


class TestPlotlyUtil(TestCase):

    def test_generate_bar_chart_when_input_date_and_data(self):
        # x = [datetime.datetime(2010, 12, 1, 10, 0),
        #      datetime.datetime(2011, 1, 4, 9, 0),
        #      datetime.datetime(2011, 5, 5, 9, 0)]
        x = ["2010-12-1", "2011-1-4", "2011-5-5", "2012-1-5", "2013-5-5", "2014-5-5"]
        y = [4, 9, 2, 2, 7, 5]
        generate_bar_chart(x, y)
