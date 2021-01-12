#!/bin/python3
#
# Copyright 2020 Alexander Saastamoinen
#
#  Licensed under the EUPL, Version 1.2 or – as soon they
# will be approved by the European Commission - subsequent
# versions of the EUPL (the "Licence");
#  You may not use this work except in compliance with the
# Licence.
#  You may obtain a copy of the Licence at:
#
#  https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
#
#  Unless required by applicable law or agreed to in
# writing, software distributed under the Licence is
# distributed on an "AS IS" basis,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied.
#  See the Licence for the specific language governing
# permissions and limitations under the Licence.
#


import os
import pathlib
from datetime import datetime
import re
import argparse
from templates import euplTop, euplFull
from templates import gpl3Top, gpl3, mitTop, mitFull
from templates import agplTop, agplFull, mozillaTop, mozillaFull
from templates import beerTop, beerFull, unlicenseTop, unlicenseFull

license = {
        "eupl": [euplTop, euplFull],
        "gpl3": [gpl3Top, gpl3],
        "gpl": [gpl3Top, gpl3],
        "mit": [mitTop, mitFull],
        "agpl": [agplTop, agplFull],
        "mozilla": [mozillaTop, mozillaFull],
        "beer": [beerTop, beerFull],
        "unlicense": [unlicenseTop, unlicenseFull],
        }

const_ignore_dirs = [
        (".git", "simple"),
        ("testdata", "simple"),
        ("node_modules", "simple"),
        ("dist", "simple"),
        ("__pycache__", "simple"),
        (r"^\..+", "regex"),
        ]

const_ignore_files = [
        (r"README\.*\w{0,5}$", "regex"),  # skip REAME
        (r"^.+\.txt$", "regex"),  # skip txt files
        (r"^.+\.xml$", "regex"),  # skip xml definitions
        (r"^.+\.json$", "regex"),  # skip json definitions
        (r"^.+\.jpg$", "regex"),  # skip jpg definitions
        (r"^.+\.png$", "regex"),  # skip png definitions
        (r"^.+\.yml$", "regex"),  # skip yaml definitions
        (r"^.+\.yaml$", "regex"),  # skip yaml definitions
        (r"^\..+", "regex"),  # skip hidden files
        (r"^\w+$", "regex"),  # skip binaries
        ("go.sum", "simple"),  # go sum files
        ("favicon.ico", "simple"),  # website icon file
        ("go.mod", "simple"),  # go module file
        ]

comment_format_by_ext = {
        "py": ["#"],
        "scss": ["//"],
        "js": ["//"],
        "ts": ["//"],
        "cpp": ["//"],
        "c": ["//"],
        "C": ["//"],
        "go": ["//"],
        "yml": ["#"],
        "html": ["<!--", "-->"],
        "css": ["/*", "*/"],
        }

comment_format_by_filere = [  # these are regex strings
        ("Dockerfile", ["#"]),  # this exists as reference, ignored by prog
        ]


def main():
    # parse command line arguments
    args = parser().parse_args()

    # initialize class that shares parsed flags with functionality
    i_details = implementation_details(args.verbose, args.regex, args.force)

    # print licenses and exit
    if args.listlicenses:
        i_details.print_licenses()

    # get license holder if not provided
    if len(args.license_holder) == 0:
        license_holder = i_details.get_license_holder()
    else:
        license_holder = " ".join(args.license_holder)
    if args.verbose:
        print("License holder: ", license_holder)

    # print date to be used
    if args.verbose:
        print("Date: ", args.date)

    # Set build-in items to ignore
    ignoredirs = ignore_items(const_ignore_dirs)
    ignorefiles = ignore_items(const_ignore_files)
    # Set commandline in items to ignore
    i_details.add_ignores([
            (args.skipdir, ignoredirs),
            (args.skipfile, ignorefiles)
            ])

    # add command line formats
    formats = file_format()
    if args.format is not None:
        for target, syntax in args.format:
            formats.add(target, syntax)

    # get licence text
    if args.verbose:
        print("Licence: ", args.license)
    try:
        lic = license[args.license]
    except KeyError:
        print("license not supported")
        raise SystemExit

    # get files and ignore some of them
    files = finder(args.verbose, ignoredirs, ignorefiles).get_files(args.path)

    # Double check user wants to continue
    i_details.confirm_continue(files)

    # add license to each source file
    for f in files:
        if args.comment == "":
            # attempt filetype detection by extension
            format_str = formats.comment_syntax(f)
        else:
            format_str = args.comment
        top = comment_out(lic[0], format_str) % (args.date,
                                                 license_holder)
        if not already_has_license(f, top):
            write_top(top, f)
        else:
            print("file ", f, " already has license, skipping")

    # add full text
    location = find_root(args.path)
    i_details.write_license(lic[1], location, args.license_file_name)


