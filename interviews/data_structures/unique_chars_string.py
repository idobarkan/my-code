def is_all_chars_unique(string):
    chars = set()
    for c in string:
        if c in chars:
            return False
        else:
            chars.add(c)
    return True


def is_all_chars_unique2(string):
    for i in xrange(len(string)):
        c = string[i]
        for j in xrange(i):
            if c == string[j]:
                return False
    return True


import unittest


class UniqueCharsTestCase(unittest.TestCase):
    def test_unique_chars(self):
        self.assertTrue(is_all_chars_unique('abc'))

    def test_non_unique_chars(self):
        self.assertFalse(is_all_chars_unique('aabc'))

    def test_empty(self):
        self.assertTrue(is_all_chars_unique(''))


class UniqueCharsTestCase2(unittest.TestCase):
    def test_unique_chars(self):
        self.assertTrue(is_all_chars_unique2('abc'))

    def test_non_unique_chars(self):
        self.assertFalse(is_all_chars_unique2('aabc'))

    def test_empty(self):
        self.assertTrue(is_all_chars_unique2(''))