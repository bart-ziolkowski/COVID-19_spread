import unittest
import app


SAMPLE_RATIO = 1e6
START_DATE = '2021-04-01'
END_DATE = '2022-04-30'


class Test(unittest.TestCase):
    def run_test(self):
        app.run(countries_csv_name='a3-countries.csv', countries=['Denmark','Sweden','Norway'], sample_ratio= SAMPLE_RATIO, start_date= START_DATE, end_date= END_DATE)


unittest.main()
