"""Case conversion that gets the dotted/dotless I right.

Python's str.lower()/str.upper() follow locale-independent Unicode rules, so
"I".lower() gives "i" (should be "ı") and "i".upper() gives "I" (should be "İ"),
and "İ".lower() gives "i̇" (i + combining dot). These helpers fix that.
"""

_TO_LOWER = str.maketrans({"I": "ı", "İ": "i"})
_TO_UPPER = str.maketrans({"i": "İ", "ı": "I"})


def lower(text: str) -> str:
    """Turkish lower case: 'IŞIK İZMİR' -> 'ışık izmir'."""
    return text.translate(_TO_LOWER).lower()


def upper(text: str) -> str:
    """Turkish upper case: 'istanbul ılık' -> 'İSTANBUL ILIK'."""
    return text.translate(_TO_UPPER).upper()


def capitalize(word: str) -> str:
    """Upper-case the first letter, lower-case the rest (Turkish rules)."""
    if not word:
        return word
    return upper(word[0]) + lower(word[1:])


def title(text: str) -> str:
    """Title-case every word: 'iyi günler izmir' -> 'İyi Günler İzmir'.

    Words are split on whitespace and hyphens; apostrophe suffixes stay lower
    case ("İZMİR'DE" -> "İzmir'de").
    """
    out = []
    start = True
    for ch in text:
        if ch.isspace() or ch in "-/(":
            out.append(ch)
            start = True
        elif start and ch.isalpha():
            out.append(upper(ch))
            start = False
        else:
            out.append(lower(ch))
            if ch.isalnum():
                start = False
    return "".join(out)


def casefold(text: str) -> str:
    """Caseless-matching key using Turkish rules."""
    return lower(text)


def equals_ignore_case(a: str, b: str) -> bool:
    """Compare two strings case-insensitively with Turkish rules."""
    return casefold(a) == casefold(b)
