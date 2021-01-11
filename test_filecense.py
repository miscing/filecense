import unittest
from filecense import finder, ignore_items, file_format, find_root
from filecense import already_has_license, euplTop
from filecense import const_ignore_files, const_ignore_dirs
from filecense import write_full, write_top, syntax_arg, comment_out
import os
from datetime import datetime
from shutil import copyfile

testfiles = [
        "binFile",
        ".hiddenFile",
        "README",
        "README.md",
        "skipFile.jpg",
        "skipFile.json",
        "skipFile.png",
        "skipFile.txt",
        "sourceFile.c",
        "sourceFile.cpp",
        "sourceFile.go",
        "sourceFile.js",
        "sourceFile.py",
        "sourceFile.ts",
        "sourceFile.yml",
        "sourceFile.html",
        "sourceFile.css",
        ]

testdirs = [
        "testdata",
        "testdata/newdir",
        "testdata/newdir/nestedDir",
        "testdata/.hiddenDir",
        "testdata/testdata",
        ]

notIgnoredFiles = [
        './testdata/sourceFile.c',
        './testdata/sourceFile.js',
        './testdata/sourceFile.html',
        './testdata/sourceFile.py',
        './testdata/sourceFile.go',
        './testdata/sourceFile.ts',
        './testdata/sourceFile.cpp',
        './testdata/sourceFile.css',
        './testdata/newdir/sourceFile.c',
        './testdata/newdir/sourceFile.js',
        './testdata/newdir/sourceFile.html',
        './testdata/newdir/sourceFile.py',
        './testdata/newdir/sourceFile.go',
        './testdata/newdir/sourceFile.ts',
        './testdata/newdir/sourceFile.cpp',
        './testdata/newdir/sourceFile.css',
        './testdata/newdir/nestedDir/sourceFile.c',
        './testdata/newdir/nestedDir/sourceFile.js',
        './testdata/newdir/nestedDir/sourceFile.html',
        './testdata/newdir/nestedDir/sourceFile.py',
        './testdata/newdir/nestedDir/sourceFile.go',
        './testdata/newdir/nestedDir/sourceFile.ts',
        './testdata/newdir/nestedDir/sourceFile.cpp',
        './testdata/newdir/nestedDir/sourceFile.css'
        ]


def validFile(name):
    for f in testfiles:
        if name == f:
            return True

    return False


def validDir(name):
    for d in testdirs:
        if name == d:
            return True
    return False


class TestIgnoreItems(unittest.TestCase):
    def test_simple_check(self):
        ignoredirs = ignore_items(const_ignore_dirs)
        self.assertFalse(ignoredirs["testdata"]("testdata", "asodijsaoid"))
        self.assertTrue(ignoredirs["testdata"]("testdata", "testdata"))
        self.assertTrue(ignoredirs.ignore("testdata"))
        self.assertFalse(ignoredirs.ignore("asoidjsad"))

    def test_regex_check(self):
        ignoredirs = ignore_items(const_ignore_dirs)
        ignorefiles = ignore_items(const_ignore_files)
        self.assertFalse(ignoredirs.ignore("asdoijsa"))
        self.assertTrue(ignoredirs.ignore(".hidden"))
        self.assertFalse(ignorefiles.ignore("source.go"))
        self.assertTrue(ignorefiles.ignore("binFile"))
        self.assertTrue(ignorefiles.ignore(".hiddenFile"))
        self.assertTrue(ignorefiles.ignore("picture.jpg"))
        self.assertTrue(ignorefiles.ignore("data.json"))


