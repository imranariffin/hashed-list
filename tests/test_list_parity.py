from typing import List
import unittest

from hashed_list import HashedList


class TestListParity(unittest.TestCase):
    """Assert that HashedArray is in feature parity with builtin list"""

    def test_index(self):
        harray = HashedList(list(range(10)))
        index = harray.index(9)
        self.assertEqual(index, 9)

    def test_index__with_start(self):
        ls: List[str] = ["10", "3", "5"]
        harray: HashedList[str] = HashedList(ls)

        self.assertEqual(harray.index("10", start=0), ls.index("10", 0))
        self.assertEqual(harray.index("3", start=1), ls.index("3", 1))
        self.assertEqual(harray.index("5", start=2), ls.index("5", 2))
        with self.assertRaises(ValueError) as context_harray:
            harray.index("10", start=1)
        with self.assertRaises(ValueError) as context_ls:
            ls.index("10", 1)
        self.assertEqual(context_harray.exception.args, context_ls.exception.args)

    def test_index__with_start_and_end(self):
        ls: List[str] = ["10", "3", "5"]
        harray: HashedList[str] = HashedList(ls)

        self.assertEqual(harray.index("10", start=0, end=3), ls.index("10", 0, 3))
        self.assertEqual(harray.index("3", start=1, end=3), ls.index("3", 1, 3))
        self.assertEqual(harray.index("5", start=2, end=3), ls.index("5", 2, 3))
        with self.assertRaises(ValueError) as context_harray:
            harray.index("5", start=0, end=1)
        with self.assertRaises(ValueError) as context_ls:
            ls.index("5", 0, 1)
        self.assertEqual(context_harray.exception.args, context_ls.exception.args)

    def test_empty(self):
        harray = HashedList([])
        try:
            ls = []
            ls.index(1)
        except Exception as e_list:
            try:
                harray.index(1)
            except Exception as e_harray:
                self.assertEqual(e_list.__class__, e_harray.__class__)
                self.assertEqual(e_list.args, e_harray.args)

    def test_lookup(self):
        ls = [1, 10, 22, -1]
        harray = HashedList(ls)

        self.assertEqual(ls[0], harray[0])
        self.assertEqual(ls[2], harray[2])
        self.assertEqual(ls[-1], harray[-1])
        self.assertEqual(ls[2:3], harray[2:3])

    def test_setitem(self):
        ls = [1, 10, 22, -1]
        harray = HashedList(ls)
        ls[0] = 2
        harray[0] = 2
        self.assertEqual(ls[0], harray[0])

        ls = [1, 10, 22, -1]
        harray = HashedList(ls)
        ls[2] = 99
        harray[2] = 99
        self.assertEqual(ls[2], harray[2])

        ls = [1, 10, 22, -1]
        harray = HashedList(ls)
        ls[-1] = -111
        harray[-1] = -111
        self.assertEqual(ls[-1], harray[-1])

        ls = [1, 10, 22, -1]
        harray = HashedList(ls)
        ls[1:3] = [3, 9]
        harray[1:3] = [3, 9]
        self.assertEqual(ls[1:3], harray[1:3])

    def test_append(self):
        ls = ["a", "b", "c"]
        harray = HashedList(ls)

        ls.append("Z")
        harray.append("Z")

        self.assertEqual(ls, harray)
        self.assertEqual(ls.index("Z"), harray.index("Z"))
        self.assertEqual(ls.index("c"), harray.index("c"))
        self.assertEqual(ls.index("b"), harray.index("b"))
        self.assertEqual(ls.index("a"), harray.index("a"))

    def test_extend(self):
        ls = ["a", "b", "c"]
        harray = HashedList(ls)

        ls.extend(["X", "Y", "Z"])
        harray.extend(["X", "Y", "Z"])

        self.assertEqual(ls, harray)
        self.assertEqual(ls.index("Z"), harray.index("Z"))
        self.assertEqual(ls.index("Y"), harray.index("Y"))
        self.assertEqual(ls.index("X"), harray.index("X"))
        self.assertEqual(ls.index("c"), harray.index("c"))
        self.assertEqual(ls.index("b"), harray.index("b"))
        self.assertEqual(ls.index("a"), harray.index("a"))

    def test_insert(self):
        # Insert at the beginning
        ls = ["a", "b", "c"]
        harray = HashedList(ls)
        ls.insert(0, "Z")
        harray.insert(0, "Z")
        self.assertEqual(ls, harray)
        self.assertEqual(ls.index("Z"), harray.index("Z"))
        self.assertEqual(ls.index("c"), harray.index("c"))
        self.assertEqual(ls.index("b"), harray.index("b"))
        self.assertEqual(ls.index("a"), harray.index("a"))

        # Insert into the middle
        ls = ["a", "b", "c"]
        harray = HashedList(ls)
        ls.insert(1, "Z")
        harray.insert(1, "Z")
        self.assertEqual(ls, harray)
        self.assertEqual(ls.index("Z"), harray.index("Z"))
        self.assertEqual(ls.index("c"), harray.index("c"))
        self.assertEqual(ls.index("b"), harray.index("b"))
        self.assertEqual(ls.index("a"), harray.index("a"))

        # Insert into the end
        ls = ["a", "b", "c"]
        harray = HashedList(ls)
        ls.insert(3, "Z")
        harray.insert(3, "Z")
        self.assertEqual(ls, harray)
        self.assertEqual(ls.index("Z"), harray.index("Z"))
        self.assertEqual(ls.index("c"), harray.index("c"))
        self.assertEqual(ls.index("b"), harray.index("b"))
        self.assertEqual(ls.index("a"), harray.index("a"))

    def test_remove(self):
        # Remove from the beginning
        ls = ["a", "b", "c"]
        harray = HashedList(ls)
        ls.remove("a")
        harray.remove("a")
        self.assertEqual(ls, harray)
        self.assertEqual(ls.index("c"), harray.index("c"))
        self.assertEqual(ls.index("b"), harray.index("b"))

        # Remove from the middle
        ls = ["a", "b", "c"]
        harray = HashedList(ls)
        ls.remove("b")
        harray.remove("b")
        self.assertEqual(ls, harray)
        self.assertEqual(ls.index("c"), harray.index("c"))
        self.assertEqual(ls.index("a"), harray.index("a"))

        # Remove from the end
        ls = ["a", "b", "c"]
        harray = HashedList(ls)
        ls.remove("c")
        harray.remove("c")
        self.assertEqual(ls, harray)
        self.assertEqual(ls.index("b"), harray.index("b"))
        self.assertEqual(ls.index("a"), harray.index("a"))

    def test_pop(self):
        # Pop from the beginning
        ls = ["a", "b", "c"]
        harray = HashedList(ls)
        value_ls = ls.pop(0)
        value_harray = harray.pop(0)
        self.assertEqual(ls, harray)
        self.assertEqual(value_ls, value_harray)
        self.assertEqual(ls.index("c"), harray.index("c"))
        self.assertEqual(ls.index("b"), harray.index("b"))

        # Pop from the middle
        ls = ["a", "b", "c"]
        harray = HashedList(ls)
        value_ls = ls.pop(1)
        value_harray = harray.pop(1)
        self.assertEqual(ls, harray)
        self.assertEqual(value_ls, value_harray)
        self.assertEqual(ls.index("c"), harray.index("c"))
        self.assertEqual(ls.index("a"), harray.index("a"))

        # Pop from the end
        ls = ["a", "b", "c"]
        harray = HashedList(ls)
        value_ls = ls.pop()
        value_harray = harray.pop()
        self.assertEqual(ls, harray)
        self.assertEqual(value_ls, value_harray)
        self.assertEqual(ls.index("b"), harray.index("b"))
        self.assertEqual(ls.index("a"), harray.index("a"))

    def test_clear(self):
        ls = ["a", "b", "c"]
        harray = HashedList(ls)

        ls.clear()
        harray.clear()
        self.assertEqual(ls, harray)
        with self.assertRaises(ValueError) as context_ls:
            ls.index("a")
        with self.assertRaises(ValueError) as context_harray:
            harray.index("a")
        self.assertEqual(context_harray.exception.args, context_ls.exception.args)

    def test_count(self):
        ls = ["c", "b"]
        harray = ["c", "b"]
        self.assertEqual(ls.count("c"), harray.count("c"))
        self.assertEqual(ls.count("b"), harray.count("b"))

    def test_sort(self):
        ls = ["c", "b", "1"]
        harray = ["c", "b", "1"]

        ls.sort()
        harray.sort()

        self.assertEqual(ls, harray)
        self.assertEqual(ls.index("1"), harray.index("1"))
        self.assertEqual(ls.index("b"), harray.index("b"))
        self.assertEqual(ls.index("c"), harray.index("c"))

    def test_reverse(self):
        ls = ["b", "c", "1"]
        harray = ["b", "c", "1"]

        ls.reverse()
        harray.reverse()

        self.assertEqual(ls, harray)
        self.assertEqual(ls.index("1"), harray.index("1"))
        self.assertEqual(ls.index("b"), harray.index("b"))
        self.assertEqual(ls.index("c"), harray.index("c"))
