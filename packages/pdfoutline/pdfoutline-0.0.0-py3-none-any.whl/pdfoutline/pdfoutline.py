"""
Adobe pdfMark Reference
https://opensource.adobe.com/dc-acrobat-sdk-docs/acrobatsdk/pdfs/acrobatsdk_pdfmark.pdf

in toc file, you must close the parenthesis()!! otherwise, gs fails.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile


class Entry:
    def __init__(self, name: str, page: int, children: list[Entry]) -> None:
        self.name = name
        self.page = page
        self.children = children  # Entry list

    def pritty_print(self, depth: int) -> None:
        print(depth * "  " + f"{self.name}:{self.page}")
        for c in self.children:
            c.pritty_print(depth + 1)


class PDFOutline:
    def __init__(self, gs_path: str | None = None) -> None:
        self.gs_path = "gs" if gs_path is None else gs_path

    def run(self, inpdf: str, tocfilename: str, outpdf: str) -> None:
        for toc_line in open(tocfilename):
            elist = self.toc_to_elist(toc_line)
            gs_command = self.elist_to_gs(elist)

        tmp = tempfile.NamedTemporaryFile(mode="w", delete=False)
        tmp.write(gs_command)
        tmp.close()

        process = subprocess.Popen(
            [self.gs_path, "-o", outpdf, "-sDEVICE=pdfwrite", tmp.name, "-f", inpdf],
            stdout=subprocess.PIPE,
        )

        gs_stdout = process.stdout
        if gs_stdout is None:
            print(
                "gs command did not output anything. Something wrong?", file=sys.stderr
            )
            sys.exit(1)

        # show progress bar
        totalPage = 0
        for line in gs_stdout:
            tot = re.findall(r"Processing pages 1 through (\d+)", line.decode("ascii"))
            if tot:
                totalPage = int(tot[0])
                self.__printProgressBar(0, totalPage)
                break

        for line in gs_stdout:
            currentPage = re.findall(r"Page (\d+)", line.decode("ascii").strip())
            if currentPage:
                self.__printProgressBar(int(currentPage[0]), totalPage)

        os.unlink(tmp.name)

    @staticmethod
    def __printProgressBar(
        iteration: int,
        total: int,
        prefix: str = "",
        suffix: str = "",
        decimals: int = 1,
        length: int = 50,
        fill: str = "█",
        printEnd: str = "\r",
    ) -> None:
        """https://stackoverflow.com/questions/3173320"""
        percent = ("{0:." + str(decimals) + "f}").format(
            100 * (iteration / float(total))
        )
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + "-" * (length - filledLength)
        print(f"\r{prefix} |{bar}| {percent}% {suffix}", end=printEnd)
        # Print New Line on Complete
        if iteration == total:
            print()

    @staticmethod
    def toc_to_elist(toc: str) -> list[Entry]:
        tab = ""  # indentation character(s) evaluated and assigned to this later
        cur_entry: list[list[Entry]] = [[]]  # current entries by depth
        offset = 0
        for idx, line in enumerate(toc.split("\n")):
            depth = 0
            if line == "":
                continue
            # if indentation style hasn't been evaluated yet and the line starts
            # with a whitespace character, assume its an indent and assign all the
            # leading whitespace to tab

            # find length of leading whitespace in string
            tab_count = len(line) - len(line.lstrip())
            if tab == "" and line[0].isspace():
                tab = "" if tab_count == 0 else line[0] * tab_count
            else:
                # determine depth level of indent
                # count indent level up to first non-whitespace character;
                # allows for "indents" to appear inside section titles e.g. if an
                # indent level of a single space was chosen
                depth = line.count(tab, 0, tab_count)

            line, *_ = line.strip().split("#")  # strip comments and white spaces

            if line.startswith("+"):
                offset += int(line[1:])
            elif line.startswith("-"):
                offset -= int(line[1:])
            else:
                m = re.match(r"(?P<name>.*) (?P<page>\d+)$", line)
                if m is None:
                    # todo display line number
                    print(
                        f"syntax error in toc-file. line {idx}:\n" + line,
                        file=sys.stderr,
                    )
                    sys.exit(1)
                else:
                    name, page = m.group("name"), int(m.group("page")) + offset
                    cur_entry = cur_entry[: depth + 1] + [
                        [Entry(name, page, cur_entry[depth + 1])]
                    ]

        return cur_entry[0]

    @staticmethod
    def elist_to_gs(elist: list[Entry]) -> str:
        def __elist_to_gslist(elist: list[Entry]) -> list[str]:
            gs_list = []
            for entry in elist:
                gs_list.append(
                    f"[/Page {entry.page} "
                    "/View [/XYZ null null null] "
                    f"/Title <{entry.name.encode('utf-16').hex()}> "
                    f"/Count {len(entry.children)} /OUT pdfmark"
                )
                gs_list += __elist_to_gslist(entry.children)
            return gs_list

        return "\n".join(__elist_to_gslist(elist))
