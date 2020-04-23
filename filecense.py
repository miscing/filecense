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
import datetime
import re
import argparse

#  templates
euplTop = """Copyright %d %s

 Licensed under the EUPL, Version 1.2 or – as soon they
will be approved by the European Commission - subsequent
versions of the EUPL (the "Licence");
 You may not use this work except in compliance with the
Licence.
 You may obtain a copy of the Licence at:

 https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

 Unless required by applicable law or agreed to in
writing, software distributed under the Licence is
distributed on an "AS IS" basis,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
express or implied.
 See the Licence for the specific language governing
permissions and limitations under the Licence."""

euplFull = """                     EUROPEAN UNION PUBLIC LICENCE v. 1.2
                      EUPL © the European Union 2007, 2016

This European Union Public Licence (the ‘EUPL’) applies to the Work (as defined
below) which is provided under the terms of this Licence. Any use of the Work,
other than as authorised under this Licence is prohibited (to the extent such
use is covered by a right of the copyright holder of the Work).

The Work is provided under the terms of this Licence when the Licensor (as
defined below) has placed the following notice immediately following the
copyright notice for the Work:

        Licensed under the EUPL

or has expressed by any other means his willingness to license under the EUPL.

1. Definitions

In this Licence, the following terms have the following meaning:

- ‘The Licence’: this Licence.

- ‘The Original Work’: the work or software distributed or communicated by the
  Licensor under this Licence, available as Source Code and also as Executable
  Code as the case may be.

- ‘Derivative Works’: the works or software that could be created by the
  Licensee, based upon the Original Work or modifications thereof. This Licence
  does not define the extent of modification or dependence on the Original Work
  required in order to classify a work as a Derivative Work; this extent is
  determined by copyright law applicable in the country mentioned in Article 15.

- ‘The Work’: the Original Work or its Derivative Works.

- ‘The Source Code’: the human-readable form of the Work which is the most
  convenient for people to study and modify.

- ‘The Executable Code’: any code which has generally been compiled and which is
  meant to be interpreted by a computer as a program.

- ‘The Licensor’: the natural or legal person that distributes or communicates
  the Work under the Licence.

- ‘Contributor(s)’: any natural or legal person who modifies the Work under the
  Licence, or otherwise contributes to the creation of a Derivative Work.

- ‘The Licensee’ or ‘You’: any natural or legal person who makes any usage of
  the Work under the terms of the Licence.

- ‘Distribution’ or ‘Communication’: any act of selling, giving, lending,
  renting, distributing, communicating, transmitting, or otherwise making
  available, online or offline, copies of the Work or providing access to its
  essential functionalities at the disposal of any other natural or legal
  person.

2. Scope of the rights granted by the Licence

The Licensor hereby grants You a worldwide, royalty-free, non-exclusive,
sublicensable licence to do the following, for the duration of copyright vested
in the Original Work:

- use the Work in any circumstance and for all usage,
- reproduce the Work,
- modify the Work, and make Derivative Works based upon the Work,
- communicate to the public, including the right to make available or display
  the Work or copies thereof to the public and perform publicly, as the case may
  be, the Work,
- distribute the Work or copies thereof,
- lend and rent the Work or copies thereof,
- sublicense rights in the Work or copies thereof.

Those rights can be exercised on any media, supports and formats, whether now
known or later invented, as far as the applicable law permits so.

In the countries where moral rights apply, the Licensor waives his right to
exercise his moral right to the extent allowed by law in order to make effective
the licence of the economic rights here above listed.

The Licensor grants to the Licensee royalty-free, non-exclusive usage rights to
any patents held by the Licensor, to the extent necessary to make use of the
rights granted on the Work under this Licence.

3. Communication of the Source Code

The Licensor may provide the Work either in its Source Code form, or as
Executable Code. If the Work is provided as Executable Code, the Licensor
provides in addition a machine-readable copy of the Source Code of the Work
along with each copy of the Work that the Licensor distributes or indicates, in
a notice following the copyright notice attached to the Work, a repository where
the Source Code is easily and freely accessible for as long as the Licensor
continues to distribute or communicate the Work.

4. Limitations on copyright

Nothing in this Licence is intended to deprive the Licensee of the benefits from
any exception or limitation to the exclusive rights of the rights owners in the
Work, of the exhaustion of those rights or of other applicable limitations
thereto.

5. Obligations of the Licensee

The grant of the rights mentioned above is subject to some restrictions and
obligations imposed on the Licensee. Those obligations are the following:

Attribution right: The Licensee shall keep intact all copyright, patent or
trademarks notices and all notices that refer to the Licence and to the
disclaimer of warranties. The Licensee must include a copy of such notices and a
copy of the Licence with every copy of the Work he/she distributes or
communicates. The Licensee must cause any Derivative Work to carry prominent
notices stating that the Work has been modified and the date of modification.

Copyleft clause: If the Licensee distributes or communicates copies of the
Original Works or Derivative Works, this Distribution or Communication will be
done under the terms of this Licence or of a later version of this Licence
unless the Original Work is expressly distributed only under this version of the
Licence — for example by communicating ‘EUPL v. 1.2 only’. The Licensee
(becoming Licensor) cannot offer or impose any additional terms or conditions on
the Work or Derivative Work that alter or restrict the terms of the Licence.

Compatibility clause: If the Licensee Distributes or Communicates Derivative
Works or copies thereof based upon both the Work and another work licensed under
a Compatible Licence, this Distribution or Communication can be done under the
terms of this Compatible Licence. For the sake of this clause, ‘Compatible
Licence’ refers to the licences listed in the appendix attached to this Licence.
Should the Licensee's obligations under the Compatible Licence conflict with
his/her obligations under this Licence, the obligations of the Compatible
Licence shall prevail.

Provision of Source Code: When distributing or communicating copies of the Work,
the Licensee will provide a machine-readable copy of the Source Code or indicate
a repository where this Source will be easily and freely available for as long
as the Licensee continues to distribute or communicate the Work.

Legal Protection: This Licence does not grant permission to use the trade names,
trademarks, service marks, or names of the Licensor, except as required for
reasonable and customary use in describing the origin of the Work and
reproducing the content of the copyright notice.

6. Chain of Authorship

The original Licensor warrants that the copyright in the Original Work granted
hereunder is owned by him/her or licensed to him/her and that he/she has the
power and authority to grant the Licence.

Each Contributor warrants that the copyright in the modifications he/she brings
to the Work are owned by him/her or licensed to him/her and that he/she has the
power and authority to grant the Licence.

Each time You accept the Licence, the original Licensor and subsequent
Contributors grant You a licence to their contributions to the Work, under the
terms of this Licence.

7. Disclaimer of Warranty

The Work is a work in progress, which is continuously improved by numerous
Contributors. It is not a finished work and may therefore contain defects or
‘bugs’ inherent to this type of development.

For the above reason, the Work is provided under the Licence on an ‘as is’ basis
and without warranties of any kind concerning the Work, including without
limitation merchantability, fitness for a particular purpose, absence of defects
or errors, accuracy, non-infringement of intellectual property rights other than
copyright as stated in Article 6 of this Licence.

This disclaimer of warranty is an essential part of the Licence and a condition
for the grant of any rights to the Work.

8. Disclaimer of Liability

Except in the cases of wilful misconduct or damages directly caused to natural
persons, the Licensor will in no event be liable for any direct or indirect,
material or moral, damages of any kind, arising out of the Licence or of the use
of the Work, including without limitation, damages for loss of goodwill, work
stoppage, computer failure or malfunction, loss of data or any commercial
damage, even if the Licensor has been advised of the possibility of such damage.
However, the Licensor will be liable under statutory product liability laws as
far such laws apply to the Work.

9. Additional agreements

While distributing the Work, You may choose to conclude an additional agreement,
defining obligations or services consistent with this Licence. However, if
accepting obligations, You may act only on your own behalf and on your sole
responsibility, not on behalf of the original Licensor or any other Contributor,
and only if You agree to indemnify, defend, and hold each Contributor harmless
for any liability incurred by, or claims asserted against such Contributor by
the fact You have accepted any warranty or additional liability.

10. Acceptance of the Licence

The provisions of this Licence can be accepted by clicking on an icon ‘I agree’
placed under the bottom of a window displaying the text of this Licence or by
affirming consent in any other similar way, in accordance with the rules of
applicable law. Clicking on that icon indicates your clear and irrevocable
acceptance of this Licence and all of its terms and conditions.

Similarly, you irrevocably accept this Licence and all of its terms and
conditions by exercising any rights granted to You by Article 2 of this Licence,
such as the use of the Work, the creation by You of a Derivative Work or the
Distribution or Communication by You of the Work or copies thereof.

11. Information to the public

In case of any Distribution or Communication of the Work by means of electronic
communication by You (for example, by offering to download the Work from a
remote location) the distribution channel or media (for example, a website) must
at least provide to the public the information requested by the applicable law
regarding the Licensor, the Licence and the way it may be accessible, concluded,
stored and reproduced by the Licensee.

12. Termination of the Licence

The Licence and the rights granted hereunder will terminate automatically upon
any breach by the Licensee of the terms of the Licence.

Such a termination will not terminate the licences of any person who has
received the Work from the Licensee under the Licence, provided such persons
remain in full compliance with the Licence.

13. Miscellaneous

Without prejudice of Article 9 above, the Licence represents the complete
agreement between the Parties as to the Work.

If any provision of the Licence is invalid or unenforceable under applicable
law, this will not affect the validity or enforceability of the Licence as a
whole. Such provision will be construed or reformed so as necessary to make it
valid and enforceable.

The European Commission may publish other linguistic versions or new versions of
this Licence or updated versions of the Appendix, so far this is required and
reasonable, without reducing the scope of the rights granted by the Licence. New
versions of the Licence will be published with a unique version number.

All linguistic versions of this Licence, approved by the European Commission,
have identical value. Parties can take advantage of the linguistic version of
their choice.

14. Jurisdiction

Without prejudice to specific agreement between parties,

- any litigation resulting from the interpretation of this License, arising
  between the European Union institutions, bodies, offices or agencies, as a
  Licensor, and any Licensee, will be subject to the jurisdiction of the Court
  of Justice of the European Union, as laid down in article 272 of the Treaty on
  the Functioning of the European Union,

- any litigation arising between other parties and resulting from the
  interpretation of this License, will be subject to the exclusive jurisdiction
  of the competent court where the Licensor resides or conducts its primary
  business.

15. Applicable Law

Without prejudice to specific agreement between parties,

- this Licence shall be governed by the law of the European Union Member State
  where the Licensor has his seat, resides or has his registered office,

- this licence shall be governed by Belgian law if the Licensor has no seat,
  residence or registered office inside a European Union Member State.

Appendix

‘Compatible Licences’ according to Article 5 EUPL are:

- GNU General Public License (GPL) v. 2, v. 3
- GNU Affero General Public License (AGPL) v. 3
- Open Software License (OSL) v. 2.1, v. 3.0
- Eclipse Public License (EPL) v. 1.0
- CeCILL v. 2.0, v. 2.1
- Mozilla Public Licence (MPL) v. 2
- GNU Lesser General Public Licence (LGPL) v. 2.1, v. 3
- Creative Commons Attribution-ShareAlike v. 3.0 Unported (CC BY-SA 3.0) for
  works other than software
- European Union Public Licence (EUPL) v. 1.1, v. 1.2
- Québec Free and Open-Source Licence — Reciprocity (LiLiQ-R) or Strong
  Reciprocity (LiLiQ-R+).

The European Commission may update this Appendix to later versions of the above
licences without producing a new version of the EUPL, as long as they provide
the rights granted in Article 2 of this Licence and protect the covered Source
Code from exclusive appropriation.

All other changes or additions to this Appendix require the production of a new
EUPL version."""




