import unittest

from unrolled_linked_list_tools import UnrolledLinkedList


class TestConstruction(unittest.TestCase):
    def test_empty(self):
        lst = UnrolledLinkedList()
        self.assertEqual(len(lst), 0)
        self.assertEqual(list(lst), [])

    def test_default_capacity_is_positive(self):
        lst = UnrolledLinkedList()
        lst.append(1)
        self.assertEqual(list(lst), [1])

    def test_invalid_capacity_raises(self):
        with self.assertRaises(ValueError):
            UnrolledLinkedList(0)

    def test_invalid_negative_capacity_raises(self):
        with self.assertRaises(ValueError):
            UnrolledLinkedList(-3)

    def test_capacity_one_supports_single_element_per_node(self):
        lst = UnrolledLinkedList(node_capacity=1)
        for i in range(4):
            lst.append(i)
        self.assertEqual(list(lst), [0, 1, 2, 3])


class TestAppend(unittest.TestCase):
    def test_append_grows_size(self):
        lst = UnrolledLinkedList(node_capacity=3)
        for i in range(7):
            lst.append(i)
        self.assertEqual(len(lst), 7)

    def test_append_preserves_order_across_nodes(self):
        lst = UnrolledLinkedList(node_capacity=3)
        for i in range(10):
            lst.append(i)
        self.assertEqual(list(lst), list(range(10)))

    def test_append_after_prepend_keeps_both_visible(self):
        lst = UnrolledLinkedList(node_capacity=3)
        lst.append(10)
        lst.prepend(5)
        lst.append(15)
        self.assertEqual(list(lst), [5, 10, 15])


class TestPrepend(unittest.TestCase):
    def test_prepend_to_empty_list(self):
        lst = UnrolledLinkedList(node_capacity=2)
        lst.prepend("a")
        self.assertEqual(list(lst), ["a"])

    def test_prepend_allocates_new_head_when_full(self):
        lst = UnrolledLinkedList(node_capacity=2)
        lst.append(1)
        lst.append(2)
        lst.prepend(0)
        self.assertEqual(list(lst), [0, 1, 2])

    def test_repeated_prepend_reverse_insertion(self):
        lst = UnrolledLinkedList(node_capacity=2)
        for i in range(5):
            lst.prepend(i)
        self.assertEqual(list(lst), [4, 3, 2, 1, 0])


class TestGetitem(unittest.TestCase):
    def test_positive_index_within_bounds(self):
        lst = UnrolledLinkedList(node_capacity=3)
        for i in range(8):
            lst.append(i)
        for i in range(8):
            self.assertEqual(lst[i], i)

    def test_negative_index_counts_from_end(self):
        lst = UnrolledLinkedList(node_capacity=3)
        for i in range(6):
            lst.append(i)
        self.assertEqual(lst[-1], 5)
        self.assertEqual(lst[-6], 0)

    def test_index_out_of_range_positive_raises(self):
        lst = UnrolledLinkedList(node_capacity=3)
        lst.append(1)
        with self.assertRaises(IndexError):
            _ = lst[1]

    def test_index_out_of_range_negative_raises(self):
        lst = UnrolledLinkedList(node_capacity=3)
        lst.append(1)
        with self.assertRaises(IndexError):
            _ = lst[-2]

    def test_index_on_empty_list_raises(self):
        lst = UnrolledLinkedList()
        with self.assertRaises(IndexError):
            _ = lst[0]


class TestPop(unittest.TestCase):
    def test_pop_returns_last_appended(self):
        lst = UnrolledLinkedList(node_capacity=3)
        lst.append(1)
        lst.append(2)
        self.assertEqual(lst.pop(), 2)
        self.assertEqual(list(lst), [1])

    def test_pop_drains_to_empty(self):
        lst = UnrolledLinkedList(node_capacity=2)
        for i in range(4):
            lst.append(i)
        order = [lst.pop() for _ in range(4)]
        self.assertEqual(order, [3, 2, 1, 0])
        self.assertEqual(len(lst), 0)
        self.assertEqual(list(lst), [])

    def test_pop_on_empty_raises_index_error(self):
        lst = UnrolledLinkedList(node_capacity=2)
        with self.assertRaises(IndexError):
            lst.pop()

    def test_pop_then_append_reuses_structure(self):
        lst = UnrolledLinkedList(node_capacity=2)
        lst.append(1)
        lst.append(2)
        self.assertEqual(lst.pop(), 2)
        lst.append(3)
        self.assertEqual(list(lst), [1, 3])


class TestIteration(unittest.TestCase):
    def test_iter_empty(self):
        lst = UnrolledLinkedList()
        self.assertEqual(list(lst), [])

    def test_iter_after_partial_pop(self):
        lst = UnrolledLinkedList(node_capacity=3)
        for i in range(6):
            lst.append(i)
        lst.pop()
        lst.pop()
        self.assertEqual(list(lst), [0, 1, 2, 3])

    def test_iter_does_not_mutate(self):
        lst = UnrolledLinkedList(node_capacity=2)
        for i in range(5):
            lst.append(i)
        _ = list(lst)
        self.assertEqual(len(lst), 5)


if __name__ == "__main__":
    unittest.main()
