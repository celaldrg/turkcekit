"""ASCII folding and URL slugs for Turkish text."""

import re
import unicodedata

_FOLD = str.maketrans({
    "ç": "c", "Ç": "C", "ğ": "g", "Ğ": "G", "ı": "i", "İ": "I",
    "ö": "o", "Ö": "O", "ş": "s", "Ş": "S", "ü": "u", "Ü": "U",
    "â": "a", "Â": "A", "î": "i", "Î": "I", "û": "u", "Û": "U",
})


def asciify(text: str) -> str:
    """Replace Turkish letters with ASCII ones: 'Çığ Şöförü' -> 'Cig Soforu'.

    Other accented Latin letters are stripped of their marks; characters with
    no ASCII form are dropped.
    """
    text = unicodedata.normalize("NFC", text).translate(_FOLD)
    decomposed = unicodedata.normalize("NFKD", text)
    return "".join(c for c in decomposed if not unicodedata.combining(c)).encode(
        "ascii", "ignore").decode("ascii")


def slugify(text: str, sep: str = "-", max_length: int = 0) -> str:
    """URL-safe slug: 'Ağaç Ev & Bahçe Fiyatları 2026' -> 'agac-ev-bahce-fiyatlari-2026'."""
    from .case import lower

    s = asciify(lower(text)).lower()
    s = s.replace("'", "").replace("\u2019", "")
    s = re.sub(r"[^a-z0-9]+", sep, s).strip(sep)
    if max_length and len(s) > max_length:
        cut = s[:max_length]
        if s[max_length] != sep and sep in cut:
            cut = cut.rsplit(sep, 1)[0]
        s = cut.strip(sep)
    return s
