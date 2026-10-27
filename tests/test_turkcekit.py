from decimal import Decimal

import pytest

import turkcekit as tk
from turkcekit.cli import main


def test_lower_upper():
    assert tk.lower("IŞIK İZMİR") == "ışık izmir"
    assert tk.upper("istanbul ılık") == "İSTANBUL ILIK"
    assert tk.lower("İ") == "i" and len(tk.lower("İ")) == 1
    assert tk.upper(tk.lower("DİYARBAKIR")) == "DİYARBAKIR"


def test_title_and_capitalize():
    assert tk.title("iyi günler izmir") == "İyi Günler İzmir"
    assert tk.title("İZMİR'DE ılık HAVA") == "İzmir'de Ilık Hava"
    assert tk.capitalize("iSTANBUL") == "İstanbul"
    assert tk.capitalize("") == ""


def test_equals_ignore_case():
    assert tk.equals_ignore_case("KIRIK", "kırık")
    assert not tk.equals_ignore_case("KIRIK", "kirik")


def test_asciify_and_slugify():
    assert tk.asciify("Çığ Şoförü Ömür Ünal") == "Cig Soforu Omur Unal"
    assert tk.asciify("kâğıt") == "kagit"
    assert tk.slugify("Ağaç Ev & Bahçe Fiyatları 2026") == "agac-ev-bahce-fiyatlari-2026"
    assert tk.slugify("İSTANBUL'UN EN İYİ KEBABI") == "istanbulun-en-iyi-kebabi"
    assert tk.slugify("  --  ") == ""
    assert tk.slugify("çok uzun bir başlık", max_length=10) == "cok-uzun"
    assert tk.slugify("a b", sep="_") == "a_b"


def test_sorting():
    words = ["şeker", "zeytin", "çay", "ılık", "irmik", "can", "ördek", "ozan", "ütü", "uçak", "ğ", "gaz"]
    assert tk.sorted_tr(words) == ["can", "çay", "gaz", "ğ", "ılık", "irmik",
                                   "ozan", "ördek", "şeker", "uçak", "ütü", "zeytin"]
    assert tk.sorted_tr(["İzmir", "Iğdır", "Hatay"]) == ["Hatay", "Iğdır", "İzmir"]
    assert tk.sorted_tr(["b", "a"], reverse=True) == ["b", "a"]


@pytest.mark.parametrize("n,words", [
    (0, "sıfır"), (7, "yedi"), (10, "on"), (19, "on dokuz"), (100, "yüz"),
    (101, "yüz bir"), (342, "üç yüz kırk iki"), (1000, "bin"), (1001, "bin bir"),
    (1234, "bin iki yüz otuz dört"), (2000, "iki bin"), (11000, "on bir bin"),
    (100000, "yüz bin"), (101000, "yüz bir bin"), (1000000, "bir milyon"),
    (2500000000, "iki milyar beş yüz milyon"), (-45, "eksi kırk beş"),
])
def test_number_to_words(n, words):
    assert tk.number_to_words(n) == words


def test_number_to_words_errors():
    with pytest.raises(TypeError):
        tk.number_to_words(1.5)
    with pytest.raises(TypeError):
        tk.number_to_words(True)
    with pytest.raises(ValueError):
        tk.number_to_words(10 ** 40)


def test_amount_to_words():
    assert tk.amount_to_words("1250.75") == "bin iki yüz elli Türk lirası yetmiş beş kuruş"
    assert tk.amount_to_words(0.5) == "elli kuruş"
    assert tk.amount_to_words(0) == "sıfır Türk lirası"
    assert tk.amount_to_words(3) == "üç Türk lirası"
    assert tk.amount_to_words("-10.10") == "eksi on Türk lirası on kuruş"
    assert tk.amount_to_words(1.005) == "bir Türk lirası bir kuruş"
    assert tk.amount_to_words(5, currency="dolar", subunit="sent") == "beş dolar"


def test_format_and_parse_tl():
    assert tk.format_tl(1234567.5) == "1.234.567,50 ₺"
    assert tk.format_tl(999) == "999,00 ₺"
    assert tk.format_tl(-1500, symbol="TL") == "-1.500,00 TL"
    assert tk.format_tl("1000", symbol_first=True) == "₺1.000,00"
    assert tk.format_tl(1234.4, decimals=0, symbol="") == "1.234"
    assert tk.parse_tl("₺1.234,50") == Decimal("1234.50")
    assert tk.parse_tl("1.234,50 TL") == Decimal("1234.50")
    assert tk.parse_tl("-12,5") == Decimal("-12.5")
    with pytest.raises(ValueError):
        tk.parse_tl("TL")
    with pytest.raises(ValueError):
        tk.parse_tl("abc")


def test_cli(capsys):
    assert main(["slug", "Çelik", "Kapı", "Modelleri"]) == 0
    assert capsys.readouterr().out == "celik-kapi-modelleri\n"
    assert main(["yazi", "1250,75"]) == 0
    assert capsys.readouterr().out == "bin iki yüz elli Türk lirası yetmiş beş kuruş\n"
    assert main(["yazi", "--bitisik", "1250"]) == 0
    assert capsys.readouterr().out == "BinİkiYüzElli\n"
    assert main(["upper", "iğne"]) == 0
    assert capsys.readouterr().out == "İĞNE\n"
    assert main(["yazi", "abc"]) == 1


def test_cli_stdin(monkeypatch, capsys):
    import io
    monkeypatch.setattr("sys.stdin", io.StringIO("zeytin\nçay\nbal\n"))
    assert main(["sort"]) == 0
    assert capsys.readouterr().out == "bal\nçay\nzeytin\n"
