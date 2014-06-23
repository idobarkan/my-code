def q_sort_all(array):
    q_sort(array, 0, len(array) - 1)


def q_sort(array, i, k):
    if i < k:
        pivot = partition(array, i, k)
        q_sort(array, i, pivot-1)
        q_sort(array, pivot+1, k)


def partition(array, left, right):
    pivot_index = choose_pivot(left, right)
    pivot_value = array[pivot_index]
    array[pivot_index], array[right] = array[right], array[pivot_index]
    store_index = left

    for i in xrange(left, right):
        if array[i] <= pivot_value:
            array[i], array[store_index] = array[store_index], array[i]
            store_index += 1

    array[store_index], array[right] = array[right], array[store_index]
    return store_index


def choose_pivot(left, right):
    return (left + right) / 2


import unittest


class QuicksortTestcase(unittest.TestCase):
    def test_choose_pivot(self):
        self.assertEqual(choose_pivot(4, 2), 3)
        self.assertEqual(choose_pivot(4, 4), 4)
        self.assertEqual(choose_pivot(4, 1), 2)

    def test_quick_sort_already_sorted(self):
        a = range(5)
        q_sort_all(a)
        self.assertEqual(a, range(5))

    def test_quick_sort_duplicates(self):
        a = [1, 1, 3]
        q_sort_all(a)
        self.assertEqual(a, [1, 1, 3])

    def test_quick_sort_reversed(self):
        a = [6, 5, 4, 3, 2, 1]
        q_sort_all(a)
        self.assertEqual(a, sorted(a))

    def test_quick_sort_shuffled(self):
        a = [3, 10, 19, 13, 2, 8, 6, 15, 11, 0, 7, 18, 16, 1, 14, 9, 12, 5, 4, 17]
        q_sort_all(a)
        self.assertEqual(a, sorted(a))