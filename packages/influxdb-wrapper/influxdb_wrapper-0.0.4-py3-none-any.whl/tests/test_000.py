import unittest
import os
import sys
import inspect

from influxdb_wrapper import influxdb_factory


class Testing(unittest.TestCase):
    db = influxdb_factory(db_type='mock')
    db.openConn(None)

    def test_insert(self):
        points = [
                    {"tags": {"sensorid": 0}, "fields": {"temp": 20.0, "humidity": 50.0}},
                    {"tags": {"sensorid": 0}, "fields": {"temp": 21.0, "humidity": 50.1}},
                    {"tags": {"sensorid": 1}, "fields": {"temp": 10.0, "humidity": 100.0}}
                 ]
        self.db.insert('DHT22', points)

    def test_select(self):
        points = self.db. select('DHT22', [('sensorid', 0)], order_by='time', order_asc=False, limit=1)
        self.assertEqual(len(points), 1)


if __name__ == '__main__':
    unittest.main()
