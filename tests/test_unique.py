import unittest

from hashed_list import DuplicateValueError, HashedList


class TestUnique(unittest.TestCase):
    """Assert that HashedArray supports only unique values"""

    def test_not_unique(self):
        # HashedList only support unique items
        with self.assertRaises(DuplicateValueError) as context:
            HashedList([1, 2, 3, 3])
        self.assertEqual(context.exception.args, ("Duplicate values in HashedList",))

    def test_setitem__duplicate(self):
        ls = [1, 10, 22, -1]
        harray = HashedList(ls)

        with self.assertRaises(DuplicateValueError) as context:
            harray[0] = 10
        self.assertEqual(context.exception.args, ("Duplicate values in HashedList",))

    def test_append__duplicate(self):
        harray = HashedList(["a", "b", "c"])

        with self.assertRaises(DuplicateValueError) as context:
            harray.append("a")
        self.assertEqual(context.exception.args, ("Duplicate values in HashedList",))

    def test_extend__duplicate(self):
        harray = HashedList(["a", "5", "-1"])

        with self.assertRaises(DuplicateValueError) as context:
            harray.extend(["1", "5"])
        self.assertEqual(context.exception.args, ("Duplicate values in HashedList",))

    def test_insert__duplicate(self):
        harray = HashedList([1, 2, 10])
        with self.assertRaises(DuplicateValueError) as context:
            harray.insert(0, 2)
        self.assertEqual(context.exception.args, ("Duplicate values in HashedList",))
