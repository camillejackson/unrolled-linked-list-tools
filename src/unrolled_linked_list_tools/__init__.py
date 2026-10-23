"""Unrolled linked list tools.

Exposes :class:`UnrolledLinkedList` and :exc:`IndexError`-based access for
sequences that benefit from packing multiple elements per linked node.
"""

from .core import UnrolledLinkedList

__all__ = ["UnrolledLinkedList"]
