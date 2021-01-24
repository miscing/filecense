from setuptools import setup, find_packages
import os
import glob
import shutil
from distutils.cmd import Command


class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""
    CLEAN_FILES = './build ./dist ./*.pyc ./*.tgz ./*.egg-info'.split(' ')
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        here = os.path.dirname(os.path.realpath(__file__))

        for path_spec in self.CLEAN_FILES:
            # Make paths absolute and relative to this path
            abs_paths = glob.glob(os.path.normpath(os.path.join(here, path_spec)))
            for path in [str(p) for p in abs_paths]:
                if not path.startswith(here):
                    # Die if path in CLEAN_FILES is absolute + outside this directory
                    raise ValueError("%s is not a path inside %s" % (path, here))
                print('removing %s' % os.path.relpath(path))
                shutil.rmtree(path)


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
        name='filecense',
        version='0.1',
        packages=find_packages(),
        author="miscing",
        author_email="miscing-public@pm.me",
        description="Adds a license to a project.",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/miscing/filecense",
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)",
            "Operating System :: OS Independent",
            ],
        python_requires='>=3.6',
        )
