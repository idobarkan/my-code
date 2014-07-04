import heapq
import unittest


class MinHeapQ(object):
    def __init__(self, _list=[]):
        heapq.heapify(list(_list))
        self._h = _list

    def push(self, item):
        heapq.heappush(self._h, item)

    def pop(self):
        return heapq.heappop(self._h)

    def pushpop(self, item):
        return heapq.heappushpop(self._h, item)

    def replace(self, item):
        return heapq.heapreplace(self._h, item)

    def pick(self):
        return self._h[0]

    def empty(self):
        return len(self._h) == 0

    def __len__(self):
        return len(self._h)
    
    
class Backwards(int):
    def __lt__(self, other):
        return not int.__le__(other)
    
    def __le__(self, other):
        return not int.__lt__(other)
    
    def __gt__(self, other):
        return not int.__ge__(other)
    
    def __ge__(self, other):
        return not int.__gt__(other)


class MaxHeapQ(MinHeapQ):
    def __init__(self, _list=[]):
        if not _list:
            backwards_list = []
        else:
            backwards_list = list(Backwards(x) for x in _list)

        super(MaxHeapQ, self).__init__(backwards_list)

    def push(self, item):
        heapq.heappush(self._h, Backwards(item))

    def pop(self):
        return super(MaxHeapQ, self).pop()

    def pushpop(self, item):
        return super(MaxHeapQ, self).pushpop(self._h, Backwards(item))

    def replace(self, item):
        return heapq.heapreplace(self._h, Backwards(item))


class MedianTracker(list):
    def __init__(self):
        super(MedianTracker, self).__init__()
        self._max_heap = MaxHeapQ()
        self._min_heap = MinHeapQ()
        self._even = True

    def append(self, _int):
        if self._min_heap.empty():
            self._min_heap.push(_int)
        elif _int < self._min_heap.pick():
            self._min_heap.push(_int)
        else:
            self._max_heap.push(_int)
        self._even = not self._even

    @property
    def len_max(self):
        return len(self._max_heap)

    @property
    def len_min(self):
        return len(self._min_heap)

    def _balance_even_quantity(self):
        if self.len_max > self.len_min:
            while self.len_max > self.len_min:
                self._min_heap.push(self._max_heap.pop())
        else:
            while self.len_max < self.len_min:
                self._max_heap.push(self._min_heap.pop())

    def median(self):
        if self._even:
            self._balance_even_quantity()
            return (self._max_heap.pick() + self._min_heap.pick()) / 2
        else:
            if self.len_max > self.len_min:
                while self.len_max - 1 > self.len_min:
                    self._min_heap.push(self._max_heap.pop())
                return self._max_heap.pick()
            else:
                while self.len_max < self.len_min - 1:
                    self._max_heap.push(self._min_heap.pop())
                return self._min_heap.pick()


class MedianTrackerTestCase(unittest.TestCase):
    def test_median_even(self):
        l = range(5)
        tracker = MedianTracker()
        for i in l:
            tracker.append(i)
        self.assertEqual(tracker.median(), 2)