import unittest
from tests.persistence_testcase import PersistenceTestCase


class CollectionPersistenceTestCase(PersistenceTestCase):

    def test_insert_list(self):
        letters = ['A', 'B', 'C', 'D']
        doc = {
            'letters': letters
        }
        doc_id = self.dao.insert(**doc)
        self.assertIsNotNone(doc_id)
        doc = self.dao.find_one_by_id(doc_id)
        letter_list = doc['letters']
        self.assertEqual(len(letter_list), 4)
        self.assertEqual(letter_list[3], 'D')


if __name__ == '__main__':
    unittest.main()
