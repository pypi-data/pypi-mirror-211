import unittest
from tests.persistence_testcase import PersistenceTestCase
import datetime


class DatetimePersistenceTest(PersistenceTestCase):

    def test_insert_date(self):
        today: datetime.date = datetime.date.today()
        doc = {
            'today': today
        }
        doc_id = self.dao.insert(**doc)
        self.assertIsNotNone(doc_id)
        doc = self.dao.find_one_by_id(doc_id)
        today_dt = doc['today']
        self.assertEqual(today_dt.date(), today)
        self.assertEqual(today_dt.time(), datetime.time.min)

    def test_insert_datetime(self):
        now: datetime.datetime = datetime.datetime.now()
        ms = now.microsecond
        now = now.replace(microsecond=ms - ms % 1000)
        doc = {
            'now': now
        }
        doc_id = self.dao.insert(**doc)
        self.assertIsNotNone(doc_id)
        doc = self.dao.find_one_by_id(doc_id)
        print(doc)
        now_dt = doc['now']
        self.assertEqual(now_dt, now)

    def test_insert_time(self):
        doc = {
            'min_time': datetime.time.min,
            'max_time': datetime.time.max,
        }
        doc_id = self.dao.insert(**doc)
        self.assertIsNotNone(doc_id)
        doc = self.dao.find_one_by_id(doc_id)
        min_t = datetime.time.fromisoformat(doc['min_time'])
        max_t = datetime.time.fromisoformat(doc['max_time'])
        self.assertEqual(min_t, datetime.time.min)
        self.assertEqual(max_t, datetime.time.max)


if __name__ == '__main__':
    unittest.main()