def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("license_holder", help="name of licence holder, use quotation marks to include whitespace")
    parser.add_argument("-d", "--date", help="year to use, no sanity checks will be used literally", default=datetime.datetime.now().year)
    parser.add_argument("-l", "--license", help="specifies license to add", default="eupl" )
    parser.add_argument("-ln", "--license_file_name", help="specifies name of license file, default LICENSE", default="LICENSE" )
    parser.add_argument("-sd", "--skipdir", help="sets directories to skip", nargs="+")
    parser.add_argument("-sf", "--skipfile", help="sets files to skip", nargs="+")
    parser.add_argument("-re", "--regex", help="together with skip flags causes arguments to be interpreted as regex strings", action="store_true")
    parser.add_argument("-p", "--path", help="specifies path to parse, default is current directory", default=".")
    parser.add_argument("-f", "--format", help="specifies comment syntax based on language, such as py for python comments. Usually unnecessary", default="")
    parser.add_argument("-c", "--comment", help="places provided string at the front of every sentence  of top template, overrides format option", default="")
    parser.add_argument("-v", "--verbose", help="increased verbosity", action="store_true")
    args = parser.parse_args()

    if (args.verbose):
        print("using current year: ", args.date)

    # Set up items to ignore
    ignoredirs = ignore_items()
    ignoredirs.add_item(".git", "simple")
    ignoredirs.add_item("testdata", "simple")
    ignoredirs.add_item("^\..+", "regex")
    if args.skipdir != None:
        for sd in args.skipdir:
            if args.regex:
                ignoredirs.add_item(sd, "regex")
            else:
                ignoredirs.add_item(sd, "simple")

    ignorefiles = ignore_items()
    ignorefiles.add_item("README\.*\w{0,5}$", "regex")
    ignorefiles.add_item("^.+\.txt$", "regex")
    ignorefiles.add_item("^\..+", "regex")
    ignorefiles.add_item("^\w+$", "regex")
    if args.skipfile != None:
        for sf in args.skipfile:
            if args.regex:
                ignorefiles.add_item(sf, "regex")
            else:
                ignorefiles.add_item(sf, "simple")


    fer = finder(args.verbose, ignoredirs, ignorefiles)
    res = fer.find_files(args.path)

    license = {
            "eupl" : [euplTop, euplFull],
            }
    try:
        lic = license[args.license]
    except:
        print("license not supported")
        return 2
    else:
        for p in res:
            format_str = ""
            if args.comment == "":
                formats = {
                        "py" : "#",
                        "js" : "//",
                        "ts" : "//",
                        "cpp" : "//",
                        "c" : "//",
                        "C" : "//",
                        "go" : "//"
                        }
                if args.format != "":
                    try:
                        format_str = formats[args.format]
                    except:
                        print("specified format not supported")
                        return 2
                else:
                    # attempt filetype detection by extension
                    try:
                        format_str = formats[os.path.splitext(p)[1][1:]]
                    except:
                        print(os.path.splitext(p)[1][1:])
                        print("could not detect filetype (or filetype not supported, use '-c' flag or '-f' flags) of file: ", p)
                        return 2

                top = comment_out(lic[0], format_str)
            else:
                format_str = args.comment
            top = comment_out(lic[0], format_str)
            # print( top % (args.date, args.license_holder))
            try:
                write_top(top % (args.date, args.license_holder), p)
            except Exception as error:
                print("failed to write top, quitting")
                print(error)
                return 2

        # add full text
        tuples = os.walk(args.path, topdown=True)
        for root, dirs, files in tuples:
            for d in dirs:
                if d == ".git":
                    if (args.verbose):
                        print("found .git directory at: ", root, " adding full license text there from presumption it's project root")
                    write_full(lic[1], root, args.license_file_name)

