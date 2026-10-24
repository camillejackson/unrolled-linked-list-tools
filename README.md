# unrolled-linked-list-tools

A small, zero-dependency Python implementation of an unrolled linked list: a linked sequence of fixed-capacity node arrays that improves cache locality over a plain singly-linked list while still supporting O(1) amortized appends.

```python
from unrolled_linked_list_tools import UnrolledLinkedList

lst = UnrolledLinkedList(node_capacity=8)
lst.append("a")
lst.append("b")
lst.prepend("z")
print(list(lst))   # ['z', 'a', 'b']
print(lst[0])      # 'z'
print(lst.pop())   # 'b'
```

## Why

A standard linked list allocates one node per element, which is wasteful and cache-unfriendly for sequential work. An unrolled list packs several elements into each node so a single pointer hop yields a run of contiguous data. The trade-off is that per-element access becomes a two-level search (walk nodes, then index within a block), and the API here deliberately stays small: append, prepend, pop, index, and iteration. No slice assignment, no in-place mutation beyond the ends. Keeping the surface narrow means the behaviour is easy to reason about and test.

## Edge cases worth knowing

`node_capacity` must be at least 1; smaller values raise `ValueError`. `pop()` on an empty list raises `IndexError`. When `pop()` empties a tail node, that node is detached so subsequent iteration does not walk dead nodes — but `prepend()` onto a full head always allocates a new head rather than stealing capacity from the second node. This keeps prepend O(1) and avoids shuffling elements between nodes.

## Layout

- `src/unrolled_linked_list_tools/__init__.py` — re-exports `UnrolledLinkedList`.
- `src/unrolled_linked_list_tools/core.py` — the implementation.
- `tests/test_core.py` — `unittest` suite; run with `PYTHONPATH=src python -m unittest discover -s tests`.
