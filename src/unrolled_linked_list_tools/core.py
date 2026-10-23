from __future__ import annotations

from collections.abc import Iterator


class _Node:
    """A single link in the unrolled list.

    Stores up to ``capacity`` elements in a Python ``list`` to improve cache
    locality versus a singly-linked list of one element per node. ``slots`` is
    unnecessary here since each node owns a list of references; the list object
    itself dominates memory, so per-node attribute overhead is negligible and
    readability wins.
    """

    __slots__ = ("capacity", "elements", "next")

    def __init__(self, capacity: int, next: _Node | None = None) -> None:
        self.capacity = capacity
        self.elements: list[object] = []
        self.next = next

    def is_full(self) -> bool:
        return len(self.elements) >= self.capacity


class UnrolledLinkedList:
    """An unrolled (linked-block) list.

    Elements are stored in fixed-capacity nodes linked in a chain. Compared to a
    plain linked list, more elements fit per allocation, improving locality for
    sequential iteration. Compared to a flat ``list``, insertion at the front
    or middle does not shift the entire tail.

    Interpretation decisions (see README):
      * The list is **not** mutable in place beyond :meth:`append`,
        :meth:`prepend`, and :meth:`pop`. Deliberately simple surface.
      * Node capacity is fixed at construction; auto-resize is out of scope.
      * Iteration yields every stored element in order.
    """

    def __init__(self, node_capacity: int = 16) -> None:
        if node_capacity < 1:
            raise ValueError("node_capacity must be >= 1")
        self._node_capacity = node_capacity
        self._head: _Node | None = None
        self._tail: _Node | None = None
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[object]:
        node = self._head
        while node is not None:
            for item in node.elements:
                yield item
            node = node.next

    def __getitem__(self, index: int) -> object:
        size = self._size
        if index < 0:
            index += size
        if index < 0 or index >= size:
            raise IndexError(index)
        node = self._head
        seen = 0
        while node is not None:
            block_len = len(node.elements)
            if index < seen + block_len:
                return node.elements[index - seen]
            seen += block_len
            node = node.next
        # Unreachable given the bounds check above; defensive only.
        raise IndexError(index)

    def append(self, item: object) -> None:
        """Add ``item`` to the end in O(1) amortized time."""
        if self._tail is None or self._tail.is_full():
            node = _Node(self._node_capacity)
            if self._tail is None:
                self._head = node
                self._tail = node
            else:
                self._tail.next = node
                self._tail = node
        self._tail.elements.append(item)
        self._size += 1

    def prepend(self, item: object) -> None:
        """Add ``item`` to the front in O(1) when the head has room.

        If the head is full, a new head node is allocated. This keeps the
        prepend path simple and avoids shuffling elements between nodes.
        """
        if self._head is None:
            node = _Node(self._node_capacity)
            self._head = node
            self._tail = node
        elif self._head.is_full():
            node = _Node(self._node_capacity, next=self._head)
            self._head = node
        self._head.elements.insert(0, item)
        self._size += 1

    def pop(self) -> object:
        """Remove and return the last element.

        Empty-list tail nodes are removed after draining so iteration does not
        walk dead nodes. Raises :class:`IndexError` on an empty list.
        """
        if self._tail is None:
            raise IndexError("pop from empty list")
        item = self._tail.elements.pop()
        self._size -= 1
        if not self._tail.elements:
            self._remove_tail_node()
        return item

    def _remove_tail_node(self) -> None:
        if self._head is self._tail:
            self._head = None
            self._tail = None
            return
        node = self._head
        assert node is not None
        while node.next is not self._tail:
            assert node.next is not None
            node = node.next
        node.next = None
        self._tail = node
