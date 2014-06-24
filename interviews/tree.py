class BinaryNode(object):
    def __init__(self, value):
        self.value = value
        self._left, self._right = None, None

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    def add_left(self, value):
        self._left = value

    def add_right(self, value):
        self._right = value

    def __str__(self):
        return '{0} ({1}, {2})'.format(self.value, self.left, self.right)


def create_tree():
    root = BinaryNode('F')
    B = BinaryNode('B')
    root.add_left(B)
    B.add_left(BinaryNode('A'))
    D = BinaryNode('D')
    B.add_right(D)
    D.add_left(BinaryNode('C'))
    D.add_right(BinaryNode('E'))
    G = BinaryNode('G')
    root.add_right(G)
    I = BinaryNode('I')
    G.add_right(I)
    I.add_left(BinaryNode('H'))
    return root


def pre_order(node, traversed):
    traversed.append(node.value)
    if node.left is not None:
        pre_order(node.left, traversed)
    if node.right is not None:
        pre_order(node.right, traversed)
    return traversed


def in_order(node, traversed):
    if node.left is not None:
        in_order(node.left, traversed)
    traversed.append(node.value)
    if node.right is not None:
        in_order(node.right, traversed)
    return traversed


def post_order(node, traversed):
    if node.left is not None:
        post_order(node.left, traversed)
    if node.right is not None:
        post_order(node.right, traversed)
    traversed.append(node.value)
    return traversed

import unittest


class TreeTraversal(unittest.TestCase):
    def test_pre_order(self):
        root = create_tree()
        self.assertEqual(pre_order(root, []), ['F', 'B', 'A', 'D', 'C', 'E', 'G', 'I', 'H'])

    def test_in_order(self):
        root = create_tree()
        self.assertEqual(in_order(root, []), ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'])

    def test_post_order(self):
        root = create_tree()
        self.assertEqual(post_order(root, []), ['A', 'C', 'E', 'D', 'B', 'H', 'I', 'G', 'F'])

