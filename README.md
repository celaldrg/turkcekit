# turkcekit

**Turkish text done right in Python.** Correct `İ/ı` casing, URL slugs, Turkish alphabetical sorting, numbers and lira amounts in words, and `1.234,50 ₺` formatting. Zero dependencies, one small package, plus a CLI.

[![CI](https://github.com/celaldrg/turkcekit/actions/workflows/ci.yml/badge.svg)](https://github.com/celaldrg/turkcekit/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License: MIT](https://img.shields.io/badge/license-MIT-green)

## Why

Python's built-in string methods don't know Turkish:

```python
>>> "DİYARBAKIR".lower()
'di̇yarbakir'          # 'İ' becomes i + a stray combining dot, 'I' becomes 'i'
>>> "istanbul".upper()
'ISTANBUL'            # should be 'İSTANBUL'
>>> sorted(["zeytin", "çay", "ırmak", "irmik", "ördek", "ozan"])
['irmik', 'ozan', 'zeytin', 'çay', 'ördek', 'ırmak']   # ç, ö, ı land after z
```

Every Turkish project ends up re-writing the same helpers. `turkcekit` is that set of helpers, tested.

## Install

```bash
pip install git+https://github.com/celaldrg/turkcekit
```

## Python usage

```python
import turkcekit as tk

tk.lower("IŞIK İZMİR")                 # 'ışık izmir'
tk.upper("istanbul ılık")              # 'İSTANBUL ILIK'
tk.title("İZMİR'DE ılık HAVA")         # "İzmir'de Ilık Hava"
tk.equals_ignore_case("KIRIK", "kırık")   # True  (and "kirik" is False)

tk.asciify("Çığ Şoförü Ömür Ünal")     # 'Cig Soforu Omur Unal'
tk.slugify("Ağaç Ev & Bahçe Fiyatları 2026")   # 'agac-ev-bahce-fiyatlari-2026'

tk.sorted_tr(["zeytin", "çay", "ırmak", "irmik", "ördek", "ozan"])
# ['çay', 'ırmak', 'irmik', 'ozan', 'ördek', 'zeytin']
sorted(names, key=tk.sort_key)         # works anywhere a key= is accepted

tk.number_to_words(1234)               # 'bin iki yüz otuz dört'
tk.number_to_words(2_500_000_000)      # 'iki milyar beş yüz milyon'
tk.amount_to_words("1250.75")          # 'bin iki yüz elli Türk lirası yetmiş beş kuruş'

tk.format_tl(1234567.5)                # '1.234.567,50 ₺'
tk.format_tl(1000, symbol_first=True)  # '₺1.000,00'
tk.parse_tl("1.234,50 TL")             # Decimal('1234.50')
```

Number words follow real usage: `100` is *yüz* (not *bir yüz*), `1000` is *bin* (not *bir bin*), but `1 000 000` is *bir milyon*. Amounts use `Decimal` and round half-up to the kuruş, so `1.005` really is *bir Türk lirası bir kuruş*.

## CLI

Every command takes text as arguments or reads lines from stdin. This is real output:

```console
$ turkcekit upper iyi akşamlar diyarbakır
İYİ AKŞAMLAR DİYARBAKIR
$ turkcekit title "İZMİR'DE ılık bir gün"
İzmir'de Ilık Bir Gün
$ turkcekit slug "Ağaç Ev & Bahçe Fiyatları 2026"
agac-ev-bahce-fiyatlari-2026
$ turkcekit yazi 1250,75
bin iki yüz elli Türk lirası yetmiş beş kuruş
$ turkcekit yazi --bitisik 1250
BinİkiYüzElli
$ turkcekit tl 1234567.5
1.234.567,50 ₺
$ turkcekit sort < words.txt
çay
ırmak
irmik
ozan
ördek
zeytin
```

Commands: `lower`, `upper`, `title`, `ascii`, `slug`, `sort [-r]`, `yazi [--para] [--bitisik]`, `tl`.

## API

| Function | What it does |
| --- | --- |
| `lower`, `upper`, `capitalize`, `title` | Case conversion with Turkish `I/ı` and `İ/i` rules |
| `casefold`, `equals_ignore_case` | Caseless matching keys and comparison |
| `asciify(text)` | Fold `çğıöşü` (and `âîû`) to ASCII |
| `slugify(text, sep="-", max_length=0)` | URL slug; trims on word boundaries |
| `sort_key`, `sorted_tr`, `ALPHABET` | Turkish dictionary order (`a b c ç d … ş t u ü v y z`) |
| `number_to_words(n, sep=" ")` | Integer to Turkish words, up to *desilyon*, negatives as *eksi* |
| `amount_to_words(value, currency, subunit)` | Lira and kuruş in words, for invoices and cheques |
| `format_tl(value, symbol="₺", decimals=2)` | `1.234,50 ₺` style formatting |
| `parse_tl(text)` | Parse `₺1.234,50`, `1.234,50 TL` into `Decimal` |

## Development

```bash
pip install pytest
python -m pytest
```

## License

MIT © Celalettin Durğaç