class TestFinder(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ignoredirs = ignore_items(const_ignore_dirs)
        ignorefiles = ignore_items(const_ignore_files)
        cls.finder = finder(False, ignoredirs, ignorefiles)

    def test_find_files(self):
        all_files = self.finder.find_files("./testdata/")
        for root, _, files in all_files:
            self.assertTrue(validDir(os.path.normpath(root)))
            self.assertEqual(len(files), len(testfiles))
            for f in files:
                self.assertTrue(validFile(f))

    def test_ignoreItems(self):
        all_files = self.finder.find_files("./testdata/")
        trimmedFiles = [
                 'sourceFile.c',
                 'sourceFile.js',
                 'sourceFile.html',
                 'sourceFile.py',
                 'sourceFile.go',
                 'sourceFile.ts',
                 'sourceFile.cpp',
                 'sourceFile.css',
                 ]
        for _, d, _ in all_files:
            self.finder.ignoreItems(True, d)
            self.assertEqual(['newdir'], d)
            break
        for _, _, f in all_files:
            self.finder.ignoreItems(False, f)
            self.assertEqual(trimmedFiles, f)
            break

    def test_ignore(self):
        all_files = self.finder.find_files("./testdata/")
        files_after_ignore = self.finder.ignore(all_files)
        self.assertEqual(notIgnoredFiles, files_after_ignore)

    def test_get_files(self):
        files = self.finder.get_files("./testdata/")
        self.assertEqual(notIgnoredFiles, files)


class TestFileFormat(unittest.TestCase):
    def setUp(self):
        self.ff = file_format()

    def test_comment_syntax(self):
        self.assertEqual(self.ff.comment_syntax('correct.py'), ["#"])
        self.assertEqual(self.ff.comment_syntax('Dockerfile'), ["#"])
        self.assertEqual(self.ff.comment_syntax('website.html'),
                         ["<!--", "-->"])
        self.assertEqual(self.ff.comment_syntax('styling.css'), ["/*", "*/"])
        for incorrect in ['incorrect', 'noExt']:
            with self.assertRaises(ValueError):
                self.ff.comment_syntax(incorrect)

    def test_add(self):
        testFormats = [
                ('Dockerfile', '#'),
                ('.ext', '#'),
                ]
        ff = file_format({}, [])
        for t, s in testFormats:
            ff.add(t, s)

        self.assertEqual(ff.ext, {"ext": "#"})
        self.assertEqual(ff.fileregex, [("Dockerfile", "#")])

    def test_add_ext(self):
        self.ff.add_ext("not", ["!!"])
        self.assertEqual(self.ff.comment_syntax("file.not"), ["!!"])

    def test_add_filere(self):
        self.ff.add_filere("Somefilename", ["!!"])
        self.assertEqual(self.ff.comment_syntax("Somefilename"), ["!!"])


class TestTopLicense(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.uncommented = """this is a supposed license text that goes
at the top saoiudhjasoid aoiahsdio;asldasdb salkdha
with some asoidjasoidas  $9058 %%%%@!!!<F13>@)(!*@
and then the end
"""
        hashtag = """#
# this is a supposed license text that goes
# at the top saoiudhjasoid aoiahsdio;asldasdb salkdha
# with some asoidjasoidas  $9058 %%%%@!!!<F13>@)(!*@
# and then the end
#
"""
        slashslash = """//
// this is a supposed license text that goes
// at the top saoiudhjasoid aoiahsdio;asldasdb salkdha
// with some asoidjasoidas  $9058 %%%%@!!!<F13>@)(!*@
// and then the end
//
"""
        html = """<!-- -->
<!-- this is a supposed license text that goes -->
<!-- at the top saoiudhjasoid aoiahsdio;asldasdb salkdha -->
<!-- with some asoidjasoidas  $9058 %%%%@!!!<F13>@)(!*@ -->
<!-- and then the end -->
<!-- -->
"""

        cls.euplCommented = """//
// Copyright %d %s
//
//  Licensed under the EUPL, Version 1.2 or – as soon they
// will be approved by the European Commission - subsequent
// versions of the EUPL (the "Licence");
//  You may not use this work except in compliance with the
// Licence.
//  You may obtain a copy of the Licence at:
//
//  https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
//
//  Unless required by applicable law or agreed to in
// writing, software distributed under the Licence is
// distributed on an "AS IS" basis,
//  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
// express or implied.
//  See the Licence for the specific language governing
// permissions and limitations under the Licence.
//

"""

        cls.syntax_and_hardcoded_text = [
                (["#"], hashtag),
                (["//"], slashslash),
                (["<!--", "-->"], html),
        ]

    def test_already_has_license(self):
        dst_path = "test_file_should_not_exist.go"
        src_path = "./testdata/sourceFile.go"
        copyfile(src_path, dst_path)
        name = "John Doe"
        date = datetime.now().year
        top = comment_out(euplTop, ["//"]) % (date, name)
        self.assertFalse(already_has_license(dst_path, top))
        write_top(top, dst_path)
        self.assertTrue(already_has_license(dst_path, top))
        os.remove(dst_path)

    def test_write_top(self):
        dst_path = "test_file_should_not_exist.go"
        src_path = "./testdata/sourceFile.go"
        with open(src_path) as f:
            src_content = f.read()
        for s, ht in self.syntax_and_hardcoded_text:
            copyfile(src_path, dst_path)
            write_top(comment_out(self.uncommented, s), dst_path)
            with open(dst_path) as f:
                dst_content = f.read()
            self.assertEqual(ht+"\n"+src_content, dst_content)
            os.remove(dst_path)
        # same but using actual license
        copyfile(src_path, dst_path)
        name = "John Doe"
        date = datetime.now().year
        write_top(comment_out(euplTop, ["//"]) % (date, name), dst_path)
        with open(dst_path) as f:
            dst_content = f.read()
        self.assertEqual(dst_content, self.euplCommented % (date, name)+src_content)
        os.remove(dst_path)

    def test_comment_out(self):
        for s, ht in self.syntax_and_hardcoded_text:
            commented = comment_out(self.uncommented, s)
            self.assertEqual(commented, ht)


class TestFunctions(unittest.TestCase):
    def test_syntax_arg(self):
        self.assertEqual(syntax_arg("hello=world"), ('hello', 'world'))
        self.assertNotEqual(syntax_arg("hello=asdoisd"), ('hello', 'world'))
        for inc in ["hello=asdoisd=asd09", "heasodijasd"]:
            with self.assertRaises(ValueError):
                syntax_arg(inc)

    def test_write_full(self):
        write_full("This is not a license", ".", "TESTLICENSE", "x")
        self.assertTrue(os.path.isfile("TESTLICENSE"))
        with self.assertRaises(FileExistsError):
            write_full("This is not a license", ".", "TESTLICENSE", "x")
        write_full("This is not a license", ".", "TESTLICENSE", "w")
        self.assertTrue(os.path.isfile("TESTLICENSE"))
        os.remove("TESTLICENSE")


class TestFindRoot(unittest.TestCase):
    def setUp(self):
        self.hardcoded_path = os.path.abspath("./testdata/.hiddenDir/.git")

    def tearDown(self):
        os.rmdir(self.hardcoded_path)

    def test_find_root(self):
        os.mkdir(self.hardcoded_path)
        root_path = find_root("./testdata")
        self.assertEqual(root_path, os.path.dirname(self.hardcoded_path))
        self.assertNotEqual(root_path, "./testdata")


if __name__ == '__main__':
    unittest.main()