def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("license_holder",
                        help="Name of licence holder."
                        "use quotation marks to include whitespace. Place"
                        " as first argument for safe usage with other flags. "
                        "Default license: EUPL",
                        nargs=argparse.REMAINDER, default="")
    parser.add_argument("-p", "--path",
                        help="Specifies path to parse, "
                        "defaults to current directory",
                        default=".")
    parser.add_argument("-d", "--date",
                        help="Date as year (int) to use",
                        type=int,
                        default=datetime.now().year)
    parser.add_argument("-l", "--license",
                        help="Specifies license to add",
                        default="eupl")
    parser.add_argument("-f", "--force",
                        help="Overrides checks and user input.",
                        action="store_true")
    parser.add_argument("-list", "--listlicenses",
                        help="Lists available licenses",
                        action="store_true")
    parser.add_argument("-ln", "--license_file_name",
                        help="Specifies name of license file, default LICENSE",
                        default="LICENSE")
    parser.add_argument("-e", "--end",
                        help="Does nothing, use to end a multi item flag "
                        "before providing license holder",
                        action="store_true")
    parser.add_argument("-sd", "--skipdir",
                        help="Sets directories to skip. "
                        "Make sure you have a flag before license holder",
                        nargs="+", action="extend")
    parser.add_argument("-sf", "--skipfile",
                        help="Sets files to skip. "
                        "Make sure you have a flag before license holder",
                        nargs="+", action="extend")
    parser.add_argument("-re", "--regex",
                        help="Use with skip flags, "
                        "causes arguments to be interpreted as regex strings",
                        action="store_true")
    parser.add_argument("-fmt", "--format",
                        type=syntax_arg,
                        help="Add filetype comment syntax. "
                        "EXT/REGEX=SYNTAX. "
                        "Make sure you have a flag before license holder. "
                        "Example: '-f .ext=!! Dockerfile=#' "
                        "Use '.ext' for extension detection, "
                        "otherwise will be interpreted as a regex string",
                        nargs="+", action="extend")
    parser.add_argument("-c", "--comment",
                        help="Set comment syntax, replaces filetype detection",
                        default="")
    parser.add_argument("-v", "--verbose",
                        help="Increased verbosity",
                        action="store_true")
    return parser


# puts together parsed flags and some basic operations
# meant to keep details out of the main function
class implementation_details:
    def __init__(self, verbose, regex, force):
        self.verbose = verbose
        self.regex = regex
        self.force = force

    def get_license_holder(self):
        if self.force:
            raise RuntimeError("force flag requires license holder"
                               "to be provided in command line")
        return input("Please provide name to use on license:\n")

    def add_ignores(self, args_and_obj):
        for skip_args, obj in args_and_obj:
            if skip_args is not None:
                for ignore in skip_args:
                    if self.regex:
                        obj.set_regex(ignore)
                    else:
                        obj.set_simple(ignore)

    def confirm_continue(self, files):
        if self.verbose:
            print("About to add licence to:")
            for f in files:
                print("\t", f)
        else:
            print("Adding license to ", len(files), " files")
        if self.force:
            return
        response = input("continue? (y/N)\n")
        if response != 'y':
            print("execution stopped by user")
            raise SystemExit

    def print_licenses():
        for lic in license:
            print(lic)
        raise SystemExit

    def write_license(self, license, location, filename):
        try:
            write_full(license, location, filename, "x")
        except FileExistsError:
            if self.force:
                return
            resp = input("Full license already exists, overwrite? (y/n)\n")
            if resp != 'y':
                raise SystemExit
            else:
                write_full(license, location, filename, "w")


def find_root(path):
    tuples = os.walk(path, topdown=True)
    for root, dirs, files in tuples:
        for d in dirs:
            if d == ".git":
                return os.path.abspath(root)
    return os.path.abspath(path)


def write_full(text, location, name, open_opt):
    with open(os.path.join(location, name), open_opt) as f:
        f.write(text)


def already_has_license(filepath, top):
    regex = re.compile("^#!/.+$")
    with open(filepath, "r") as f:
        content = f.read().split("\n")
        if regex.match(content[0]):
            content = content[1:]
        return "\n".join(content).startswith(top)


