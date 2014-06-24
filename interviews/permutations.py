import unittest


def merge(seq, elem):
    all_merges = set()
    elem = tuple(elem)
    for i in xrange(len(seq) + 1):
        all_merges.add(seq[0:i] + elem + seq[i:])
    return all_merges


def all_perms(seq, perms=None):
    perms = perms or set()
    if len(seq) == 1:
        perms.add(tuple(seq))
    elif len(seq) == 2:
        perms.add(tuple(seq))
        perms.add(tuple(reversed(seq)))
    else:
        all_but_last, last = seq[:-1], seq[-1:]
        short_perms = all_perms(all_but_last)
        for p in short_perms:
            merged = merge(p, last)
            perms |= merged
    return perms


class PermutationsTestCase(unittest.TestCase):
    def test_merge(self):
        self.assertEqual(
            merge((1, 2, 3), [9]),
            set([(9, 1, 2, 3), (1, 9, 2, 3), (1, 2, 9, 3), (1, 2, 3, 9)]))

    def test_all_perms_single_elem(self):
        self.assertEqual(all_perms([1]), set([(1,)]))

    def test_all_perms_two_elem(self):
        self.assertEqual(all_perms([1, 2]), set([(1, 2), (2, 1)]))

    def test_general(self):
        expected = set([
            (1, 2, 3, 4), (1, 2, 4, 3), (1, 3, 2, 4), (1, 3, 4, 2),
            (1, 4, 2, 3), (1, 4, 3, 2),
            (2, 1, 3, 4), (2, 1, 4, 3), (2, 3, 1, 4), (2, 3, 4, 1),
            (2, 4, 1, 3), (2, 4, 3, 1),
            (3, 1, 2, 4), (3, 1, 4, 2), (3, 2, 1, 4), (3, 2, 4, 1),
            (3, 4, 2, 1), (3, 4, 1, 2),
            (4, 1, 2, 3), (4, 1, 3, 2), (4, 2, 1, 3), (4, 2, 3, 1),
            (4, 3, 2, 1), (4, 3, 1, 2),
        ])
        self.assertEqual(len(expected), 4 * 3 * 2)
        self.assertEqual(all_perms([1, 2, 3, 4]), expected)