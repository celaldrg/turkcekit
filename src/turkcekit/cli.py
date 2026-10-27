"""Command line: turkcekit <command> [text...]  (reads stdin when no text given)."""

import argparse
import sys

from . import (__version__, amount_to_words, asciify, format_tl, lower,
               number_to_words, slugify, sorted_tr, title, upper)


def _text(args) -> list:
    if args.text:
        return [" ".join(args.text)]
    return [line.rstrip("\n") for line in sys.stdin]


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="turkcekit",
                                description="Turkish-aware text utilities.")
    p.add_argument("--version", action="version", version=f"turkcekit {__version__}")
    sub = p.add_subparsers(dest="cmd", required=True)
    for name, helptext in [("lower", "Turkish lower case"), ("upper", "Turkish upper case"),
                           ("title", "Turkish title case"), ("ascii", "fold to ASCII"),
                           ("slug", "make a URL slug"), ("sort", "sort lines alphabetically (Turkish)"),
                           ("yazi", "number or amount to words"), ("tl", "format as Turkish lira")]:
        sp = sub.add_parser(name, help=helptext)
        sp.add_argument("text", nargs="*")
        if name == "sort":
            sp.add_argument("-r", "--reverse", action="store_true")
        if name == "yazi":
            sp.add_argument("--para", action="store_true", help="read as a lira amount")
            sp.add_argument("--bitisik", action="store_true", help="joined cheque style")
    args = p.parse_args(argv)
    lines = _text(args)

    try:
        if args.cmd == "sort":
            out = sorted_tr([l for l in lines if l], reverse=args.reverse)
        elif args.cmd == "yazi":
            out = []
            for l in lines:
                l = l.strip()
                if not l:
                    continue
                if args.para or "." in l or "," in l:
                    w = amount_to_words(l.replace(",", "."))
                else:
                    w = number_to_words(int(l))
                out.append(title(w).replace(" ", "") if args.bitisik else w)
        else:
            fn = {"lower": lower, "upper": upper, "title": title, "ascii": asciify,
                  "slug": slugify, "tl": format_tl}[args.cmd]
            out = [fn(l) for l in lines]
    except (ValueError, TypeError) as e:
        print(f"turkcekit: {e}", file=sys.stderr)
        return 1
    print("\n".join(out))
    return 0
