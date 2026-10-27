"""Numbers in Turkish: words ("sayıyı yazıya çevirme") and lira formatting."""

from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from typing import Union

Number = Union[int, float, str, Decimal]

_ONES = ["", "bir", "iki", "üç", "dört", "beş", "altı", "yedi", "sekiz", "dokuz"]
_TENS = ["", "on", "yirmi", "otuz", "kırk", "elli", "altmış", "yetmiş", "seksen", "doksan"]
_SCALES = ["", "bin", "milyon", "milyar", "trilyon", "katrilyon", "kentilyon",
           "sekstilyon", "septilyon", "oktilyon", "nonilyon", "desilyon"]


def _below_thousand(n: int) -> list:
    words = []
    h, rest = divmod(n, 100)
    if h:
        if h > 1:
            words.append(_ONES[h])
        words.append("yüz")
    t, o = divmod(rest, 10)
    if t:
        words.append(_TENS[t])
    if o:
        words.append(_ONES[o])
    return words


def number_to_words(n: int, sep: str = " ") -> str:
    """1234 -> 'bin iki yüz otuz dört'; -1000000 -> 'eksi bir milyon'.

    Follows Turkish usage: 100 is 'yüz' (not 'bir yüz'), 1000 is 'bin'
    (not 'bir bin'), but 1000000 is 'bir milyon'.
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("number_to_words expects an int")
    if n == 0:
        return "sıfır"
    if n < 0:
        return "eksi" + sep + number_to_words(-n, sep)
    groups = []
    while n:
        n, g = divmod(n, 1000)
        groups.append(g)
    if len(groups) > len(_SCALES):
        raise ValueError("number too large")
    words = []
    for i in range(len(groups) - 1, -1, -1):
        g = groups[i]
        if not g:
            continue
        if i == 1 and g == 1:
            words.append("bin")
            continue
        words.extend(_below_thousand(g))
        if _SCALES[i]:
            words.append(_SCALES[i])
    return sep.join(words)


def _to_decimal(value: Number) -> Decimal:
    if isinstance(value, float):
        value = repr(value)
    try:
        return Decimal(value)
    except InvalidOperation:
        raise ValueError(f"not a number: {value!r}") from None


def amount_to_words(value: Number, currency: str = "Türk lirası",
                    subunit: str = "kuruş", sep: str = " ") -> str:
    """Amount in words for invoices and cheques.

    amount_to_words("1250.75") -> 'bin iki yüz elli Türk lirası yetmiş beş kuruş'
    Use sep="" for the joined style printed on cheques ('BinİkiYüzElli...').
    """
    d = _to_decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    negative = d < 0
    d = abs(d)
    lira = int(d)
    kurus = int((d - lira) * 100)
    parts = []
    if lira or not kurus:
        parts.append(number_to_words(lira, sep) + sep + currency.replace(" ", sep))
    if kurus:
        parts.append(number_to_words(kurus, sep) + sep + subunit)
    text = sep.join(parts)
    return ("eksi" + sep + text) if negative else text


def format_tl(value: Number, symbol: str = "₺", decimals: int = 2,
              symbol_first: bool = False) -> str:
    """Format money the Turkish way: 1234567.5 -> '1.234.567,50 ₺'."""
    q = Decimal(1).scaleb(-decimals) if decimals else Decimal(1)
    d = _to_decimal(value).quantize(q, rounding=ROUND_HALF_UP)
    sign = "-" if d < 0 else ""
    whole, _, frac = f"{abs(d):f}".partition(".")
    groups = []
    while len(whole) > 3:
        groups.insert(0, whole[-3:])
        whole = whole[:-3]
    groups.insert(0, whole)
    number = ".".join(groups) + ("," + frac if decimals else "")
    if not symbol:
        return sign + number
    return f"{sign}{symbol}{number}" if symbol_first else f"{sign}{number} {symbol}"


def parse_tl(text: str) -> Decimal:
    """Parse a Turkish-formatted amount: '₺1.234,50' or '1.234,50 TL' -> Decimal('1234.50')."""
    s = text.strip()
    for token in ("₺", "TRY", "TL", "tl"):
        s = s.replace(token, "")
    s = s.replace(" ", "").replace("\u00a0", "")
    negative = s.startswith("-")
    s = s.lstrip("-+")
    if not s:
        raise ValueError(f"not an amount: {text!r}")
    s = s.replace(".", "").replace(",", ".")
    d = _to_decimal(s)
    return -d if negative else d
