#!/usr/bin/python3

import argparse
import sys

from .pdfoutline import PDFOutline


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="pdfoutline", description="add table of contents to a pdf"
    )

    parser.add_argument("in_pdf", metavar="in.pdf", help="the input pdf file")
    parser.add_argument(
        "in_toc",
        metavar="in.toc",
        help=" a table of contents file in the specified format ",
    )
    parser.add_argument("out_pdf", metavar="out.pdf", help=" the output pdf file")
    parser.add_argument(
        "-g",
        "--gs_path",
        metavar="PATH",
        type=str,
        help="path to the ghostscript executable",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.in_pdf == args.out_pdf:
        print("Specify different names for input and output files.")
        sys.exit(1)
    p = PDFOutline(gs_path=args.gs_path)
    p.run(args.in_pdf, args.in_toc, args.out_pdf)


if __name__ == "__main__":
    main()
