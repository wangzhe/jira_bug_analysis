from unittest import TestCase

from module.pyplot_util import generate_bar_chart, generate_barh_chart, generate_pie_chart


class TestPlotlyUtil(TestCase):

    def test_generate_bar_chart_when_input_date_and_data(self):
        # x = [datetime.datetime(2010, 12, 1, 10, 0),
        #      datetime.datetime(2011, 1, 4, 9, 0),
        #      datetime.datetime(2011, 5, 5, 9, 0)]
        x = ["2010-12-1", "2011-1-4", "2011-5-5", "2012-1-5", "2013-5-5", "2014-5-5"]
        y = [4, 9, 2, 2, 7, 5]
        generate_bar_chart(x, y)

    def test_generate_barh_chart_when_input_date_and_data(self):
        # label = [datetime.datetime(2010, 12, 1, 10, 0),
        #      datetime.datetime(2011, 1, 4, 9, 0),
        #      datetime.datetime(2011, 5, 5, 9, 0)]
        label = ['Low', 'Medium', 'High', 'Highest']
        data = [1, 48, 0, 0]
        generate_barh_chart(label, data)

    def test_generate_pie_chart_when_input_date_and_data(self):
        label = ['Fore-End', 'Product Logic', 'Server', 'Third Part', 'Wrong Reported']
        data = [7, 3, 15, 3, 15]
        generate_pie_chart(label, data, "some_file")
