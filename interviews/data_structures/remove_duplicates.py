def remove_duplicates(_list):
    for i in xrange(len(_list)):
        try:
            val = _list[i]
        except IndexError:
            break
        j = 0
        while j < i:
            duplicate = _list[j]
            if val == duplicate:
                del _list[j]
            else:
                j += 1
    return _list

import unittest


class RemoveDuplicateTestCase(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(remove_duplicates([]), [])

    def test_no_duplicates(self):
        self.assertEqual(remove_duplicates([1, 2, 3]), [1, 2, 3])

    def test_duplicates(self):
        self.assertEqual(remove_duplicates([1 ,2, 2, 3, 3, 3]), [1, 2, 3])