def write_full(text, location, name):
    try:
        f = open(os.path.join(location, name), "x")
    except:
        print("license file of name: ", os.path.join(location, name), " exists")
        return
    else:
        f.write(text)
        f.close()

def comment_out(text, comment):
    res = []
    res.append(comment)
    for line in text.splitlines():
        if line == "":
            res.append(comment)
        else:
            res.append(comment+' '+line)
    res.append(comment)
    res.append("")
    return "\n".join(res)

class ignore_items(dict):
    def __init__(self):
        self.data = {}
    def __setitem__(self, k, v):
        self.data[k] = v
    def __getitem__(self, k):
        return self.data[k]
    def __iter__(self):
        return iter(self.data.keys())
    def add_item(self, name, mode):
        modes = {
                "simple" : self.set_simple,
                "regex" : self.set_regex
                }
        modes[mode](name)
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
        try:
            res = regex.search(toMatch)
        except:
            print("error doing regex search")
            return False
        else:
            if ( res != None ):
                return True
            else:
                return False

class finder:
    def __init__(self, verbose, ignore_dirs, ignore_files):
        self.verbose = verbose
        self.ignore_dirs = ignore_dirs
        self.ignore_files = ignore_files
    def find_files(self, path):
        res = []
        tuples = os.walk(path, topdown=True)
        if self.verbose:
            print("Directories to skip:")
            for skipdir in self.ignore_dirs:
                print("\t", end='')
                print(skipdir)
            print("Files to skip:")
            for skipfile in self.ignore_files:
                print("\t", end='')
                print(skipfile)

        for root, dirs, files in tuples:
            if self.verbose:
                print("\nDirs and files found:")
                for d in dirs:
                    print(d)
                for f in files:
                    print(f)
                print()

            mark = True
            doubleBreak = False
            while mark: # we need to restart from top after deleting an element
                i = 0
                for d in dirs:
                    for key in self.ignore_dirs:
                        if ( self.ignore_dirs[key](key, d) ):
                            if self.verbose:
                                print("skipping dir: ", os.path.join(root, d), " due to: ", key)
                            try:
                                dirs.remove(d)
                            except:
                                print("failed to ignore a directory", d)
                                return 2
                            else:
                                doubleBreak = True
                                break
                    if doubleBreak:
                        doubleBreak = False
                        break
                    i+=1
                if i >= len(dirs):
                    mark = False
                    break

            for f in files:
                mark = True
                for key in self.ignore_files:
                    if ( self.ignore_files[key](key, f) ):
                        if self.verbose:
                            print("skipping file: ", os.path.join(root, f), " due to: ", key)
                        mark = False
                        break
                    else:
                        continue
                if mark:
                    res.append(os.path.join(root, f))
                    if self.verbose:
                        print("file: ", os.path.join(root, f), "to be operated on")
        if self.verbose:
            print("\nfiles to add license to")
            print(res)
            print()
        return res

def write_top(ntop, path):
    regex= re.compile("^#!/.+$")
    f = open(path, 'r')
    line = f.readline()
    mark = False
    if regex.search(line) != None:
        mark = True
        pass
    else:
        f.seek(0) # reset file position
    saved = f.read()
    f.close()

    f = open(path, 'w')
    if mark:
        f.write(line)
    f.writelines([ntop ,"\n",saved])
    f.close()

if __name__ == "__main__":
    main()