def write_top(ntop, path):
    regex = re.compile("^#!/.+$")
    f = open(path, 'r')
    line = f.readline()
    mark = False
    if regex.search(line) is not None:
        mark = True
        pass
    else:
        f.seek(0)  # reset file position
    saved = f.read()
    f.close()
    f = open(path, 'w')
    if mark:
        f.write(line)
    f.writelines([ntop, "\n", saved])
    f.close()


def comment_out(text, comment):
    def comment_left(text):
        if text == "":
            return comment[0]
        return comment[0]+' '+text

    def comment_both(text):
        if text == "":
            return comment[0]+' '+comment[1]
        return comment[0]+' '+text+' '+comment[1]
    if not isinstance(comment, list) or len(comment) > 2:
        raise ValueError("incorrect comment arg, must be array of 1 or 2")
    if len(comment) == 1:
        line_maker = comment_left
    elif len(comment) == 2:
        line_maker = comment_both
    else:
        raise ValueError("comment syntax must be an array of 1 or 2")
    res = []
    res.append(line_maker(""))
    for line in text.splitlines():
        res.append(line_maker(line))
    res.append(line_maker(""))
    res.append("")
    return "\n".join(res)


def syntax_arg(arg):
    key_and_comment = arg.split("=")
    if len(key_and_comment) != 2:
        raise ValueError("syntax arguments must be given in key=value format")
    comments = key_and_comment[1].split(",")
    return (key_and_comment[0], comments)


class file_format:
    def __init__(self, ext=None, filere=None):
        if ext is None:
            self.ext = comment_format_by_ext
        else:
            self.ext = ext
        if filere is None:
            self.fileregex = comment_format_by_filere
        else:
            self.fileregex = filere

    def add(self, target, comment_syntax):
        if target[0] == '.':
            self.add_ext(target[1:], comment_syntax)
        else:
            self.add_filere(target, comment_syntax)

    def add_ext(self, ext, comment_syntax):
        self.ext[ext] = comment_syntax

    def add_filere(self, filere, comment_syntax):
        self.fileregex.append((filere, comment_syntax))

    def comment_syntax(self, name):
        if pathlib.PurePath(name).suffix != "":
            return self.ext[pathlib.PurePath(name).suffix[1:]]
        else:
            for filere, comment in self.fileregex:
                regex = re.compile(filere)
                if regex.match(name):
                    return comment
            raise ValueError("no comment syntax for given file")


class ignore_items:
    def __init__(self, items=None):
        self.data = {}
        if items is not None:
            self.add_items(items)

    def __setitem__(self, k, v):
        self.data[k] = v

    def __getitem__(self, k):
        return self.data[k]

    def __iter__(self):
        return iter(self.data.keys())

    def add_items(self, tuples):
        for k, v in tuples:
            if v == "regex":
                self.set_regex(k)
            else:
                self.set_simple(k)

    def ignore(self, item):
        for key in self:
            if self[key](key, item):
                return True
        return False

    def set_simple(self, name):
        self[name] = self.simple_check

    def set_regex(self, name):
        self[name] = self.regex_check

    def simple_check(self, matchTo, toMatch):
        if matchTo == toMatch:
            return True
        else:
            return False

    def regex_check(self, matchTo, toMatch):
        regex = re.compile(matchTo)
        res = regex.search(toMatch)
        if (res is not None):
            return True
        else:
            return False


class finder:
    def __init__(self, verbose, ignore_dirs, ignore_files):
        self.verbose = verbose
        self.ignore_dirs = ignore_dirs
        self.ignore_files = ignore_files

    def get_files(self, path):
        return self.ignore(self.find_files(path))

    def find_files(self, path):
        return os.walk(path, topdown=True)

    # returns files after ignoring relevant files
    def ignore(self, all_files):
        res = []
        for root, dirs, files in all_files:
            self.ignoreItems(True, dirs)
            self.ignoreItems(False, files)
            for f in files:
                res.append(os.path.join(root, f))
        return res

    def ignoreItems(self, dirs, items):
        ignores = self.ignore_dirs if dirs else self.ignore_files
        while True:  # restart from topafter deleting an element
            i = 0
            for item in items:
                if ignores.ignore(item):
                    if self.verbose:
                        print("skipping: ", os.path.abspath(item))
                    items.remove(item)
                    break
                i += 1
            if i >= len(items):
                break


if __name__ == "__main__":
    main()
