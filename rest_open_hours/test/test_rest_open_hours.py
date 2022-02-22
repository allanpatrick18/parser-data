import unittest
from datetime import datetime
from rest_open_hours import open_hours
from rest_open_hours import database


class TestRestOpenHours(unittest.TestCase):

    def test_parse_csv_into_table(self):
        open_hours.parse_csv_into_table()

    def test_open_csv(self):
        open_hours.read_csv()

    def test_convert_range_1(self):
        open_hours.convert_open_range("Mon-Sun 11:30 am - 9 pm")

    def test_convert_range_2(self):
        for item in "Mon-Thu, Sun 11:30 am - 9 pm  / Fri-Sat 11:30 am - 9:30 pm".split('/'):
            open_hours.convert_open_range(item)

    def test_convert_range_3(self):
        for item in "Mon-Thu 11 am - 11 pm  / Fri-Sat 11 am - 12:30 am  / Sun 10 am - 11 pm".split('/'):
            open_hours.convert_open_range(item)

    def test_convert_to_time_am(self):
        res = open_hours.convert_to_time("11 AM")
        self.assertEqual(res, "11:00:00")

    def test_convert_to_time_pm(self):
        res = open_hours.convert_to_time("11:00 PM")
        self.assertEqual(res, "23:00:00")

    def test_query(self):
        res = open_hours.list_open_restaurants(datetime.today())
        self.assertTrue(len(res) > 0)

    def test_query_open(self):
        res = open_hours.query_open_hours()
        self.assertTrue(len(res) > 0)

    def test_model_insert(self):
        model = database.OpenHours()
        restaurant = database.Restaurant(name='Kushi Tsuru')
        database.session.add(restaurant)
        database.session.commit()
        open_h = open_hours.convert_open_range("Mon-Sun 11:30 am - 9 pm")
        for hours in open_h:
            model.name = 'test'
            model.restaurant = restaurant.id
            model.week_day_begin = open_hours.week_day[hours['week_day_begin'].lower()]
            model.week_day_end = open_hours.week_day[hours['week_day_end'].lower()]
            model.time_begin = open_hours.convert_to_time(hours['time_begin'])
            model.time_end = open_hours.convert_to_time(hours['time_end'])
            database.session.add(model)
            database.session.commit()



