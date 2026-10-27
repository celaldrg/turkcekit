"""turkcekit: Turkish-aware text utilities with zero dependencies."""

from .case import lower, upper, title, capitalize, casefold, equals_ignore_case
from .ascii import asciify, slugify
from .collate import sort_key, sorted_tr, ALPHABET
from .numbers import number_to_words, amount_to_words, format_tl, parse_tl

__all__ = [
    "lower", "upper", "title", "capitalize", "casefold", "equals_ignore_case",
    "asciify", "slugify", "sort_key", "sorted_tr", "ALPHABET",
    "number_to_words", "amount_to_words", "format_tl", "parse_tl",
]
__version__ = "0.1.0"
