"""Sorting in Turkish alphabetical order.

Plain sorted() puts 'ç', 'ğ', 'ı', 'ö', 'ş', 'ü' after 'z' (by code point) and
treats 'İ'/'I' wrongly. sort_key() orders words the way a Turkish dictionary does.
"""

from typing import Iterable, List

from .case import lower

ALPHABET = "abcçdefgğhıijklmnoöprsştuüvyz"
_RANK = {ch: i for i, ch in enumerate(ALPHABET)}
# Letters outside the Turkish alphabet sort after their nearest Latin neighbour.
_EXTRA = {"q": "p", "w": "v", "x": "v", "â": "a", "î": "i", "û": "u"}


def _rank(ch: str):
    if ch in _RANK:
        return (1, _RANK[ch] * 4)
    if ch in _EXTRA:
        return (1, _RANK[_EXTRA[ch]] * 4 + 1)
    if ch.isdigit():
        return (0, ord(ch))
    if ch.isalpha():
        return (2, ord(ch))
    return (-1, ord(ch))


def sort_key(text: str):
    """Key for sorted(): sorted(words, key=sort_key)."""
    folded = lower(text)
    # Primary: letters by Turkish rank. Tie-break: lower case before upper case.
    return (tuple(_rank(c) for c in folded), tuple(c != l for c, l in zip(text, folded)))


def sorted_tr(items: Iterable[str], reverse: bool = False) -> List[str]:
    """Return items sorted in Turkish alphabetical order."""
    return sorted(items, key=sort_key, reverse=reverse)
